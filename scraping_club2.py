from scraping_club import scraping_data
import requests
from pathlib import Path
import xlsxwriter

def pics_downloader(url: str, folder_path: str) -> None:
    """This function downloads an image from given URL"""
    response = requests.get(url, stream=True)
    try:
        file = open(f'{folder_path}/{url.split("/")[-1]}', 'ab')
        for piece in response.iter_content(1024*1024):
            file.write(piece)
    except FileNotFoundError as ex:
        return f'Check the file path \n {ex}'
    finally:
        file.close()

def excel_writer(collection: callable) -> None:
    """This function writes an incoming 4-piece tuple to a new Excel file and saves image links to a folder"""
    excel_path = Path(r'C:\Users\aray1\OneDrive\Рабочий стол\scraping_club_parsed.xlsx')
    image_folder_path = Path(r'C:\Users\aray1\OneDrive\Рабочий стол\goods')

    xls_file = xlsxwriter.Workbook(excel_path)
    page = xls_file.add_worksheet('Одежда')

    row = 0

    page.set_column("A:A", 50)
    page.set_column("B:B", 20)
    page.set_column("C:C", 200)
    page.set_column("D:D", 80)

    for one in collection():
        page.write(row, 0, one[0])
        page.write(row, 1, one[1])
        page.write(row, 2, one[2])
        page.write(row, 3, one[3])
        pics_downloader(one[3], image_folder_path)
        row += 1

    xls_file.close()

excel_writer(scraping_data)