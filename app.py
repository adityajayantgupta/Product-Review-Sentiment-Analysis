import concurrent.futures
import multiprocessing as mp
import urllib.parse

import requests
from bs4 import BeautifulSoup
from flask import Flask, request
from flask_cors import CORS

from database.brandReputationIndex import update_brand_score
from database.cacheAnalysis import check_cached_product, store_analyzed_product
from modules.keywordExtractor import KeywordExtractor
from modules.reviewSentimentTagger import ReviewSentimentTagger
from modules.sentimentAnalyzer import SentimentAnalyzer
from modules.summarizer import ReviewSummarizer
from scrapers.sc_amzn import get_amz_product_data, get_amz_reviews
from scrapers.sc_flpkrt import get_flp_product_data, get_flp_reviews

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

app = Flask(__name__)
cors = CORS(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

def get_summary(reviews):
    return ReviewSummarizer(reviews, max_length=150, min_length=100)

def get_tagged_summary(reviews):
    return ReviewSentimentTagger(reviews)

def get_sentiment(reviews):
    return SentimentAnalyzer(reviews)

def get_keywords(reviews):
    return KeywordExtractor(reviews)

def get_product_data(platform, url):
    if platform == "amazon":
        return get_amz_product_data(url)
    elif platform == "flipkart":
        return get_flp_product_data(url)
    else:
        return None    

def get_reviews(platform, url):
    if platform == "amazon":
        return get_amz_reviews(url)
    elif platform == "flipkart":
        return get_flp_reviews(url)
    else:
        return None

def product_finder(url_amz=None, url_flp=None):
    if not url_amz and not url_flp:
        return
    elif url_amz:
        # Get product name from url
        product_data = get_amz_product_data(url_amz)
        product_name = urllib.parse.quote(product_data["product_name"])
        # Search query url for the product in Flipkart
        query_url = f"https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

        response = requests.get(query_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.find_all('div', {'class': '_1AtVbE col-12-12'})

        # Find the first search result and scrape the url
        if len(container) > 0:            
            for result in container:
                product = result.find('div', {'class':'_4ddWXP'})
                if product is not None:
                    return 'https://www.flipkart.com' + product.find('a')['href'] 
        else:
            return None
    elif url_flp:
        # Get product name from url
        product_data = get_flp_product_data(url_flp)
        product_name = urllib.parse.quote(product_data["product_name"])
        # Search query url for the product in Amazon
        query_url = f"https://www.amazon.in/s?k={product_name}"

        response = requests.get(query_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', {'class': ['s-result-item'], 'data-component-type': 's-search-result'})
        
        # Filter out sponsored results
        for r in results:
            if 'AdHolder' not in r.get('class'):
                return 'https://www.amazon.in' + (r.find('a')['href'])
        return None
    
def store_results(result, site):    
    brand = result[site]["product_data"]["product_name"].split(" ")[0]
    sentiment_score = result[site]["analysis"]["sentiment_score"]

    update_brand_score(brand, sentiment_score, site)
    store_analyzed_product(result, site)

def generate_analysis(platform, url, reviews_func):
    reviews = reviews_func(platform, url)
    sentiment = get_sentiment(reviews)
    keywords = get_keywords(reviews)
    summary = get_summary(reviews)
    tagged_summary = get_tagged_summary(summary)

    return {
        "sentiment_score": sentiment ,
        "keywords": keywords,
        "summary": summary,
        "tagged_summary": tagged_summary,
    }

def generate_single_result(site, url, data_function, reviews_func):
    result = {
        site: {
            "product_data": data_function(url),
            "analysis": {} 
        },
    }

    result[site]["analysis"] = check_cached_product(result[site]["product_data"]["product_name"])["analysis"] or generate_analysis(url, reviews_func)
                        
    store_results(result, site)
    return result

def generate_combined_result(req_one, req_two, autoMatchPlatform = None):  
    result = {}

    result[req_one["platform"]] = {
        "product_data": get_product_data(req_one["platform"], req_one["url"]),
        "autoMatch": False,
        "analysis": {}
    }

    result[req_two["platform"]] = {
        "product_data": get_product_data(req_two["platform"], req_two["url"]),
        "autoMatch": False,
        "analysis": {}
    }

    if autoMatchPlatform is not None:
        result[autoMatchPlatform]["autoMatch"] = True

    result[req_one["platform"]]["analysis"] = check_cached_product(result[req_one["platform"]]["product_data"]["product_name"])["analysis"]
    result[req_two["platform"]]["analysis"] = check_cached_product(result[req_two["platform"]]["product_data"]["product_name"])["analysis"]


    if not result[req_one["platform"]]["analysis"] and not result[req_two["platform"]]["analysis"]:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(generate_analysis, req_one["platform"], req_one["url"], get_reviews): result[req_one["platform"]]["analysis"],
                executor.submit(generate_analysis, req_two["platform"], req_two["url"],  get_reviews): result[req_two["platform"]]["analysis"]
            }

            for future, site_analysis in futures.items():
                site_analysis.update(future.result())
    elif not result[req_one["platform"]]["analysis"]:
        result[req_one["platform"]]["analysis"] = generate_analysis(req_one["platform"], req_one["url"],get_reviews)
    else:        
        result[req_two["platform"]]["analysis"] = generate_analysis(req_two["platform"], req_two["url"],get_reviews)

    # Update brand quality index for Amazon
    store_results(result, req_one["platform"])
    store_results(result, req_two["platform"])

    return result

def handle_single_platform_request (url, platform):    
    if platform == "amazon":
        url_flp = product_finder(url_amz=url, url_flp=None)

        if (url_flp is not None):
            return generate_combined_result({"url": url, "platform": "amazon"}, {"url": url_flp, "platform": "flipkart"}, autoMatchPlatform = "flipkart")
        else:
            return generate_single_result("amazon", url_amz, get_amz_product_data, get_amz_reviews)
            
    elif platform == "flipkart":
        url_amz = product_finder(url_amz=None, url_flp=url)

        if (url_amz is not None):
            return generate_combined_result({"url": url_amz, "platform": "amazon"}, {"url": url, "platform": "flipkart"}, autoMatchPlatform = "amazon")
        else:    
            return generate_single_result("flipkart", url_flp, get_flp_product_data, get_flp_reviews)  



def handle_multi_platform_request (req_one, req_two):
    return generate_combined_result(req_one, req_two, autoMatchPlatform = None)


@app.route('/analyze', methods=['GET'])
def analyze():
    print("received request")
    args = request.args
    platformOne = args.get('platformOne')
    platformTwo = args.get('platformTwo')

    if platformOne and platformTwo:
        return handle_multi_platform_request(
            {
                "url": args.get("urlOne"),
                "platform": platformOne,
            }, {
                "url": args.get("urlTwo"),
                "platform": platformTwo,
            }
        ) 
    elif platformOne or platformTwo:
        url = args.get('urlOne') or args.get('urlTwo')
        platform = args.get('platformOne') or args.get('platformTwo')
        return handle_single_platform_request(url, platform)