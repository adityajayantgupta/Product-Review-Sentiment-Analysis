import concurrent.futures
import multiprocessing as mp
import urllib.parse

import requests
from bs4 import BeautifulSoup
from flask import Flask, request
from flask_cors import CORS

from modules.keywordExtractor import KeywordExtractor
from modules.sentimentAnalyzer import SentimentAnalyzer
from modules.summarizer import ReviewSummarizer
from scrapers.sc_amzn import get_amz_product_data, get_amz_reviews
from scrapers.sc_flpkrt import get_flp_product_data, get_flp_reviews

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def get_summary(reviews):
    return ReviewSummarizer(reviews, max_length=150, min_length=100)

def get_sentiment(reviews):
    return SentimentAnalyzer(reviews)

def get_keywords(reviews):
    return KeywordExtractor(reviews)

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

        print(query_url)

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
      
app = Flask(__name__)
cors = CORS(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


def generate_analysis(url, reviews_func):
    reviews = reviews_func(url)
    return {
        "sentiment_score": get_sentiment(reviews),
        "keywords": get_keywords(reviews),
        "summary": get_summary(reviews)
    }

def generate_result(site, url, data_function, reviews_func):
    result = {
        site: {
            "product_data": data_function(url),
            "analysis": generate_analysis(url, reviews_func) 
        },
    } 
    return result     

def generate_combined_result(url_amz, url_flp):
    result = {
        "amazon": {
            "product_data": get_amz_product_data(url_amz),
            "analysis": {}
        },
        "flipkart": {
            "product_data": get_flp_product_data(url_flp),
            "analysis": {}
        }
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(generate_analysis, url_amz, get_amz_reviews): result["amazon"]["analysis"],
            executor.submit(generate_analysis, url_flp, get_flp_reviews): result["flipkart"]["analysis"]
        }

        for future, site_analysis in futures.items():
            site_analysis.update(future.result())

    return result

@app.route('/analyze', methods=['GET'])
def analyze():
    print("received request")
    args = request.args
    url_amz = args.get('url_amz')
    url_flp = args.get('url_flp')

    if url_amz and url_flp:
      return generate_combined_result(url_amz, url_flp)
    elif url_amz:
        url_flp = product_finder(url_amz=url_amz, url_flp=None)
        
        if (url_flp is not None):
            return generate_combined_result(url_amz, url_flp)
        else:
            return generate_result("amazon", url_amz, get_amz_product_data, get_amz_reviews)
            
    elif url_flp:            
        url_amz = product_finder(url_amz=None, url_flp=url_flp)
        
        if (url_amz is not None):
            return generate_combined_result(url_amz, url_flp)
        else:    
            return generate_result("flipkart", url_flp, get_flp_product_data, get_flp_reviews)  
