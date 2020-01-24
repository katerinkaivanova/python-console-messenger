import sys
import json

from socket import *
from configs.default import *
from configs.utils import *


def parse_client_msg(presence):
    """
    Обработчик сообщений клиентов
    :param presence: словарь сообщения
    :return: словарь ответа
    """
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
    server = socket(AF_INET, SOCK_STREAM)

    # Извлекает ip-адрес из командной строки
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''

    # Извлекает порт из командной строки
    try:
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        port = DEFAULT_PORT
    except ValueError:
        print('Порт должен быть целым числом в диапазоне (1024; 65535).')
        sys.exit(0)

    # Связывает сокет с ip-адресом и портом сервера
    server.bind((addr, port))

    # Запускает режим прослушивания
    server.listen(MAX_CONNECTIONS)

    while True:
        # Принимает запрос на соединение
        # Возвращает кортеж (новый сокет, адрес клиента)
        client, addr = server.accept()

        try:
            # Принимает сообщение от клиента
            message_from_client = receive_message(client)
            print(message_from_client)

            # Формирует ответ клиенту
            response = parse_client_msg(message_from_client)
            send_message(client, response)

            client.close()

        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()
