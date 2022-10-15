import os
from src.auth.auth_instance import AuthInstance
from random import randrange
import jwt  
from lang.phone_verification_formatter import phoneVerificationFormatter
from src.auth.encryption.encrypt import Encrypto
from time import time
from src.auth.tools.send_verification_code import SendVerificationSMSTwillo, SendVerificationSMSNexmo
from firebase_admin import auth
    
from lang.translate import Translate
    
    
class SignUpSession2(AuthInstance):

    schema = {
        'lang': 'String',
        'phoneNumber': "String"
    }

    def __init__(self):
        self.json_data = self.get_req_body
        self.lang = self.json_data.get('lang')
        self.translate = Translate(self.lang)

    def return_invalid_phone_number(self):
        return {'message': self.translate.t('invalidPhoneNumber'), 'field': 'phoneNumber'}, 403

    def search_for_phone_number(self, phone_number):
        try:
            auth.get_user_by_phone_number(phone_number)
        except auth.UserNotFoundError:
            return False
        else:
            return True

    def validate_phone_number(self, phone_number):
        if len(phone_number[4:]) != 9:
            return False
        return True

    def generate_sms_code(self):
        return randrange(100000, 999999)

    def send_message_sms(self, phone_number, message):
        send_verification_sms = SendVerificationSMSTwillo(phone_number)
        twillio_sms_successful, twillio_exception, twillio_raw_output = send_verification_sms.send(message)

        if not twillio_sms_successful and twillio_exception in ["internal", "other"]:
            # Try other providers
            send_verification_sms = SendVerificationSMSNexmo(phone_number)
            nexmo_sms_successful, nexmo_exception, nexmo_raw_output = send_verification_sms.send(message)
            if not nexmo_sms_successful and nexmo_exception in ["internal", "other"]:
                return False, "provider_error", nexmo_raw_output
            elif not nexmo_sms_successful and nexmo_exception == "invalid_number":
                # If the nexmo works, but the phone number is incorrect
                return False, "invalid_number", nexmo_raw_output
        elif not twillio_sms_successful and twillio_exception == "invalid_number":
            # If the twillio works, but the phone number is incorrect
            return False, "invalid_number", twillio_raw_output

        return True, None, None

    def post(self):
        phone_number = self.json_data.get('phoneNumber')

        # check temptoken
        temptoken_persists = self.check_temptoken()
        if not temptoken_persists:
            return self.get_no_temp_token_header_exception

        # validate req body
        valid_req_body = self.validate_req_body(self.schema, self.json_data)

        if not valid_req_body:
            return self.get_invalid_schema_request_message()

        # check if the phone number is not linked to an account
        is_phone_number_linked = self.search_for_phone_number(phone_number)

        if is_phone_number_linked:
            return {'message': self.translate.t('phoneAlreadyLinked'), 'field': 'phoneNumber'}, 403
  
        # check if the phone number is valid
        valid = self.validate_phone_number(phone_number)

        if not valid:
            return self.return_invalid_phone_number()

        try:  
            # get the previous information from the last session using the token
            session1_credentials = {
                "payload": {
                    **jwt.decode(self.get_temp_token, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])['payload'],
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
            code = self.generate_sms_code()
            processed_message = phoneVerificationFormatter(code, self.lang)

            success, exception, raw_exception = self.send_message_sms(message=processed_message, phone_number=phone_number)

            if not success and exception == "provider_error":
                return {
                   "message": self.translate.t('errorSendingSMS'),
                   "field": 'phoneNumber'
               }, 500
            elif not success and exception == "invalid_number":
                return self.return_invalid_phone_number()

            # get .env variables
            jwt_key = os.environ.get("SMS_JWT_KEY")
            code_encryption_key = os.environ.get("SMS_CODE_ENCRYPTION_KEY")

            # instantiate a crypto class instance
            encrypto = Encrypto()

            try:
                # to generate a code that only we can access and decrypt later
                print(code)
                encrypted_code = encrypto.encrypt(string=str(code), key=code_encryption_key)
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
            except Exception as e:
                return {
                    "message": e,
                    "field": "token"
                }, 403

        return {"message": f"Success! An message code was sent to {phone_number}", "token": token}, 200
