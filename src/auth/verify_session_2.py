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
from src.email_html.verification_code import VerificationCodeHTMLTemplate

class VerifyAccountSession2(AuthInstance):
    phone_schema = {
        'phoneNumber': "String",
        'provider': 'String'
    }

    email_schema = {
        'email': 'String',
        'provider': 'String'
    }

    def __init__(self):
        self.json_data = self.get_req_body
        self.lang = self.get_lang_from_previous_session
        self.translate = Translate(self.lang)

    def return_invalid_phone_number(self):
        return {'message': self.translate.t('invalidPhoneNumber'), 'field': 'phoneNumber'}, 403
        
    def return_invalid_email_address(self):
        return {'message': self.translate.t('invalidEmailAddress'), 'field': 'email'}, 403

    def post(self):
        # get .env variables required for this operation
        jwt_key = os.environ.get("SMS_JWT_KEY")
        code_encryption_key = os.environ.get("SMS_CODE_ENCRYPTION_KEY")
        
        verification_provider = self.json_data.get('provider', DEFAULT_PROVIDER)
        
        # check if verification provider element is type string.
        if type(verification_provider) != type('String'):
            return self.get_invalid_schema_request_message()
        
        # check temptoken
        temptoken_persists = self.check_temptoken()
        if not temptoken_persists:
            return self.get_no_temp_token_header_exception
            
        previous_session_credentials, previous_session_decode_exception = self.decode_previous_session()

        if verification_provider == PHONE_PROVIDER:
            # validate req body for conditional phone provider
            valid_req_body_phone = self.validate_req_body(self.phone_schema, self.json_data)

            if not valid_req_body_phone:
                return self.get_invalid_schema_request_message()

            phone_number = self.json_data.get('phoneNumber')
            phone_provider = AuthProviderPhone(phone_number=phone_number)

            # check if the phone number is not linked to an account
            is_phone_number_linked, firebase_search_exception = phone_provider.search_for_phone_number(phone_number)

            if firebase_search_exception == "invalid_phone_number":
                return self.return_invalid_phone_number()
            
            if is_phone_number_linked:
                return {'message': self.translate.t('phoneAlreadyLinked'), 'field': 'phoneNumber'}, 403
            
            if previous_session_credentials is not None:
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
                            **previous_session_credentials,
                            "phoneNumber": phone_number,
                            "provider": PHONE_PROVIDER
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
                        "message": self.translate.t('internal_server_error'),
                        "field": "token"
                    }, 403
                else:
                    return {"message": f"{self.translate.t('success_an_message_code_has_been_sent_to')} {phone_number}", "token": token}, 200
            elif previous_session_decode_exception == "token_expired":
                return {
                    "message": self.translate.t('token_expired')
                }, 403
            elif previous_session_decode_exception == "invalid_token":
                return {
                    "message": self.translate.t('invalid_token')
                }, 403

        elif verification_provider == EMAIL_PROVIDER:
            # validate req body for conditional email provider
            valid_req_body_email = self.validate_req_body(self.email_schema, self.json_data)

            if not valid_req_body_email:
                return self.get_invalid_schema_request_message()

            email_address = self.json_data.get('email')
            email_provider = AuthProviderEmail(email=email_address)
            
            # check if email is not linked to any existing accounts
            verify_existing_account = previous_session_credentials.get('verify_existing_account', False)
            is_email_linked, email_exception = email_provider.is_linked_to_an_account(email=email_address)
            
            if email_exception == "invalid_email":
                return self.return_invalid_email_address()
            
            if verify_existing_account is False and is_email_linked:
                return {
                    'message': self.translate.t('emailAlreadyLinked'),
                    'field': 'email'
                }, 403

            if previous_session_credentials is not None:
                # send code to email address
                email_code = email_provider.generate_code()
                sent_successfully, send_code_exception = email_provider.send_code(to=email_address, code=email_code, lang=self.lang)
                
                print(email_code)
                
                if sent_successfully:
                    # prepare JWT Token
                    encrypto = Encrypto()
                    try:
                        # to generate a code that only we can access and decrypt later
                        encrypted_code = encrypto.encrypt(string=str(email_code), key=code_encryption_key)
                        # expire in 5 minutes
                        expiration_time = time() + 10
                    
                        new_credentials = {
                            "payload": {
                                **previous_session_credentials,
                                "provider": EMAIL_PROVIDER
                            }
                        }
                    
                        token = jwt.encode(
                            {
                                **new_credentials,
                                "code": email_code,
                                "exp": expiration_time
                            },
                            jwt_key,
                            algorithm='HS256'
                        )
                    except Exception as e:
                        print(e)
                        return {
                            "message": self.translate.t("internal_server_error"),
                            "field": "token"
                        }, 403
                    else:
                        return {"message": f"{self.translate.t('success_an_message_code_has_been_sent_to')} {email_address}", "token": token}, 200
                elif send_code_exception == "error_send":
                    return {
                        "message": self.translate.t('error_sending_message_code_at_this_time'),
                        "field": "email"
                    }
            elif previous_session_decode_exception == "token_expired":
                return {
                    "message": self.translate.t('token_expired')
                }, 403
            elif previous_session_decode_exception == "invalid_token":
                return {
                    "message": self.translate.t('invalid_token')
                }, 403
        else:
            return {
                "message": self.translate.t('you_have_chosen_an_incorrect_auth_provider'), "field": "request"
            }, 400
            
        return {
            "message": "An error occurred"
        }
