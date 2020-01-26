import sys
import json
import logging
import logs.server_log_config

from socket import *
from configs.default import *
from configs.utils import *


# Инициализация серверного логера
server_logger = logging.getLogger('server')


def parse_client_msg(presence):
    """
    Обработчик сообщений клиентов
    :param presence: словарь сообщения
    :return: словарь ответа
    """
    server_logger.debug(f'Разбор сообщения от клиента : {presence}')
    if ACTION in presence and presence[ACTION] == PRESENCE and TIME in presence and USER in presence and \
            presence[USER][ACCOUNT_NAME] == 'Guest':
        return {
            RESPONSE: 200
        }
    else:
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


if __name__ == '__main__':

    # Создает TCP-сокет сервера
    server_tcp = socket(AF_INET, SOCK_STREAM)

    # Извлекает ip-адрес из командной строки
    try:
        listen_addr = sys.argv[1]
    except IndexError:
        listen_addr = ''

    # Извлекает порт из командной строки
    try:
        listen_port = int(sys.argv[2])
        if listen_port < 1024 or listen_port > 65535:
            server_logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                   f'{listen_port}. Допустимы адреса с 1024 до 65535.')
            raise ValueError
    except IndexError:
        listen_port = DEFAULT_PORT
    except ValueError:
        print('Порт должен быть целым числом в диапазоне (1024; 65535).')
        sys.exit(0)

    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_addr}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Связывает сокет с ip-адресом и портом сервера
    server_tcp.bind((listen_addr, listen_port))

    # Запускает режим прослушивания
    server_tcp.listen(MAX_CONNECTIONS)

    while True:
        # Принимает запрос на соединение
        # Возвращает кортеж (новый сокет, адрес клиента)
        client, client_addr = server_tcp.accept()
        server_logger.info(f'Установлено соедение с клиентов {client_addr}')

        try:
            # Принимает сообщение от клиента
            message_from_client = receive_message(client)
            server_logger.debug(f'Получено сообщение {message_from_client}')
            print(message_from_client)

            # Формирует ответ клиенту
            response = parse_client_msg(message_from_client)
            server_logger.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)

            server_logger.debug(f'Соединение с клиентом {client_addr} закрывается.')
            client.close()
        except json.JSONDecodeError:
            server_logger.error(f'Не удалось декодировать json-строку, полученную от '
                                f'клиента {client_addr}. Соединение закрывается.')
            client.close()
