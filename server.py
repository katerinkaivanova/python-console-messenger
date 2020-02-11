import sys
import json
import socket
import select
import argparse
import time
import logging
import logs.server_log_config

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, EXIT, RESPONSE_200, RESPONSE_400
from configs.utils import send_message, receive_message
from decorators.decorators import MyLogger

# Инициализация серверного логера
server_logger = logging.getLogger('server')


@MyLogger
def parse_client_msg(message, messages_list, sock, clients_list, names):
    """
    Обработчик сообщений клиентов
    :param message: словарь сообщения
    :param messages_list: список сообщений
    :param sock: клиентский сокет
    :param clients_list: список клиентских сокетов
    :param names: список зарегистрированных клиентов
    :return: словарь ответа
    """
    server_logger.debug(f'Разбор сообщения от клиента: {message}')
    print(f'Разбор сообщения от клиента: {message}')

    # возвращает сообщение о присутствии
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message:

        # авторизация
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = sock
            send_message(sock, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(sock, response)
            clients_list.remove(sock)
            sock.close()
        return

    # формирует очередь сообщений
    elif ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and DESTINATION in message and \
            MESSAGE_TEXT in message and TIME in message:
        messages_list.append(message)
        return

    # выход клиента
    elif ACTION in message and message[ACTION] == EXIT and \
            ACCOUNT_NAME in message:
        clients_list.remove(names[message[USER][ACCOUNT_NAME]])
        names[message[USER][ACCOUNT_NAME]].close()
        del names[message[USER][ACCOUNT_NAME]]
        return

    # возвращает сообщение об ошибке
    else:
        response = RESPONSE_400
        response[ERROR] = 'Некорректный запрос.'
        send_message(sock, response)
        return


@MyLogger
def route_client_msg(message, names, clients):
    """
    Адресная отправка сообщений.
    :param message: словарь сообщения
    :param names: список зарегистрированных клиентов
    :param clients: список слушающих клиентских сокетов
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in clients:
        send_message(names[message[DESTINATION]], message)
        server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in clients:
        raise ConnectionError
    else:
        server_logger.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@MyLogger
def parse_cmd_arguments():
    """
    Парсер аргументов командной строки
    :return: ip-адрес и порт сервера
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')

    namespace = parser.parse_args(sys.argv[1:])
    addr = namespace.a
    port = namespace.p

    # Валидация номера порта
    if port < 1024 or port > 65535:
        server_logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return addr, port


if __name__ == '__main__':

    # Извлекает ip-адрес и порт из командной строки
    listen_addr, listen_port = parse_cmd_arguments()

    # Создает TCP-сокет сервера
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Связывает сокет с ip-адресом и портом сервера
    server_tcp.bind((listen_addr, listen_port))

    # Таймаут для операций с сокетом
    server_tcp.settimeout(0.5)

    # Запускает режим прослушивания
    server_tcp.listen(MAX_CONNECTIONS)

    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_addr}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    print(f'Запущен сервер, порт для подключений: {listen_port}, '
          f'адрес с которого принимаются подключения: {listen_addr}.')

    # Список клиентов и очередь сообщений
    all_clients = []
    all_messages = []

    # Словарь зарегистрированных клиентов: ключ - имя пользователя, значение - сокет
    all_names = dict()

    while True:
        # Принимает запрос на соединение
        # Возвращает кортеж (новый TCP-сокет клиента, адрес клиента)
        try:
            client_tcp, client_addr = server_tcp.accept()
        except OSError:
            pass
        else:
            server_logger.info(f'Установлено соедение с клиентом {client_addr}')
            print(f'Установлено соедение с клиентом {client_addr}')
            all_clients.append(client_tcp)

        r_clients = []
        w_clients = []
        errs = []

        # Запрашивает информацию о готовности к вводу, выводу и о наличии исключений для группы дескрипторов сокетов
        try:
            if all_clients:
                r_clients, w_clients, errs = select.select(all_clients, all_clients, [], 0)
        except OSError:
            pass

        # Чтение запросов из списка клиентов
        if r_clients:
            for r_sock in r_clients:
                try:
                    parse_client_msg(receive_message(r_sock), all_messages, r_sock, all_clients, all_names)
                except Exception as ex:
                    server_logger.error(f'Клиент отключился от сервера. '
                                        f'Тип исключения: {type(ex).__name__}, аргументы: {ex.args}')
                    all_clients.remove(r_sock)

        # Роутинг сообщений адресатам
        for msg in all_messages:
            try:
                route_client_msg(msg, all_names, w_clients)
            except Exception:
                server_logger.info(f'Связь с клиентом {msg[DESTINATION]} была потеряна')
                all_clients.remove(all_names[msg[DESTINATION]])
                del all_names[msg[DESTINATION]]
        all_messages.clear()
