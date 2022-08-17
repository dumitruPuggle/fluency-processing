import unittest

from flask_restful import http_status_message


class FlaskTests(unittest.TestCase):

    def test_http_code(self):
        self.assertEqual(http_status_message(200), 'OK')
        self.assertEqual(http_status_message(404), 'Not Found')


if __name__ == "__main__":
    unittest.main()