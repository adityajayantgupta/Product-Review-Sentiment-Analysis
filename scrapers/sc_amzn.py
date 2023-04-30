
# import module
import requests
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
  
def get_multipage_reviews(url, pages=1):  
    url = url.split("/")
    url = list(map(lambda x: x.replace('dp', 'product-reviews'), url))
    url = "/".join(url)

    multiPageData = []

    for i in range(1,pages+1):    
        response = requests.get(url + '&pageNumber=' + str(i), headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        multiPageData.append(soup)
    
    return multiPageData

def get_amz_product_data(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Extract the product name
    product_name = soup.find('span', {'id': 'productTitle'}).text.strip()

    # Extract the product price
    product_price = soup.find('span', {'class': 'a-price-whole'}).text.strip()

    # Extract the product rating
    product_rating = soup.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]

    # Extract the product image URL
    product_image_url = soup.find('img', {'id': 'landingImage'})['data-old-hires']

    return {"product_name": product_name, "product_price": product_price, "product_rating": product_rating, "product_image_url":product_image_url, "product_url": url}



def get_amz_reviews(url, pages=1):
    multiPageData = get_multipage_reviews(url,pages)
    reviews = []
    for page in multiPageData:
        review_containers = page.find_all('div', {'data-hook': 'review'})
        for container in review_containers:
            review_text = container.find('span', {'data-hook': 'review-body'}).text.strip()
            review_text = review_text.replace('\n', '').replace('\t', '')
            verified_purchase = 'Verified Purchase' in container.find('span', {'class': 'a-size-mini a-color-state a-text-bold'}).text
            review_item = {
                 "review_text": review_text,
                 "verified_purchase": verified_purchase or False
            }
            reviews.append(review_text)            
    return reviews

