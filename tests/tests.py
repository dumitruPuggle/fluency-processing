import json

from dotenv import load_dotenv
import os
import unittest
import requests
import random_name_generator as rng
import jwt
from time import time
from random import randrange

load_dotenv()


class AuthTests(unittest.TestCase):
    url = f"http://{os.environ.get('HOST')}:{os.environ.get('PORT')}"
    first_session_token: str = ""
    second_session_token: str = ""

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
        session2_headers = {"_temptoken": self.first_session_token}

        # CHECK existing account
        body = {
            'phoneNumber': "+37360286928",
            'lang': 'ro'
        }
        existing_account_response = requests.post(session2_url, json=body, headers=session2_headers)
        self.assertEqual(existing_account_response.status_code, 403)

        # check incorrect phone number
        body = {
            'phoneNumber': "+3736941488777",
            'lang': 'ro'
        }
        incorrect_number_response = requests.post(session2_url, json=body, headers=session2_headers)
        self.assertEqual(incorrect_number_response.status_code, 403)

        # check incorrectly formatted code
        body = {
            'phoneNumber': "+5105005036941488777",
            'lang': 'ro'
        }
        invalid_formated_response = requests.post(session2_url, json=body, headers=session2_headers)
        self.assertEqual(invalid_formated_response.status_code, 403)

        # check no _temptoken parameter
        body = {
            'phoneNumber': "+37360286928",
            'lang': 'ro'
        }
        no_temptoken_response = requests.post(session2_url, json=body, headers={})
        self.assertEqual(no_temptoken_response.status_code, 403)

        # normal phone number
        body = {
            'phoneNumber': f"+3736028{randrange(4013, 9999)}",
            'lang': 'ro'
        }
        normal_phone_response = requests.post(session2_url, json=body, headers=session2_headers)
        AuthTests.second_session_token = json.loads(normal_phone_response.text).get('token')
        self.assertEqual(normal_phone_response.status_code, 200)

if __name__ == "__main__":
    unittest.main()