import requests as r
import os
from bs4 import BeautifulSoup
from data.latin1_to_utf8 import file_converter

class_list = ("1pla",
              "1plb",
              "1plc",
              "1pta",
              "1ptb",
              "1ptm",
              "1gta",
              "1gtb",
              "1gm1",
              "1gm2",
              "1gla",
              "1glb",
              "2la",
              "2lb",
              "2ta",
              "2tb",
              "2tc",
              "2tm1",
              "2tm2",
              "3la",
              "3lb",
              "3ta",
              "3tb",
              "3tc",
              "3tm1",
              "3tm2",
              "4ta",
              "4tb",
              "4tc",
              "4tm1",
              "4tm2",
              "4tm3")

headers = {"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) "
                         "Version/9.0.2 Safari/601.3.9"}

class Sorter:
    def __init__(self, path_to_file: str):
        self.path = path_to_file

    def file_filter(self):
        with open(self.path, "r") as utf8:
            file_list = utf8.readlines()
        while True:
            for element in file_list:
                if element == "\xa0\n":
                    del file_list[file_list.index("\xa0\n")]
                elif element == "\n":
                    del file_list[file_list.index("\n")]
            try:
                file_list.index("\n")
            except ValueError:
                try:
                    file_list.index("\xa0\n")
                except ValueError:
                    break
        with open(self.path, "w") as utf8:
            for element in file_list:
                utf8.writelines(element)

if __name__ == "__main__":
    page = r.get("http://zastepstwa.staff.edu.pl/", headers=headers)
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all("tr")
    os.makedirs("parser_files", exist_ok=True)
    sorter = Sorter("parser_files/file_utf-8.txt")
    with open("parser_files/file.txt", "w") as f:
        for link in links:
            f.writelines(str(link))
    file_converter("parser_files/file")
    sorter.file_filter()

# TODO: Zapisywanie plików klasa.json z informacjami o zastępstwie (w przypadku braku informacji usunięcie pliku)
# TODO: Serwer HTTPS (wyrobienie certyfikatu + integracja z aplikacją)
