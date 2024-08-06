import requests
from bs4 import BeautifulSoup
from time import sleep


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
BASE_URL = 'https://scrapingclub.com/'

def collect_links():
    """Function=generator yields links one by one"""
    for page in range(1, 7):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={page}'
        try:
            response = requests.get(url=url, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('div', attrs={'class': 'w-full rounded border'})

        for link in links:
            card_link = BASE_URL + link.find('a')['href']
            yield card_link


def scraping_data():
    """This function collects data from scraping.club.com and yields them one by one for further usage"""

    for link in collect_links():
        response = requests.get(url=link, headers=HEADERS)
        sleep(1)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h3', class_='card-title').text
        price = soup.find('h4', class_='my-4 card-price').text
        description = soup.find('p', class_='card-description').text
        img_link = BASE_URL + soup.find('img', class_='card-img-top')['src']

        yield title, price, description, img_link

