import os
from src.auth.auth_instance import AuthInstance
import jwt
from lang.phone_verification_formatter import phoneVerificationFormatter
from src.auth.encryption.encrypt import Encrypto
from time import time
from lang.translate import Translate
from src.auth.auth_provider_phone import AuthProviderPhone
from src.auth.auth_provider_email import AuthProviderEmail
from src.constant.constants_vars import PHONE_PROVIDER, EMAIL_PROVIDER, DEFAULT_PROVIDER


class SignUpSession2(AuthInstance):
    phone_schema = {
        'lang': 'String',
        'phoneNumber': "String",
        'provider': 'String'
    }

    email_schema = {
        'lang': 'String',
        'email': 'String',
        'provider': 'String'
    }

    def __init__(self):
        self.json_data = self.get_req_body
        self.lang = self.json_data.get('lang')
        self.translate = Translate(self.lang)

    def return_invalid_phone_number(self):
        return {'message': self.translate.t('invalidPhoneNumber'), 'field': 'phoneNumber'}, 403

    def post(self):
        # check temptoken
        temptoken_persists = self.check_temptoken()
        if not temptoken_persists:
            return self.get_no_temp_token_header_exception

        verification_provider = self.json_data.get('provider', DEFAULT_PROVIDER)
        phone_number = self.json_data.get('phoneNumber')

        if verification_provider == PHONE_PROVIDER:
            # validate req body for conditional phone provider
            valid_req_body_phone = self.validate_req_body(self.phone_schema, self.json_data)

            if not valid_req_body_phone:
                return self.get_invalid_schema_request_message()

            phone_provider = AuthProviderPhone(phone_number=phone_number)

            # check if the phone number is not linked to an account
            is_phone_number_linked = phone_provider.search_for_phone_number(phone_number)

            if is_phone_number_linked:
                return {'message': self.translate.t('phoneAlreadyLinked'), 'field': 'phoneNumber'}, 403

            # check if the phone number is valid
            phone_number_valid = phone_provider.validate_phone_number(phone_number)

            if not phone_number_valid:
                return self.return_invalid_phone_number()

            try:
                # get the previous information from the last session using the token
                session1_credentials = jwt.decode(self.get_temp_token, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])['payload']
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
                code = phone_provider.generate_sms_code()
                processed_message = phoneVerificationFormatter(code, self.lang)

                success, exception, raw_exception = phone_provider.send_message_sms(message=processed_message, phone_number=phone_number)

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

                    new_credentials = {
                        "payload": {
                            **session1_credentials,
                            "phoneNumber": phone_number
                        }
                    }

                    token = jwt.encode(
                        {
                            **new_credentials,
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

        elif verification_provider == EMAIL_PROVIDER:
            # validate req body for conditional email provider
            valid_req_body_email = self.validate_req_body(self.email_schema, self.json_data)

            if not valid_req_body_email:
                return self.get_invalid_schema_request_message()

            email_address = self.json_data.get('email')
            email_provider = AuthProviderEmail(email=email_address)

            return {"message": f"Success! An message code was sent to {email_address}", "token": "To be implemented"}, 200

        return {
            "message": "An error occurred"
        }
