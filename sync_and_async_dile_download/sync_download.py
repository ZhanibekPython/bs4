import requests
from tqdm import tqdm


def download_file(url: str, filename: str):
    """This func downloads a file from given url syncronously"""

    with open(filename, 'wb') as file:
        with requests.get(url=url, stream=True) as response:
            response.raise_for_status()

            file_weight = int(response.headers.get('content-length', 0))
            tqdm_params = {
                'desc': f'{filename} download in process',
                'total': file_weight,
                'miniters': 1,
                'unit': 'it'
            }

            with tqdm(**tqdm_params) as progres_bar:
                for part in response.iter_content(chunk_size=8192):
                    progres_bar.update(len(part))
                    file.write(part)

def main():
    download_file(url="http://ipv4.download.thinkbroadband.com/50MB.zip", filename="50MB.zip")


if __name__ == '__main__':
    main()