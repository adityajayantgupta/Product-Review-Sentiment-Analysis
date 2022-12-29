import requests
from bs4 import BeautifulSoup

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

def cus_data(soup):
  rows = soup.find_all('div',attrs={'class':'col _2wzgFH K0kLPL'})
  print(f"Number of reviews:{len(rows)}\n\n\n")
  for row in rows:
      sub_row = row.find_all('div',attrs={'class':'row'})
      
      review = sub_row[1].find_all('div')[2].text
      print(f"review:{review} \n\n")

def flipkart_scrapper(url):
  soup = get_soup(url)
  reviews = cus_data(soup)
  return reviews


  