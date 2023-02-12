
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

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):
    price = soup.find("span", attrs={'class':'a-price-whole'}).text
    print(price)
    return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

def get_image_url(soup):
    try:
        image = soup.find("img", attrs={'id':'landingImage'})
        imageURL = image.get('src')
    except: 
        imageURL = ""
    return imageURL
        

def get_amz_product_data(url):
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.text, "html.parser")
    result = {"title": get_title(soup), "price": get_price(soup), "rating":get_rating(soup), "imageURL": get_image_url(soup)," productURL":url}
    return result


def extract_reviews(url, pages=1):
    multiPageData = get_multipage_reviews(url,pages)
    data_str = ""
    reviews = []
    for page in multiPageData:
        for item in page.find_all("span", class_="review-text"):
            data_str = data_str + item.get_text()
            reviews.append(data_str)
            data_str = ""
    return reviews