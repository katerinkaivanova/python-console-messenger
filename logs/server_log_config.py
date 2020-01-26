import os
import sys
import logging
import logging.handlers

from configs.default import LOGGING_LEVEL
sys.path.append('../')

# формат сообщений
server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# создание обработчика, который выводит сообщения с уровнем ERROR в поток stderr
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(server_formatter)
stream_handler.setLevel(logging.ERROR)

# создание обработчика, который выводит сообщения в файл
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')
# циклическое переименование файлов через определённый период времени
file_handler = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
file_handler.setFormatter(server_formatter)

# создание регистратора (экзмепляр класса Logger)
server_logger = logging.getLogger('server')

# добавление обработчиков
server_logger.addHandler(stream_handler)
server_logger.addHandler(file_handler)

# уровень важности
server_logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    server_logger.critical('Критическая ошибка')
    server_logger.error('Ошибка')
    server_logger.debug('Отладочная информация')
    server_logger.info('Информационное сообщение')
