import requests as r
import os
from bs4 import BeautifulSoup
from data.latin1_to_utf import file_converter

class_list = ("1pla",
              "1plb",
              "1plc",
              "1pta",
              "1ptb",
              "1ptm",
              "1gta",
              "1gtb",
              "1gm1 (1gtm1)",
              "1gm2 (1gm2)",
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

if __name__ == "__main__":
    page = r.get("http://zastepstwa.staff.edu.pl/", headers=headers)
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all("tr")
    os.makedirs("parser_files", exist_ok=True)
    with open("parser_files/file.txt", "w") as f:
        for link in links:
            f.writelines(str(link))

    # Wczytanie zawartości pliku po parsowaniu, i zapisanie go do innego pliku po konwersji
    file_converter("parser_files/file")

# TODO: Zapisywanie plików klasa.json z informacjami o zastępstwie (w przypadku braku informacji usunięcie pliku)
# TODO: Serwer HTTPS (wyrobienie certyfikatu + integracja z aplikacją)
