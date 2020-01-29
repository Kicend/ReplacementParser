from os import listdir
from time import strftime
from shutil import rmtree

def delete_unused_dirs():
    directory_list = listdir("class_files")
    today = strftime("%d.%m.%Y")
    start_index = directory_list.index(today) + 1
    while start_index != len(directory_list):
        rmtree("class_files/{}".format(directory_list[start_index]))
        start_index += 1
