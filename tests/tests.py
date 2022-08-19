import json

from dotenv import load_dotenv
import os
import unittest
import requests
import random_name_generator as rng
import jwt
from time import time

load_dotenv()


class AuthTests(unittest.TestCase):
    url = f"http://{os.environ.get('HOST')}:{os.environ.get('PORT')}"
    first_session_token: str = ""

    def test_http_code(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_session_one(self):
        name = rng.generate_one().split()[0]
        surname = rng.generate_one().split()[1]
        session1_url = f'{self.url}/api/signup/1'
        
        body = {
            "firstName": name,
            "lastName": surname,
            "email": f'{rng.generate_one().lower().strip().replace(" ", "_")}@gmail.com'
        }
        response = requests.post(url=session1_url, json=body, headers={"lang": "ro"})
        token: str = json.loads(response.text).get('token')
        AuthTests.first_session_token = token
        self.assertEqual(response.status_code, 200)

    def test_session_one_token(self):
        decoded = jwt.decode(self.first_session_token, options={"verify_signature": False})
        payload = decoded.get('payload')
        self.assertIsNotNone(payload.get('firstName'))
        self.assertIsNotNone(payload.get('lastName'))
        self.assertIsNotNone(payload.get('email'))
        self.assertGreater(decoded.get('exp'), time())

    def test_session_two(self):
        session2_url = f'{self.url}/api/signup/2'
        body = {
            'phoneNumber': "+37360286928",
            'lang': 'ro'
        }
        def response(use_header=True):
            if use_header:
                headers = {"_temptoken": self.first_session_token}
            else:
                headers = {}
            return requests.post(session2_url, json=body, headers=headers)

        # CHECK existing account
        self.assertEqual(response().status_code, 403)
        # check incorrect phone number
        body = {
            'phoneNumber': "+3736941488777",
            'lang': 'ro'
        }
        self.assertEqual(response().status_code, 403)
        # check no _temptoken parameter
        body = {
            'phoneNumber': "+37360286928",
            'lang': 'ro'
        }
        self.assertEqual(response(use_header=False).status_code, 403)


if __name__ == "__main__":
    unittest.main()