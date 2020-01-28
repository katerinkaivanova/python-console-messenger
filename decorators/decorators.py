import sys
import logging
import logs.server_log_config
import logs.client_log_config


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


# Decorator Function
def my_logger(orig_func):

    def wrapper(*args, **kwargs):
        LOGGER.debug(f'@my_logger -> function {orig_func.__name__} ran with args: {args} and kwargs: {kwargs}. '
                     f'From module: {orig_func.__module__}')
        return orig_func(*args, **kwargs)

    return wrapper


# Decorator Class
class MyLogger(object):

    def __init__(self, orig_func):
        self.orig_func = orig_func

    def __call__(self, *args, **kwargs):
        LOGGER.debug(f'@MyLogger -> function {self.orig_func.__name__} ran with args: {args} and kwargs: {kwargs}. /'
                     f'From module: {self.orig_func.__module__}')
        return self.orig_func(*args, **kwargs)
