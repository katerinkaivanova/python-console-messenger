import os
import sys
import logging
import logging.handlers

from configs.default import LOGGING_LEVEL
sys.path.append('../')

# формат сообщений
client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# создание обработчика, который выводит сообщения с уровнем ERROR в поток stderr
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(client_formatter)
stream_handler.setLevel(logging.ERROR)

# создание обработчика, который выводит сообщения в файл
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')
# циклическое переименование файлов через определённый период времени
file_handler = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
file_handler.setFormatter(client_formatter)

# создание регистратора (экзмепляр класса Logger)
client_logger = logging.getLogger('client')

# добавление обработчиков
client_logger.addHandler(stream_handler)
client_logger.addHandler(file_handler)

# уровень важности
client_logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    client_logger.critical('Критическая ошибка')
    client_logger.error('Ошибка')
    client_logger.debug('Отладочная информация')
    client_logger.info('Информационное сообщение')
