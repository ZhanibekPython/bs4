import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


books_dict = {}
for i in range(1, 11):
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    response = requests.get(url=url)
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, 'lxml')
        books = bs.select_one('ol[class=row]').find_all('li')
        for book in books:
            name = book.find('h3').find('a')['title']
            link = 'https://books.toscrape.com/' + book.find('a')['href']
            price = book.select_one('p[class=price_color]').text
            books_dict[name] = [link, price]

    else:
        continue

print(len(books_dict))
