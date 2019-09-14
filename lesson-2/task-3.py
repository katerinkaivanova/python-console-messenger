"""
3. Задание на закрепление знаний по модулю YAML. Написать скрипт, автоматизирующий сохранение  данных в файле
   YAML-формата.
"""

import yaml


def write_to_yaml(items, items_quantity, items_price, path):
    items_dict = dict(zip(items, items_price))
    data_to_yaml = {
        'items': items,
        'items_quantity': items_quantity,
        'items_price': items_dict
    }

    with open(path, 'w') as f:
        yaml.dump(data_to_yaml, f, default_flow_style=False, allow_unicode=True)


items = ['computer', 'printer', 'keyboard', 'mouse']
items_quantity = 4
items_price = ['200€-1000€', '100€-300€', '5€-50€', '4€-7€']

write_to_yaml(items, items_quantity, items_price, 'tmp_folder/file.yaml')

with open('tmp_folder/file.yaml') as f:
    print(f.read())
