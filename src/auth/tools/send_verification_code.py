import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import json
import vonage

def send_verification_code(phone_number, message):
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            to=phone_number
        )
    except TwilioRestException as e:
        print(e)
        return {
            "message": "Error sending message",
            "field": "phoneNumber"
        }, 403


class SendVerificationSMS:
    def __init__(self, phone_number):
        self.phone_number = phone_number


class SendVerificationSMSTwillo(SendVerificationSMS):
    def __init__(self, phone_number: str):
        super().__init__(phone_number)
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    def send(self, message: str) -> (bool, ):
        try:
            client = Client(self.account_sid, self.auth_token)
            result = client.messages.create(
                body=message,
                from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                to=self.phone_number
            )
        except TwilioRestException as e:
            # return reason
            raw_exception = json.loads(json.dumps({"reason": e.__str__()})).get('reason')

            if "Authenticate\u001b" in raw_exception:
                exception = "internal"
            else:
                exception = "other"

            return False, exception, e
        else:
            return True, None, result


class SendVerificationSMSNexmo(SendVerificationSMS):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.phone_number = phone_number
        self.nexmo_from = os.environ.get('NEXMO_FROM')
        self.nexmo_key = os.environ.get('NEXMO_KEY')
        self.nexmo_secret = os.environ.get('NEXMO_SECRET')

    def format_phone_number_for_nexmo_variant(self):
        self.phone_number = f'373{self.phone_number[5:]}'

    def send(self, message):
        self.format_phone_number_for_nexmo_variant()

        client = vonage.Client(key=self.nexmo_key, secret=self.nexmo_secret)
        sms = vonage.Sms(client)

        response_data = sms.send_message(
            {
                "from": self.nexmo_from,
                "to": self.phone_number,
                "text": message,
            }
        )

        if response_data["messages"][0]["status"] == "0":
            return True, None, response_data
        elif response_data["messages"][0]["status"] == '29':
            return False, "internal", response_data
        else:
            return False, "other", response_data
