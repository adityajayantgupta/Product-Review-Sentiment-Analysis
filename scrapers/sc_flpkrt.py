import requests
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def get_multipage_reviews(url, pages=1):  
    url = url.split("/")
    url[4] = "product-reviews"
    url = "/".join(url)

    multiPageData = []

    for i in range(1,pages+1):    
        response = requests.get(url + '&page=' + str(i), headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        multiPageData.append(soup)
    
    return multiPageData

def review_scrapper(soup):
  rows = soup.find_all('div',attrs={'class':'col _2wzgFH K0kLPL'})
  reviews = []
  for row in rows:
      sub_row = row.find_all('div',attrs={'class':'row'})      
      review = sub_row[1].find_all('div')[2].text
      reviews.append(review)
  return reviews

def get_flp_reviews(url, pages=1):
  multiPageData = get_multipage_reviews(url,pages)
  reviews = []
  for page in multiPageData:
      reviews.extend(review_scrapper(page))
  return reviews

def get_flp_product_data(url):
  response = requests.get(url, headers=HEADERS)
  soup = BeautifulSoup(response.text, 'html.parser')

  product_rating=soup.find('div', attrs={'class':'_3LWZlK'}).text
  product_price=soup.find('div', attrs={'class':'_30jeq3 _16Jk6d'}).text
  product_image_url = soup.find('img', attrs={'class': "_396cs4 _2amPTt _3qGmMb"})['src']
  product_name = soup.find('span', attrs={'class': "B_NuCI"}).text

  return {"product_name": product_name, "product_price": product_price, "product_rating": product_rating, "product_image_url":product_image_url}

  

