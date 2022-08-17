import json

from dotenv import load_dotenv
import os
import unittest
import requests
import random_name_generator as rng

load_dotenv()


class AuthTests(unittest.TestCase):
    url = f"http://{os.environ.get('HOST')}:{os.environ.get('PORT')}"


    def test_http_code(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_session_one(self):
        name = rng.generate_one().split()[0]
        surname = rng.generate_one().split()[1]
        session1_url = f'{self.url}/api/signup/1'
        print(session1_url)
        body = {
            "firstName": name,
            "lastName": surname,
            "email": f'{rng.generate_one().lower().strip().replace(" ", "_")}@gmail.com'
        }
        response = requests.post(url=session1_url, json=body, headers={"lang": "ro"})
        print(response.text)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()