"""
2. Задание на закрепление знаний по модулю json.
   Есть файл orders в формате JSON с информацией о заказах.
   Написать скрипт, автоматизирующий его заполнение данными.
"""
import json


def write_order_to_json(order_params, path):
    item, quantity, price, buyer, date = \
        order_params[0], order_params[1], order_params[2], order_params[3], order_params[4]

    data = dict()
    data['orders'] = []
    data['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })

    with open(path, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)


write_order_to_json(["printer", "1", "6700", "Ivanov I. I.", "24.09.2017"], 'tmp_folder/orders.json')
