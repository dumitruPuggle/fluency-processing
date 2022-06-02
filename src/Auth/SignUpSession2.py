import os
from random import randrange
from flask_restful import Resource, request
import jwt
from lang.phone_verification_formatter import phoneVerificationFormatter
import cryptocode
from time import time
from src.Auth.Tools.send_verification_code import send_verification_code 
from firebase_admin import auth
import requests

from src.Auth.Decorators.use_temp_token import use_temp_token

from lang.translate import Translate

class SignUpSession2(Resource):
    # @use_temp_token
    def post(self):
        # get JSON body content from request
        json_data = request.get_json()

        # get the language from the request
        language = request.get_json()['lang']
        translate = Translate(language)

        phone_number = json_data['phoneNumber']
        lang = json_data['lang']

        try:
            auth.get_user_by_phone_number(phone_number)
        except auth.UserNotFoundError:
            pass
        else:
            return {'message': translate.t('phoneAlreadyLinked'), 'field': 'phoneNumber'}, 403

        # check if the phone number is valid
        url = f"https://api.apilayer.com/number_verification/validate?number={phone_number}"

        payload = {}
        headers= {
            "apikey": os.environ.get('NUMVERIFY_API_KEY')
        }

        # response = requests.request("GET", url, headers=headers, data = payload)

        # status_code = response.status_code
        # result = response.text
        # print(status_code, response)
        r = requests.get(url, headers=headers, data = payload)
        result = r.json()
        
        print(result)
        is_valid = r.status_code == 200 and result['valid']

        def return_invalid():
            return {'message': translate.t('invalidPhoneNumber'), 'field': 'phoneNumber'}, 403

        if is_valid:
            return return_invalid()
        if len(phone_number) < 7:
            return return_invalid()

        # try to decode the token from header
        bearer = request.headers.get('_temptoken')

        try:
            # to get get the previous information from the last session using the token
            session1_credentials = {
                "payload": {
                    **jwt.decode(bearer, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])['payload'],
                    "phoneNumber": phone_number
                }
            }
        except jwt.exceptions.InvalidSignatureError or jwt.exceptions.DecodeError:
            return {
                "message": "Invalid token"
            }, 403
        except jwt.exceptions.ExpiredSignatureError:
            return {
                "message": "Token expired"
            }, 403
        else:
            # send the message to the user
            random_code = randrange(100000, 999999)
            message = phoneVerificationFormatter(random_code, lang)

            send_verification_code(phone_number, message)
            
            # get .env variables
            jwt_key = os.environ.get("SMS_JWT_KEY")
            code_encryption_key = os.environ.get("SMS_CODE_ENCRYPTION_KEY")

            try:
                # to generate a code that only we can access and decrypt later
                print(random_code)
                encrypted_code = cryptocode.encrypt(str(random_code), code_encryption_key)
                # expire in 5 minutes
                expiration_time = time() + 300

                token = jwt.encode(
                    {
                        **session1_credentials,
                        "code": encrypted_code,
                        "exp": expiration_time
                    },
                    jwt_key,
                    algorithm='HS256'
                )
            except Exception:
                return {
                    "message": "Error generating new token",
                    "field": "token"
                }, 403

        return {"message": f"Success! An message code was sent to {phone_number}", "token": token}, 200
