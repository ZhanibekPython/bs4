import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
MAIN_URL = 'https://quotes.toscrape.com/'
LOGIN_URL = 'https://quotes.toscrape.com/login'

def get_login(main_url: str, login_url: str) -> str:
    session = requests.Session()
    session.get(main_url, headers=HEADERS)

    login = session.get(login_url, headers=HEADERS)
    soup = BeautifulSoup(login.text, 'lxml')
    token = soup.find('form').find('input')['value']

    result = session.post(login_url, headers=HEADERS,
                 data={'csrf_token': token, 'username': 'Johny', 'password':'123456123'}, allow_redirects=True)

    return result.text


print(get_login(MAIN_URL, LOGIN_URL))
