import requests as r
from bs4 import BeautifulSoup

headers = {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/74.0.3729.169 Safari/537.36"}

def get_class_list():
    class_list = []
    page = r.get("http://planlekcji.staff.edu.pl/lista.html", headers=headers)
    soup = BeautifulSoup(page.text.encode("latin1").decode("utf-8"), "lxml")
    links = soup.find_all("ul")
    with open("parser_files/class_file.txt", "w") as f:
        f.writelines(str(links[0]))
    with open("parser_files/class_file.txt", "r") as f:
        class_raw_data = f.readlines()
    for line in class_raw_data:
        try:
            classname_start = line.index(">", 4) + 1
            classname_end = line.index("<", 5)
            classname = line[classname_start:classname_end]
            if classname.count(" "):
                classname = classname[:classname.index(" ")]
            class_list.append(classname + "\n")
        except ValueError:
            pass
    with open("config/class_list.txt", "w") as f:
        f.writelines(class_list)

def get_teachers_list():
    teachers_list = []
    page = r.get("http://planlekcji.staff.edu.pl/lista.html", headers=headers)
    soup = BeautifulSoup(page.text.encode("latin1").decode("utf-8"), "lxml")
    links = soup.find_all("ul")
    with open("parser_files/teachers_file.txt", "w") as f:
        f.writelines(str(links[1]))
    with open("parser_files/teachers_file.txt", "r") as f:
        teachers_raw_data = f.readlines()
    for line in teachers_raw_data:
        try:
            teacher_start = line.index(">", 4) + 1
            teacher_end = line.index("<", 5)
            teacher = line[teacher_start:teacher_end]
            teacher = teacher[0:1] + ". " + teacher[2:-5]
            teachers_list.append(teacher + "\n")
        except ValueError:
            pass
    with open("config/teachers_list.txt", "w") as f:
        f.writelines(teachers_list)
