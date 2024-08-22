import requests
import folium
from art import tprint
from fake_useragent import FakeUserAgent


ua = FakeUserAgent()
ip_url = "http://ip-api.com/json/"

def get_him_by_ip(ip: str):
    try:
        response = requests.get(url=f"{ip_url}/{ip}", headers={'User-Agent': ua.random})
        response.raise_for_status()
    except requests.exceptions.RequestException as ex:
        print(f"Got an error {ex} while requesting")
        quit()


    if response.status_code == 200:
        data = response.json()
        result = {}
        result['country'] = data.get('country', 'No country')
        result['city'] = data.get('city', 'No city')
        result['lat'] = data.get('lat', 'No lat')
        result['lon'] = data.get('lon', 'No lon')

        location = [data.get('lat'), data.get('lon')]
        on_map = folium.Map(location=location, zoom_start=12)
        folium.Marker(location=location, popup='Astana, Kazakhstan').add_to(on_map)
        on_map.save(f"{ip} - {data.get('city')}.html")
        
        return result

    return 'Something went wrong'


def main():
    ip = input("Please enter the target IP: ")
    for k, v in get_him_by_ip(ip=ip).items():
        print(f"{k} - {v}")

if __name__ == '__main__':
    tprint("CATCHA", font="block")
    main()
    tprint("Found you", "block")

