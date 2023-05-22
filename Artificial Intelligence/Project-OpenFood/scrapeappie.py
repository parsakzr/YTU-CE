from bs4 import BeautifulSoup
import requests
import csv

BASE_URL = 'https://www.ah.nl/producten/product/'

product_list = []

def get_product_info(url):
    '''
    Get Nutrients table from product page
    '''
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())

        product = {}
        # Get product name
        productname_div = soup.find('div', {'class': 'product-card-header_root__c8eM5'})
        if productname_div:
            productname = productname_div.span.text # Example: 'AH Scharrel kipfilet'
            product['name'] = productname

        # Get product score
        productscore_div = soup.find('div', {'class': 'nutriscore_root__clyII'})
        if productscore_div:
            productscore = productscore_div.svg.title.text # Example: 'Nutri-Score A'
            # remove 'Nutri-Score ' from productscore
            productscore = productscore.replace('Nutri-Score ', '')
            product['score'] = productscore
            
        # Get Nutrients table
        nutr_table = soup.find('table', {'class': 'product-info-nutrition_table__Q3m80'})
        if nutr_table:
            nutr_table_rows = nutr_table.tbody.find_all('tr') # Example [<tr><td class="">Vet</td><td>1.2 g</td></tr>]
            # Get Nutrients table data
            for row in nutr_table_rows:
                td_list = row.findChildren('td')
                row_header = td_list[0].text
                row_value = td_list[1].text
                if(row_header == 'Energie'): # Example value: '107 kJ (25 kcal)'
                    # filter only the kcal number
                    row_value = float(row_value.split()[2].replace('(', ''))
                else: # Nutrient values per 100g, Example value: '1.2 g'
                    # filter only the number
                    value, unit = row_value.split()
                    if unit == 'mg':
                        row_value = float(value) / 1000
                    elif unit == 'µg':
                        row_value = float(value) / 1000000
                    else:
                        row_value = float(value)
                    
                product[row_header] = row_value
                
        # print(f'{product=}')
        product_list.append(product)

    except Exception as e:
        print(f'[E] Error fetching {url} : {e}')
    

def write_csv(filename, product_list):
    # Get all possible keys from all products
    all_keys = []
    for product in product_list:
        for key in product.keys():
            if key not in all_keys:
                all_keys.append(key)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(product_list)


if __name__ == '__main__':
    with open('product_urls.txt', 'r') as f:
        urls = f.readlines()
        for url in urls:
            get_product_info(url.strip())

    print(f'{product_list=}')
    write_csv('data/ah.csv', product_list)