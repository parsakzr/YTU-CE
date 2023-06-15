from bs4 import BeautifulSoup
import requests
import csv

BASE_URL = 'https://www.carrefour.fr/'

def get_product_info(url):
    '''
    Get Nutrients table from product page
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())
    productscore_div = soup.find('div', {'class': 'main-details--food__scores'})
    nutr_details = soup.find('table', {'class': 'nutritional-details'})

    print(productscore_div)


get_product_info("https://www.carrefour.fr/p/jambon-le-paris-cuit-a-l-etouffee-carrefour-classic-3560071096298")