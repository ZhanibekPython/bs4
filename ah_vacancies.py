import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
from pyfiglet import Figlet
from time import sleep


ua = FakeUserAgent()
vacancy_url = "https://astanahub.com/ru/vacancy/"


def get_vacancy_list(url: str) -> list:
    """This function obtains vacancies data from astana-hub web-site"""

    for page in range(1, 89):
        try:
            response = requests.get(f"{url}?page={page}", headers={'User-Agent': ua.random})
            response.raise_for_status()
        except requests.exceptions.RequestException as ex:
            print(f"Got mistake {ex}, at page{page}")
            continue

        try:
            soup = BeautifulSoup(response.text, "lxml")
            vacancies = soup.find('div', class_='load-content').find_all('div', class_='card-vacancy')

            for vacancy in vacancies:
                link = vacancy.find('a', class_='vacancy-body').get('href')
                if link:
                    yield link
                else:
                    print('Link was not found')
                    continue

        except Exception as ex:
            print(f"The following mistake appeared, {ex}. The script was stopped")
            break



def get_data_from_link(link: str) -> None:
    """This functions scrapes data from given link"""

    try:
        response = requests.get(url=link, headers={'User-Agent': ua.random})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        try:
            title = "\n" + soup.find('h1', class_='block-title').get_text(strip=True)
            short_description = soup.find('div', class_='tiny-content vacancy-content').find_all('p')[1].get_text(strip=True)
        except:
            raise
        
        try:
            with open('astana_hub/all_data.csv', 'a', newline='\n', encoding='utf-8') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                writer.writerow([title, short_description])
        except FileNotFoundError:
            print("The file was not found")


    except requests.exceptions.RequestException as ex:
        print(f"Got mistake {ex}")


def main():
    text = Figlet(font="doh", width=275)
    print(text.renderText("Salem"))

    links = get_vacancy_list(url=vacancy_url)
    for link in links:
        get_data_from_link(link)
        sleep(1)
        

if __name__ == '__main__':
    main()
    print("Scraping task is done!")