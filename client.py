import sys
import json
import time
import logging
import logs.client_log_config

from socket import *
from configs.default import *
from configs.utils import *


# Инициализация клиентского логера
client_logger = logging.getLogger('client')


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
    client_logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def parse_server_msg(message):
    """
    Разбор сообщения от сервера
    :param message: словарь сообщения
    :return: строка статуса
    """
    client_logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


if __name__ == '__main__':

    # Создается TCP-сокет клиента
    client_tcp = socket(AF_INET, SOCK_STREAM)

    # Получаем ip-адрес и порт из командной строки
    try:
        addr = sys.argv[1]
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            client_logger.critical(
                f'Попытка запуска клиента с неподходящим номером порта: {port}.'
                f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
            raise ValueError
    except IndexError:
        addr = DEFAULT_IP_ADDRESS
        port = DEFAULT_PORT
    except ValueError:
        print('Порт должен быть целым числом в диапазоне (1024; 65535)')
        sys.exit(0)

    client_logger.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {addr} , порт: {port}')

    # Соединяется с сервером
    client_tcp.connect((addr, port))
    # Формирует сообщение о присутствии
    presence = create_presence()
    # Отправляет сообщение серверу
    send_message(client_tcp, presence)

    try:
        # Получает и разбирает сообщение от сервера
        answer = parse_server_msg(receive_message(client_tcp))
        client_logger.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную Json строку.')
    except ConnectionRefusedError:
        client_logger.critical(f'Не удалось подключиться к серверу {addr}:{port}, '
                               f'конечный компьютер отверг запрос на подключение.')
