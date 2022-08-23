import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

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
    except TwilioRestException:
        return {
            "message": "Error sending message",
            "field": "phoneNumber"
        }, 403
