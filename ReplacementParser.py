import requests as r
import os
import json
from bs4 import BeautifulSoup
from data.latin1_to_utf8 import file_converter
from data.cleanup import delete_unused_dirs

cache = {}

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
        self.mode = 0
        self.skip = False
        self.cache = []
        self.class_cache = []

    def main(self):
        self.file_filter()
        self.prepare_file()
        self.class_files()

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

    def prepare_file(self):
        with open(self.path, "r") as file:
            file_list = file.readlines()
            for number, element in enumerate(file_list):
                if self.skip:
                    self.skip = False
                    continue
                if len(element) == 2:
                    file_list.insert(number, "*")
                    self.skip = True
        with open(self.path, "w") as file:
            for element in file_list:
                file.writelines(element)
        if file_list[1].count("-"):
            self.mode = 1
        self.cache = file_list.copy()

    def class_files(self):
        counter = 0
        if self.mode == 0:
            date_line = self.cache[1]
            date = ""
            i = 0
            for char in date_line:
                for number in range(0, 10):
                    if char == str(number):
                        date = date + char
                        counter += 1
                        if counter == 2 and i != 2:
                            date = date + "."
                            counter = 0
                            i += 1
            cache["date"] = date
            cache["old_date"] = 1
            cache['new_date'] = 1
            try:
                os.mkdir("class_files/{}".format(date))
            except FileExistsError:
                pass

        with open("config/class_list.txt", "r") as class_f:
            self.class_cache = class_f.readlines()
        for class_name in self.class_cache:
            class_replacement = {}
            for i, element in enumerate(self.cache):
                if element.count("/") == 1 and self.mode == 1:
                    date = ""
                    if self.mode == 1:
                        date_line = self.cache[i]
                        dot = 0
                        for char in date_line:
                            for date_number in range(0, 10):
                                if char == str(date_number):
                                    date = date + char
                                    counter += 1
                                    if counter == 2 and dot != 2:
                                        date = date + "."
                                        counter = 0
                                        dot += 1
                        counter = 0
                        if len(cache) == 0:
                            cache["old_date"] = date
                        else:
                            if date != cache["old_date"]:
                                cache["new_date"] = date
                else:
                    if element.startswith("*"):
                        info_index_start = i + 1
                        lesson_number = self.cache[info_index_start]
                        lesson_number = lesson_number[0:-1]
                        info_index_end = 0
                        cycle = info_index_start + 1
                        while True:
                            try:
                                if self.cache[cycle].startswith("*"):
                                    info_index_end = cycle
                                    break
                                elif self.cache[cycle].startswith("<"):
                                    info_index_end = cycle
                                    break
                                cycle += 1
                            except IndexError:
                                break
                        cycle = info_index_start + 1
                        replacement_content = ""
                        alt_class_name = class_name[0] + " " + class_name[1:-1]
                        while cycle != info_index_end:
                            try:
                                content = self.cache[cycle]
                                replacement_content = replacement_content + content
                                cycle += 1
                            except IndexError:
                                content = self.cache[cycle-1]
                                replacement_content = replacement_content + content
                                break
                        if replacement_content.count(class_name[:-1]) or replacement_content.count(alt_class_name):
                            if replacement_content.count("("):
                                group_number = replacement_content[replacement_content.index("(") + 1]
                                lesson_number = lesson_number + "_" + group_number
                            dash_index = replacement_content.index("-")
                            replacement_content = replacement_content[dash_index+2:]
                            class_replacement[lesson_number] = replacement_content
                            if cache["new_date"] != cache["old_date"]:
                                try:
                                    if cache["old_date"] not in os.listdir("class_files"):
                                        os.mkdir("class_files/{}".format(cache["old_date"]))
                                except FileExistsError:
                                    pass
                                with open("class_files/{}/{}.json".format(cache["old_date"], class_name[:-1]), "w",
                                          encoding="utf8") \
                                        as class_file:
                                    json.dump(class_replacement, class_file, indent=4, ensure_ascii=False)
                                cache["old_date"] = cache["new_date"]
                            else:
                                if self.mode == 0:
                                    with open("class_files/{}/{}.json".format(cache["date"], class_name[:-1]), "w",
                                              encoding="utf8") \
                                            as class_file:
                                        json.dump(class_replacement, class_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    delete_unused_dirs()
    try:
        with open("config/class_list.txt", "r") as f_class:
            class_list = f_class.readlines()
    except FileNotFoundError:
        with open("config/class_list.txt", "a"):
            pass
    page = r.get("http://zastepstwa.staff.edu.pl/", headers=headers)
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all("tr")
    os.makedirs("parser_files", exist_ok=True)
    sorter = Sorter("parser_files/file_utf-8.txt")
    with open("parser_files/file.txt", "w") as f:
        for link in links:
            f.writelines(str(link))
    file_converter("parser_files/file")
    sorter.main()
