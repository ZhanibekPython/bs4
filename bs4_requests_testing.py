import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def get_books(url: str) -> None:
    request = requests.get(url)

    books_html = bs(request.text, 'html.parser')

    books_section = books_html.select_one('section').find('ol', attrs = {'class': 'row'}).find_all('li')

    result = []

    for book in books_section:
        title = book.find('h3').find('a')['title']
        link = 'https://books.toscrape.com/' + book.find('h3').find('a')['href']
        price = book.find('p', class_='price_color').text[1:]
        result.append({'title': title,
                                'link': link,
                                'price': price})

    with open('parsed_books.txt', 'w', encoding='utf-8') as file:
        file.write(str(result))


get_books('https://books.toscrape.com/')

