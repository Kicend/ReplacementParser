characters_dict = {
    "ą": "±",
    "ę": "ê",
    "ź": "¼",
    "ś": "¶",
    "ł": "³",
    "ń": "ñ"
}


def repair_line(line):
    keys = list(characters_dict.keys())
    values = list(characters_dict.values())
    for number in range(0, 6):
        new_line = line.replace(values[number], keys[number])
        if new_line != line:
            line = repair_line(new_line)
    return line


def file_converter(path_to_file):
    new_file = []
    with open("{}.txt".format(path_to_file), "r") as f:
        file = f.readlines()
        for line in file:
            new_file.append(repair_line(line))

    with open("{}_utf-8.txt".format(path_to_file), "a") as f:
        f.writelines(new_file)
