import requests as r
import os
from bs4 import BeautifulSoup
from data.latin1_to_utf import file_converter

headers = {"user_agent": "macOS 10.15 Catalina"}
page = r.get("http://zastepstwa.staff.edu.pl/", headers=headers)
soup = BeautifulSoup(page.text, "lxml")
links = soup.find_all("tr")
os.makedirs("files", exist_ok=True)
with open("files/file.txt", "w") as f:
    for link in links:
        f.writelines(str(link))

file_converter("files/file")  # Wczytanie zawartości pliku po parsowaniu, i zapisanie go do innego pliku po konwersji

