"""
1.  Задание на закрепление знаний по модулю CSV.
    Написать скрипт, осуществляющий выборку определённых данных из файлов info_1.txt, info_2.txt, info_3.txt и
    формирующий новый "отчётный" файл в формате CSV.
"""

import csv
import glob
import re


def get_data():
    headers = ('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')
    main_data = {k: [] for k in headers}

    for file in glob.iglob('tmp_folder/*.txt', recursive=True):
        with open(file, 'r', encoding='cp1251') as f:
            text = f.read()
            for header in headers:
                response = re.search(rf'{header}:\s+([^\n]+)', text)
                value = response.group(1)
                main_data[header].append(value)

    return main_data


def write_to_csv(main_data, path):
    with open(path, 'w') as f:
        fieldnames = main_data.keys()
        data = list(map(list, zip(*main_data.values())))

        my_list = []
        for values in data[:]:
            inner_dict = dict(zip(fieldnames, values))
            my_list.append(inner_dict)

        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()

        for row in my_list:
            writer.writerow(row)


write_to_csv(get_data(), 'tmp_folder/output.csv')
