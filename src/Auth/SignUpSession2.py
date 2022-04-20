import os
from random import randrange
from flask_restful import Resource, request
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import jwt
from lang.phone_verification_formatter import phoneVerificationFormatter
import cryptocode
class SignUpSession2(Resource):
    def post(self):
        # get JSON body content from request
        json_data = request.get_json()

        session2_credentials = {
            "phoneNumber": json_data['phoneNumber'],
            "language": json_data['lang']
        }
        random_code = randrange(100000, 999999)
        message = phoneVerificationFormatter(random_code, session2_credentials['language'])

        # try to send the message
        try:
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=message,
                from_='+12673184182',
                to=session2_credentials['phoneNumber']
            )
        except TwilioRestException as e:
            print(e)
            return {
                "message": "Error sending message",
                "field": "phoneNumber"
            }, 403

        jwtKey = os.environ.get("SMS_JWT_KEY")
        codeEncryptionKey = os.environ.get("SMS_CODE_ENCRYPTION_KEY")
        encryptedCode = cryptocode.encrypt(str(random_code), codeEncryptionKey)

        token = jwt.encode({"code": encryptedCode}, jwtKey, algorithm="HS256")
        return {"message": "Success! SMS was sent successfully.", "token": token}, 200