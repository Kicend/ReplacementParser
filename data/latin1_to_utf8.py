# Słownik tylko do reprezentacji "graficznej" liter UTF-8 do latin1
characters_dict = {
    "ą": "±",
    "ę": "ê",
    "ź": "¼",
    "ś": "¶",
    "ł": ("³", "£"),
    "ń": "ñ",
    "ż": "¿"
}

unused_words = ("<tr>",
                "</>",
                "tr",
                "td",
                "nobr",
                "lekcja",
                "opis",
                "zastępca",
                "uwagi",
                "class")

def repair_line(line):
    utf8 = ("ą", "ę", "ź", "ś", "ł", "ł", "ń", "ż")
    latin1 = ("±", "ê", "¼", "¶", "³", "£", "ñ", "¿")
    for number in range(0, 7):
        new_line = line.replace(latin1[number], utf8[number])
        if new_line != line:
            line = repair_line(new_line)
    return line

def file_converter(path_to_file):
    new_file = []
    with open("{}.txt".format(path_to_file), "r") as f:
        file = f.readlines()
        for line in file:
            new_file.append(repair_line(line))

    with open("{}_utf-8.txt".format(path_to_file), "w") as f:
        for line in new_file:
            for number, word in enumerate(unused_words):
                if line.count(word) and not line.count("colspan"):
                    break
                else:
                    if number == 9:
                        f.writelines(line)
