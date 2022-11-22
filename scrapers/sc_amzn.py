
# import module
import requests
import sys
from bs4 import BeautifulSoup
# from happytransformer import HappyTextClassification


#happy_tc = HappyTextClassification(model_type="DISTILBERT", model_name="distilbert-base-uncased-finetuned-sst-2-english", num_labels=2)
  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
  
  
def get_soup(url):  
    # pass the url
    # into getdata function
    htmldata = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(htmldata.text, 'html.parser')
      
    # display html code
    return (soup)

def product_data(soup):
  name = soup.find(id="productTitle")
  return name.get_text()


def cus_data(soup):
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    cus_list = []
  
    for item in soup.find_all("span", class_="review-text"):
        data_str = data_str + item.get_text()
        cus_list.append(data_str)
        data_str = ""
    return cus_list
  

if __name__ == "__main__":
    url = sys.argv[1]
    print(url)
    soup = get_soup(url)
    product_name = product_data(soup)
    reviews = cus_data(soup)

    for r in reviews:
        print(r)


    