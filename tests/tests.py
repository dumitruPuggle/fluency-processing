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

unittest.TestLoader.sortTestMethodsUsing = None


class AuthTests(unittest.TestCase):
    url = f"http://{os.environ.get('HOST')}:{os.environ.get('PORT')}"

    def test_http_code(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_session_one(self):
        name = rng.generate_one().split()[0]
        surname = rng.generate_one().split()[1]
        session1_url = f'{self.url}/api/signup/1'

        print('1', time())

        body = {
            "firstName": name,
            "lastName": surname,
            "email": f'{rng.generate_one().lower().strip().replace(" ", "_")}@gmail.com'
        }
        response = requests.post(url=session1_url, json=body, headers={"lang": "ro"})
        token: str = json.loads(response.text).get('token')
        with open('debug_auth_test.json', 'w') as f:
            f.write(json.dumps({'session_one': token}))
        self.assertEqual(response.status_code, 200)

    def test_session_one_token(self):
        with open('debug_auth_test.json', 'r') as f:
            first_session_token: str = json.loads(f.read()).get('session_one')

        decoded = jwt.decode(first_session_token, options={"verify_signature": False})
        payload = decoded.get('payload')
        self.assertIsNotNone(payload.get('firstName'))
        self.assertIsNotNone(payload.get('lastName'))
        self.assertIsNotNone(payload.get('email'))
        self.assertGreater(decoded.get('exp'), time())

    def test_session_two(self):
        print('2', time())
        with open('debug_auth_test.json', 'r') as f:
            first_session_token = json.loads(f.read()).get('session_one')

        session2_url = f'{self.url}/api/signup/2'
        session2_headers = {"_temptoken": first_session_token}

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
        token: str = json.loads(normal_phone_response.text).get('token')
        with open('debug_auth_test.json', 'r') as f:
            all_dict = json.loads(f.read())
            f.close()
        with open('debug_auth_test.json', 'w') as f:
            dict_to_write = {
                **all_dict,
                "second_session": token
            }
            f.write(json.dumps(dict_to_write))
            print(dict_to_write)
            f.flush()
        self.assertEqual(normal_phone_response.status_code, 200)

    def test_session_three(self):
        print('3', time())
        session3_url = f'{self.url}/api/signup/3'
        with open('debug_auth_test.json', 'r') as f:
            print(f.read())
            # second_session = json.loads(f.read()).get('second_session')
            second_session = ""

        session3_headers = {
            '_temptoken': second_session,
            'lang': 'ro'
        }

        body = {
            'code': randrange(100000, 999999)
        }

        # check no _temptoken parameter
        no_temptoken_response = requests.post(session3_url, json=body, headers={})
        self.assertEqual(no_temptoken_response.status_code, 403)

        # check empty _temptoken
        empty_token_response = requests.post(session3_url, json=body, headers={
            '_temptoken': "",
            'lang': 'ro'
        })
        print(second_session)
        self.assertEqual(empty_token_response.status_code, 403)




if __name__ == "__main__":
    unittest.main()