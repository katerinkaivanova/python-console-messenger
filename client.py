import sys
import json
import time
import socket
import argparse
import logging
import logs.client_log_config

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, RESPONSE, PRESENCE, ERROR, \
                            DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT
from configs.utils import send_message, receive_message
from decorators.decorators import my_logger


# Инициализация клиентского логера
client_logger = logging.getLogger('client')


@my_logger
def create_presence_msg(account_name='Guest'):
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


@my_logger
def create_client_msg(sock, account_name='Guest'):
    """
    Формирование сообщения клиента
    :param sock: клиентский сокет
    :param account_name: строка псевдонима
    :return message_dict: словарь сообщения клиента
    """
    message_str = input('Введите сообщение для отправки или \'stop\' для завершения работы: ')

    if message_str == 'stop':
        client_logger.info('Завершение работы по команде пользователя')
        print('*** Завершение работы ***')
        sock.close()
        sys.exit(0)

    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        },
        MESSAGE_TEXT: message_str
    }

    client_logger.debug(f'Сформировано сообщение: {message_dict}')

    return message_dict


@my_logger
def parse_server_msg(message):
    """
    Приём сообщения с сервера
    :param message: словарь сообщения
    """

    # приветственное сообщение
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            client_logger.debug(f'Получено приветственное сообщение от сервера: {message[RESPONSE]} OK')
            return f'{message[RESPONSE]} OK'
        elif message[RESPONSE] == 400:
            client_logger.debug(f'Получено сообщение от сервера: {message[RESPONSE]} {message[ERROR]}')
            return f'{message[RESPONSE]} {message[ERROR]}'

    # сообщение с сервера от другого клиента
    elif ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        client_logger.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
        print(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')

    # ошибка
    else:
        client_logger.error(f'Получено некорректное сообщение с сервера: {message[MESSAGE_TEXT]}')


@my_logger
def parse_cmd_arguments():
    """
    Парсер аргументов командной строки
    :return: ip-адрес и порт сервера, режим клиента
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')

    namespace = parser.parse_args(sys.argv[1:])
    addr = namespace.a
    port = namespace.p
    mode = namespace.mode

    # проверим подходящий номер порта
    if port < 1024 or port > 65535:
        client_logger.critical(f'Попытка запуска клиента с неподходящим номером порта: {server_port} '
                               f'Допустимы адреса с 1024 до 65535. Клиент завершается')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if mode not in ('listen', 'send'):
        client_logger.critical(f'Указан недопустимый режим работы {mode}, '
                               f'допустимые режимы: listen, send')
        sys.exit(1)

    return addr, port, mode


if __name__ == '__main__':

    # Получает ip-адрес, порт сервера, режим клиента из командной строки
    server_addr, server_port, client_mode = parse_cmd_arguments()

    client_logger.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_addr}, порт: {server_port}')
    print(f'Запущен клиент с парамертами: '
          f'адрес сервера: {server_addr}, порт: {server_port}')

    # Начало работы, приветственное сообщение
    try:
        # Создается TCP-сокет клиента
        client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Соединяется с сервером
        client_tcp.connect((server_addr, server_port))

        # Формирует сообщение о присутствии
        presence_msg = create_presence_msg()

        # Отправляет сообщение о присутствии серверу
        send_message(client_tcp, presence_msg)

        # Получает и разбирает сообщение от сервера
        server_answer = parse_server_msg(receive_message(client_tcp))

        client_logger.info(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
        print(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')

    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную json-строку')
        print('Не удалось декодировать полученную json-строку')
        sys.exit(1)

    except ConnectionRefusedError:
        client_logger.critical(f'Не удалось подключиться к серверу {server_addr}:{server_port}, '
                               f'запрос на подключение отклонён')
        print(f'Не удалось подключиться к серверу {server_addr}:{server_port}, '
              f'запрос на подключение отклонён')

    # Обмен сообщениями
    else:
        if client_mode == 'send':
            print('*** Отправка сообщений ***')
        else:
            print('*** Приём сообщений ***')

        while True:
            # Отправляет сообщения
            if client_mode == 'send':
                try:
                    send_message(client_tcp, create_client_msg(client_tcp))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с сервером {server_addr} было потеряно')
                    sys.exit(1)

            # Принимает сообщения
            if client_mode == 'listen':
                try:
                    parse_server_msg(receive_message(client_tcp))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с сервером {server_addr} было потеряно')
                    sys.exit(1)
