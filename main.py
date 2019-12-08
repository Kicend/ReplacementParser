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

headers = {"user_agent": "macOS 10.15 Catalina"}
page = r.get("http://zastepstwa.staff.edu.pl/", headers=headers)
soup = BeautifulSoup(page.text, "lxml")
links = soup.find_all("tr")
os.makedirs("parser_files", exist_ok=True)
with open("parser_files/file.txt", "w") as f:
    for link in links:
        f.writelines(str(link))

file_converter("parser_files/file")  # Wczytanie zawartości pliku po parsowaniu, i zapisanie go do innego pliku po konwersji

