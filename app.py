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


@app.route('/analyze', methods=['GET'])
def analyze():
    print("received request")
    args = request.args
    url_amz = args.get('url_amz')
    url_flp = args.get('url_flp')
    result = {
        "amazon" : {
            "product_data":None,
            "analysis": {
                "sentiment_score": 0,
                "keywords": [],
                "summary": ""
            }
        },
        "flipkart": {
            "product_data":None,
            "analysis": {
                "sentiment_score": 0,
                "keywords": [],
                "summary": ""
            }
        
        }
    }

    if url_amz and url_flp:
      result["amazon"]["product_data"] = get_amz_product_data(url_amz)
      result["flipkart"]["product_data"] = get_flp_product_data(url_flp)

      amz_reviews = get_amz_reviews(url_amz)
      flp_reviews = get_flp_reviews(url_flp)

      result["amazon"]["analysis"] = {
          "sentiment_score": get_sentiment(amz_reviews),
          "keywords": get_keywords(amz_reviews),
          "summary": get_summary(amz_reviews),
      }

      result["flipkart"]["analysis"] = {
          "sentiment_score": get_sentiment(flp_reviews),
          "keywords": get_keywords(flp_reviews),
          "summary": get_summary(flp_reviews),
      }
    elif url_amz:
        url_flp = product_finder(url_amz=url_amz, url_flp=None)

        print(url_flp)
        
        if (url_flp is not None):
            result["amazon"]["product_data"] = get_amz_product_data(url_amz)
            result["flipkart"]["product_data"] = get_flp_product_data(url_flp)

            amz_reviews = get_amz_reviews(url_amz)
            flp_reviews = get_flp_reviews(url_flp)

            result["amazon"]["analysis"] = {
                "sentiment_score": get_sentiment(amz_reviews),
                "keywords": get_keywords(amz_reviews),
                "summary": get_summary(amz_reviews),
            }

            result["flipkart"]["analysis"] = {
                "sentiment_score": get_sentiment(flp_reviews),
                "keywords": get_keywords(flp_reviews),
                "summary": get_summary(flp_reviews),
            }
        else:
            result["amazon"]["product_data"] = get_amz_product_data(url_amz)

            amz_reviews = get_amz_reviews(url_amz)

            result["amazon"]["analysis"] = {
                "sentiment_score": get_sentiment(amz_reviews),
                "keywords": get_keywords(amz_reviews),
                "summary": get_summary(amz_reviews),
            }
    elif url_flp:            
        url_amz = product_finder(url_amz=None, url_flp=url_flp)
        
        if (url_amz is not None):
            result["amazon"]["product_data"] = get_amz_product_data(url_amz)
            result["flipkart"]["product_data"] = get_flp_product_data(url_flp)

            amz_reviews = get_amz_reviews(url_amz)
            flp_reviews = get_flp_reviews(url_flp)

            result["amazon"]["analysis"] = {
                "sentiment_score": get_sentiment(amz_reviews),
                "keywords": get_keywords(amz_reviews),
                "summary": get_summary(amz_reviews),
            }

            result["flipkart"]["analysis"] = {
                "sentiment_score": get_sentiment(flp_reviews),
                "keywords": get_keywords(flp_reviews),
                "summary": get_summary(flp_reviews),
            }
        else:            
            result["flipkart"]["product_data"] = get_flp_product_data(url_flp)

            flp_reviews = get_flp_reviews(url_flp)
            

            result["flipkart"]["analysis"] = {
                "sentiment_score": get_sentiment(flp_reviews),
                "keywords": get_keywords(flp_reviews),
                "summary": get_summary(flp_reviews),
            }
    return result


            

