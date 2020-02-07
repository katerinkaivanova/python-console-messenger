import sys
import json
import socket
import select
import argparse
import time
import logging
import logs.server_log_config

from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT
from configs.utils import send_message, receive_message
from decorators.decorators import MyLogger

# Инициализация серверного логера
server_logger = logging.getLogger('server')


@MyLogger
def parse_client_msg(message, messages_list, sock):
    """
    Обработчик сообщений клиентов
    :param message: словарь сообщения
    :param messages_list: список сообщений
    :param sock: клиентский сокет
    :return: словарь ответа
    """
    server_logger.debug(f'Разбор сообщения от клиента: {message}')
    print(f'Разбор сообщения от клиента: {message}')

    # возвращает сообщение о присутствии
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(sock, {
            RESPONSE: 200
        })
        return

    # формирует очередь сообщений
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and \
            USER in message and MESSAGE_TEXT in message:

        messages_list.append((message[USER][ACCOUNT_NAME], message[MESSAGE_TEXT]))

        return messages_list

    # возвращает сообщение об ошибке
    else:
        send_message(sock, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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
                    parse_client_msg(receive_message(r_sock), all_messages, r_sock)
                except Exception as ex:
                    server_logger.error(f'Клиент отключился от сервера. '
                                        f'Тип исключения: {type(ex).__name__}, аргументы: {ex.args}')
                    all_clients.remove(r_sock)

        # Обойдёт список клиентов, читающих из сокета
        # Эхо-ответ сервера клиентам, от которых были запросы
        if all_messages and w_clients:
            response_message = {
                ACTION: MESSAGE,
                SENDER: all_messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: all_messages[0][1]
            }

            del all_messages[0]

            for w_sock in w_clients:
                try:
                    server_logger.info(f'Сформирован ответ клиенту: {response_message}')
                    print(f'Сформирован ответ клиенту {response_message}')
                    send_message(w_sock, response_message)
                except Exception as ex:
                    server_logger.error(f'Клиент отключился от сервера. '
                                        f'Тип исключения: {type(ex).__name__}, аргументы: {ex.args}')
                    all_clients.remove(w_sock)
