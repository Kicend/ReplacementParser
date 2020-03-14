import json
from os import listdir

def json_final_shape():
    with open("config/teachers_list.txt", "r") as f:
        teachers_list = f.readlines()
    dirs = listdir("class_files")
    for dir in dirs:
        files = listdir("class_files/{}".format(dir))
        for file in files:
            with open("class_files/{}/{}".format(dir, file), "r", encoding="utf8") as f:
                dictionary = dict(json.load(f))
                replacement_list_final = []
                for key in dictionary.keys():
                    if key.count("_"):
                        group = key[2:]
                        replacement_subdict = {"Lesson": key[0], "Group": group}
                    else:
                        replacement_subdict = {"Lesson": key}
                    replacement_content = str(dictionary[key])
                    if replacement_content.count("\n") == 1:
                        replacement_subdict["Description"] = dictionary[key][:-1]
                        replacement_list_final.append(replacement_subdict)
                    elif replacement_content.count("\n") == 2:
                        new_line_char_index = replacement_content.index("\n")
                        description = replacement_content[new_line_char_index+1:-1]
                        if description + "\n" in teachers_list:
                            replacement_subdict["Teacher"] = description
                        else:
                            replacement_subdict["Description"] = description
                        replacement_list_final.append(replacement_subdict)
                    else:
                        new_line_char_index = replacement_content.index("\n")
                        description = replacement_content[new_line_char_index+1:-1]
                        new_line_char_index = replacement_content.index("\n", new_line_char_index+1)
                        teacher = replacement_content[new_line_char_index+1:-1]
                        replacement_subdict["Description"] = description
                        replacement_subdict["Teacher"] = teacher
                        replacement_list_final.append(replacement_subdict)
                with open("class_files/{}/{}".format(dir, file), "w", encoding="utf8") as fw:
                    json.dump(replacement_list_final, fw, indent=4, ensure_ascii=False)
