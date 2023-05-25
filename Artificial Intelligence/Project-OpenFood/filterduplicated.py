FILENAME = 'product_url_1000.txt'
FILENAME2 = 'product_url_100.txt'

with open(FILENAME, 'r') as f:
    urls = f.readlines()

with open(FILENAME2, 'r') as f:
    urls2 = f.readlines()

url_filtered = [url if url not in urls2 else '' for url in urls]

with open('product_url_filtered.txt', 'w') as f:
    f.writelines(url_filtered)