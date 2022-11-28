from firebase_admin import auth
from random import randrange
from src.auth.tools.send_verification_code import SendVerificationSMSTwillo, SendVerificationSMSNexmo


class AuthProviderPhone:
    def __init__(self, phone_number):
        self.phoneNumber = phone_number

    def search_for_phone_number(self, phone_number):
        try:
            auth.get_user_by_phone_number(phone_number)
        except ValueError:
            return None, "invalid_phone_number"
        except auth.UserNotFoundError:
            return False, None
        else:
            return True, None

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