import sys
import json
import time

from socket import  *
from configs.default import *
from configs.utils import *


def create_presence(account_name='Guest'):
    """
    Формирование сообщения о присутствии
    :param account_name: строка псевдонима
    :return: словарь ответа о присутствии клиента
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def parse_answer(message):
    """
    Разбор сообщения от сервера
    :param message: словарь сообщения
    :return: строка статуса
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


if __name__ == '__main__':

    # Создается TCP-сокет клиента
    client = socket(AF_INET, SOCK_STREAM)

    # Получаем ip-адрес и порт из командной строки
    try:
        addr = sys.argv[1]
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        addr = DEFAULT_IP_ADDRESS
        port = DEFAULT_PORT
    except ValueError:
        print('Порт должен быть целым числом в диапазоне (1024; 65535)')
        sys.exit(0)

    # Соединяется с сервером
    client.connect((addr, port))
    # Формирует сообщение о присутствии
    presence = create_presence()
    # Отправляет сообщение серверу
    send_message(client, presence)

    try:
        # Получает и разбирает сообщение от сервера
        answer = parse_answer(get_message(client))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')
