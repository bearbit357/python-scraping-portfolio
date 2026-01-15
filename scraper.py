from bs4 import BeautifulSoup
import requests
from time import sleep
import pandas as pd

url = 'https://books.toscrape.com/catalogue/page-{}.html'
d_list = []
page = 1


while True:
    r = requests.get(url.format(page))
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    contents = soup.find_all('article',class_='product_pod')
    main_url = 'https://books.toscrape.com/catalogue/'

    # 一つの要素の取得
    for content in contents:
        title = content.find('h3').find('a').get('title')
        c = content.find('div',class_='product_price').find_all('p')
        price = c[0].text
        stock = c[1].text.strip()
        product_url = main_url + content.find('h3').find('a').get('href')
        d = {
            'title':title,
            'price':price,
            'stock':stock,
            'product_url':product_url
        }
        d_list.append(d)

    sleep(1)
    page += 1
    if not soup.find('li', class_='next'):
        break

df = pd.DataFrame(d_list)
df.to_csv('books.csv',encoding='utf-8-sig')
