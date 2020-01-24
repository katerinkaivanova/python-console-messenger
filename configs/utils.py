import json

from configs.default import *


def receive_message(sock):
    """
    Получение сообщения
    :param sock: сокет
    :return: словарь ответа
    """

    # Получает байты
    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        # Декодирует байтстроку в строку
        json_response = encoded_response.decode(ENCODING)
        # Десериализует строку, содержащую документ JSON, в объект Python
        response = json.loads(json_response)
        if isinstance(response, dict):
            # Возвращает словарь
            return response
        else:
            raise ValueError
    else:
        raise ValueError


def send_message(sock, message):
    """
    Отправка сообщения
    :param sock: сокет
    :param message: словарь сообщения
    :return: None
    """

    # Сериализует message в JSON-подобный формат
    js_message = json.dumps(message)
    # Кодирует строку в байты / байтстроку
    encoded_message = js_message.encode(ENCODING)
    # Отправляет сообщение
    sock.send(encoded_message)
