import math
from urllib.request import urlopen
import requests
import json
# CURRENCIES


def get_coin(coin):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'X-CMC_PRO_API_KEY': '6969b5bb-8ab5-49c1-982a-ba5cd0cee301',
        'Accepts': 'application/json'
    }
    params = {
        'start': '1',
        'limit': '50',
        'convert': 'USD'
    }
    json = requests.get(url, params=params, headers=headers).json()
    coins = json['data']

    i = 0
    cripto = {}
    for x in coins:
        cripto[x['symbol']] = (round(x['quote']['USD']['price'], 4))

    if coin in cripto:
        return cripto[coin]
    else:
        print("o ne la")
        return -1


def get_currency(currency):
    url_usd = 'http://api.exchangeratesapi.io/v1/latest?access_key=0b2b169eca6bb72dada577d1274cc531'
    result = requests.get(url_usd).json()
    date = result['date']

    eu_tr = float(result['rates']['TRY'])
    usd_eu = float(result['rates']['USD'])
    usd_tr = eu_tr / usd_eu

    if currency == 'EUR':
        return (round(eu_tr, 2))
    elif currency == 'USD':
        return (round(usd_tr, 2))
    else:
        return -1


def get_weather(city_name):
    api_key = "cac3fbb48ecfcc9ba91bfdb00abdb2bb"
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid='+api_key
    response = requests.get(url).json()
    with urlopen(url) as data:
        source = data.read()

    data = json.loads(source)
    temp = response['main']['temp']
    temp = math.floor(float(temp)-273.15)
    return temp
