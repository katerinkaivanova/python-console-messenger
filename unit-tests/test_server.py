import sys
import os
import unittest

from server import parse_client_msg
from configs.default import ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, PRESENCE, ERROR

sys.path.append(os.path.join(os.getcwd(), '..'))


# тестирует функцию parse_client_msg()
class TestClient(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    corr_dict = {
        RESPONSE: 200
    }

    # отсутствует ACTION в presence msg
    def test_no_action(self):
        self.assertEqual(parse_client_msg({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    # неизвестный ACTION в presence msg
    def test_wrong_action(self):
        self.assertEqual(parse_client_msg({ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.err_dict)

    # отсутствует TIME в presence msg
    def test_no_time(self):
        self.assertEqual(parse_client_msg({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    # отсутствует USER в presence msg
    def test_no_user(self):
        self.assertEqual(parse_client_msg({ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    # корректный запрос
    def test_ok_check(self):
        self.assertEqual(parse_client_msg({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.corr_dict)


if __name__ == '__main__':
    unittest.main()
