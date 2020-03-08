from os import listdir
from time import strftime
from shutil import rmtree

def delete_unused_dirs():
    directory_list = listdir("class_files")
    today = strftime("%d.%m.%Y")
    today_day, today_month, today_year = today[0:2], today[3:5], today[6:10]
    for date in directory_list:
        date_day, date_month, date_year = date[0:2], date[3:5], date[6:10]
        if today_day > date_day or today_month > date_month or today_year > date_year:
            directory_list.insert(directory_list.index(date), today)
            break
    try:
        start_index = directory_list.index(today) + 1
        while start_index != len(directory_list):
            rmtree("class_files/{}".format(directory_list[start_index]))
            start_index += 1
    except ValueError:
        pass
