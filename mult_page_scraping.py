import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def multi_page_scrap(url):
    '''This function scraps books on books.toscrape.com'''

    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = bs(response.text, 'lxml').find('ol', attrs={'class': 'row'})
    books = soup.find_all('li')

    books_list = []
    for book in books:
        title = book.select_one('h3').find('a')['title']
        book_img = 'https://books.toscrape.com/catalogue/' + book.find('div', attrs={'class':'image_container'}).find('a')['href']
        book_link = 'https://books.toscrape.com/catalogue/' + book.select_one('h3').find('a')['href']
        price = book.find('p', class_='price_color').text
        books_list.append({'title': title,
                           'image': book_img,
                           'link': book_link,
                           'price': price[1:]})

    return books_list

def next_page(url):
    """The function returns a link to the next page on books.toscrape.com"""

    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = bs(response.text, 'lxml')
    next_page_tag = soup.find('li', attrs={'class': 'next'})
    if next_page_tag:
        next_page_href = 'https://books.toscrape.com/catalogue/' + next_page_tag.find('a')['href']
        return next_page_href
    else:
        return None


def main():
    final_books_list = []
    current_url = 'https://books.toscrape.com/catalogue/page-1.html'

    while current_url:
        books_on_page = multi_page_scrap(current_url)
        if books_on_page:
            final_books_list.extend(books_on_page)

        current_url = next_page(current_url)

    pd_table = pd.DataFrame(final_books_list)
    pd_table.to_csv(sep=';', encoding='utf-8', path_or_buf=r'D:\parsers\req_bs4_tries\books.csv')


if __name__ == '__main__':
    main()