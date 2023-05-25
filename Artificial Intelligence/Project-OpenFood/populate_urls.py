import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.ah.nl'
CATEGORY_URLS = [
    'https://www.ah.nl/producten/vlees-kip-vis-vega',
    'https://www.ah.nl/producten/kaas-vleeswaren-tapas',
    'https://www.ah.nl/producten/zuivel-plantaardig-en-eieren',
    'https://www.ah.nl/producten/ontbijtgranen-en-beleg',
    'https://www.ah.nl/producten/tussendoortjes',
    'https://www.ah.nl/producten/frisdrank-sappen-koffie-thee'
]
NUMOFPRODUCTS = 100

def getProductURLs_from_page(url):
    '''
    Get a list of product urls from a specific category in ah.nl
    '''
    urls = []
    try:
        print(f'Fetching from {url}')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())

        # Get product name
        productcards = soup.findAll('article', {'class': 'product-card-portrait_root__ZiRpZ'})
        print(f'found {len(productcards)} product cards')
        '''
        Example:
        <article class="product-card-portrait_root__ZiRpZ product-grid-lane_gridItems__BBa4h" data-testhook="product-card"><div class="header_root__ilMls"><a href="/producten/product/wi221032/meester-en-zn-gerookte-spekreepjes" title="Meester &amp; Zn. Gerookte spekreepjes" class="link_root__EqRHd" data-analytics="LINK_CLICK" data-analytics-meta="%7B%22id%22%3A%22wi221032%22%2C%22key%22%3A%22products%22%2C%22href%22%3A%22%2Fproducten%2Fproduct%2Fwi221032%2Fmeester-en-zn-gerookte-spekreepjes%22%7D"><figure class="image_root__Gqe5t product-card-portrait_image__vqWuZ" data-testhook="product-image-wrapper"><div class="lazy-image_root__-m-7n lazy-image_ratio-1-1__3N2eF image_imageElement__0lJ1q"><img class="lazy-image_image__o9P+M" src="https://static.ah.nl/dam/product/AHI_434d50313439323632?revLabel=8&amp;rendition=200x200_JPG_Q85&amp;fileType=binary" alt="Een afbeelding van Meester &amp; Zn. Gerookte spekreepjes" title="Meester &amp; Zn. Gerookte spekreepjes" data-testhook="product-image" loading="lazy"></div></figure><div class="product-card-portrait_pricePromotion__nUtNo"><div class="price_portrait__pcgwD"><div class="price-amount_root__Sa88q price-amount_highlight__ekL92 price_amount__s-QN4 price_highlight__RucvZ" data-testhook="price-amount"><span class="price-amount_integer__+e2XO">3</span><span class="price-amount_dot__MV39M">.</span><span class="price-amount_fractional__kjJ7u">19</span></div><span class="price_unitSize__Hk6E4" data-testhook="product-unit-size">300 g</span></div></div><svg data-testhook="product-highlight" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="sticker-icon highlight_root__lGyLZ highlight_nutriscore-e__EmhfD product-card-portrait_highlight__lTVaU svg svg--svg_nutriscore-e" viewBox="0 0 64 35" width="70" height="70"><use href="#svg_nutriscore-e"></use></svg><div class="product-card-portrait_shieldProperties__+JZJI"><div class="" data-testhook="product-properties"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="properties_icon__jEfU0 svg svg--svg_prijsfavoriet" viewBox="0 0 24 24" width="22" height="22"><title>Prijsfavoriet</title><use href="#svg_prijsfavoriet"></use></svg></div></div></a></div><div class="body_root__3tZaN product-card-portrait_body__VhXD-"><div class="product-card-portrait_actions__xyiw5"><div class="offcanvas_root__JxF2- offcanvas_top__VZfFN"><div class="offcanvas_controls__neXmq"><div class="offcanvas_offCanvas__GW40N"><button tabindex="-1" data-testhook="product-min" class="icon-button_root__EUJjw min-button min-button_root__ZGosY offcanvas_minButton__3agYO" aria-label="Product aantal verminderen met 1" aria-disabled="false" type="button"><svg focusable="false" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="ui-icon_root__gN+Ry icon-button_icon__61nu1 min-button_icon__Uzt4S svg svg--svg_min" viewBox="0 0 12 12" width="30" height="30"><use href="#svg_min"></use></svg></button><input type="number" name="quantity" class="quantity-input quantity-input_root__887nk offcanvas_quantityInput__X35g6" aria-label="Product hoeveelheid aanpassen" data-testhook="product-quantity-input" pattern="[0-9]{1,2}" maxlength="2" max="99" aria-disabled="false" tabindex="-1" autocomplete="off" value="0"><button type="button" class="quantity-button_root__qKVXy offcanvas_quantityInputButton__nKXYV" data-testhook="product-quantity-button" aria-disabled="false">0</button><button theme="ah" data-testhook="product-plus" class="icon-button_root__EUJjw plus-button plus-button_root__ZJFfU offcanvas_plusButton__NwQQ1 offcanvas_showButton__LalTf" aria-label="Product toevoegen" aria-disabled="false" type="button"><svg focusable="false" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="ui-icon_root__gN+Ry icon-button_icon__61nu1 plus-button_icon__cSPiv svg svg--svg_plus" viewBox="0 0 24 24" width="30" height="30"><use href="#svg_plus"></use></svg></button></div><div aria-live="polite" class="sr-only"></div></div></div></div><div class="product-card-portrait_content__DQ9nP"><div class="product-card-portrait_buttonPlaceholder__8yvPJ"></div><a href="/producten/product/wi221032/meester-en-zn-gerookte-spekreepjes" title="Meester &amp; Zn. Gerookte spekreepjes" class="link_root__EqRHd product-card-portrait_link__5VsEK" tabindex="-1" data-analytics="LINK_CLICK" data-analytics-meta="%7B%22id%22%3A%22wi221032%22%2C%22key%22%3A%22products%22%2C%22href%22%3A%22%2Fproducten%2Fproduct%2Fwi221032%2Fmeester-en-zn-gerookte-spekreepjes%22%7D"><strong class="title_root__xSlPL product-card-portrait_title__ZmvmX" data-testhook="product-title"><span class="line-clamp_root__7DevG line-clamp_active__5Qc2L title_lineclamp__kjrFA" style="-webkit-line-clamp: 2; line-height: 1.3em; max-height: 2.6em;">Meester &amp; Zn. Gerookte spekreepjes</span></strong></a></div></div></article>
        '''
        for productcard in productcards:
            header = productcard.findChild('div', {'class': 'header_root__ilMls'})
            if(header == None or header.a == None):
                continue

            header = header.a
            
            # misc. card, product without nutriscore-label
            svg_label = header.findChild('svg')
            if(svg_label == None or 'nutriscore' not in svg_label.get('class')[-1]):
                continue

            url = BASE_URL + header.get('href')
            urls.append(url)
            
    except Exception as e:
        print(f'[E] Error fetching product urls from {url}: {e}')
    
    return urls


if __name__ == '__main__':

    # calculate page numbers for url based on total number of products and pooling from different categories
    # with no page specified, 39 products are shown,
    # with each '?page=x' increment, 36 more products are shown, so 39, 75, 111, 147, etc.

    pageSize_eachCategory = NUMOFPRODUCTS // len(CATEGORY_URLS)
    pageNum = (pageSize_eachCategory - 3) // 36
    
    if(pageNum >= 1):
        pageStr = '?page=' + str(pageNum)
        CATEGORY_URLS = [url+pageStr for url in CATEGORY_URLS]


    print(f'fetching from {CATEGORY_URLS=}')

    productURL_list = []
    for category_url in CATEGORY_URLS:
        urls = getProductURLs_from_page(category_url)
        productURL_list.extend(urls)

    print(f'found {len(productURL_list)} product urls')

    filename = f'product_url_{NUMOFPRODUCTS}.txt'
    with open(filename, 'w') as output:
        for url in productURL_list:
            output.write(url + '\n')
        
    print(f'wrote to {filename}')


    