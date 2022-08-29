import os

from dotenv import load_dotenv
import requests
import names
import json
import jwt
from time import time
from random import randrange

load_dotenv()

url = f'http://{os.environ.get("HOST")}:{os.environ.get("PORT")}'

def test_http_code():
    response = requests.get(url)
    assert response.status_code == 200

def test_4_sessions():
    # Session 1
    name = names.get_first_name()
    surname = names.get_last_name()
    session1_url = f'{url}/api/signup/1'

    body = {
        "firstName": name,
        "lastName": surname,
        "email": f'{names.get_full_name().lower().strip().replace(" ", "_")}@gmail.com'
    }
    response = requests.post(url=session1_url, json=body, headers={"lang": "ro"})
    token: str = json.loads(response.text).get('token')
    session_one_token = token

    assert session_one_token != None
    assert response.status_code == 200

    # Verify session one
    decoded = jwt.decode(session_one_token, options={"verify_signature": False})
    payload = decoded.get('payload')
    assert payload.get('firstName') != None
    assert payload.get('lastName') != None
    assert payload.get('email') != None
    assert decoded.get('exp') > time()

    # Verify session two
    session2_url = f'{url}/api/signup/2'
    session2_headers = {"_temptoken": session_one_token}

    # SESSION TWO: CHECK existing account
    body = {
        'phoneNumber': "+37360286928",
        'lang': 'ro'
    }
    existing_account_response = requests.post(session2_url, json=body, headers=session2_headers)
    assert existing_account_response.status_code == 403

    # SESSION TWO: check incorrect phone number
    body = {
        'phoneNumber': "+3736941488777",
        'lang': 'ro'
    }
    incorrect_number_response = requests.post(session2_url, json=body, headers=session2_headers)
    assert incorrect_number_response.status_code == 403

    # SESSION TWO: check incorrectly formatted code
    body = {
        'phoneNumber': "+5105005036941488777",
        'lang': 'ro'
    }
    invalid_formated_response = requests.post(session2_url, json=body, headers=session2_headers)
    assert invalid_formated_response.status_code == 403

    # SESSION TWO: check no _temptoken parameter
    body = {
        'phoneNumber': "+37369258122",
        'lang': 'ro'
    }
    no_temptoken_response = requests.post(session2_url, json=body, headers={})
    assert no_temptoken_response.status_code == 403

    # SESSION TWO: normal phone number
    normal_phone_response = requests.post(session2_url, json=body, headers=session2_headers)
    token: str = json.loads(normal_phone_response.text).get('token')
    session_two_token = token

    # Session three:
    session3_url = f'{url}/api/signup/3'
    session3_headers = {}
    body = {

    }
    response = requests.post(session3_url, json=body, headers=session3_headers)

    assert "Success" in json.loads(normal_phone_response.text).get('message')

    assert normal_phone_response.status_code == 200