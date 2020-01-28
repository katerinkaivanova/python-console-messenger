import sys
import os
import unittest

from client import create_presence, parse_server_msg
from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, PRESENCE, ERROR

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestClass(unittest.TestCase):
    # тестирует функцию create_presence()
    # корректный запрос
    def test_presence(self):
        test = create_presence()
        test[TIME] = 1.1  # присваиваем значения для прохождения теста
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    # тестирует функцию parse_server_msg()
    # парсинг RESPONSE 200
    def test_200_ans(self):
        self.assertEqual(parse_server_msg({RESPONSE: 200}), '200 : OK')

    # парсинг RESPONSE 400
    def test_400_ans(self):
        self.assertEqual(parse_server_msg({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    # отсутствует RESPONSE в msg
    def test_no_response(self):
        self.assertRaises(ValueError, parse_server_msg, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
