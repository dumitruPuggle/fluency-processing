import os
from firebase_admin import auth
import requests
from random import randrange
from mailjet_rest import Client
from src.email_html.verification_code import VerificationCodeHTMLTemplate
from lang.translate import fallback_lang

class AuthProviderEmail:
    def __init__(self, email):
        self.email = email

    def is_linked_to_an_account(self, email: str):
        try:
            auth.get_user_by_email(email)
        except ValueError:
            return None, 'invalid_email'
        except auth.UserNotFoundError:
            return False, None
        else:
            return True, None
            
    def generate_code(self):
        return randrange(100000, 999999)
        
    def send_code(self, to, code, lang=fallback_lang):
        # simulate some level of abstraction
        verification_html_template = VerificationCodeHTMLTemplate(lang=lang)
        api_key = '8ef5d7eb53026afc7d61bade39f2ba7b'
        api_secret = '663860c24a9a78264f44895c8a1d57b1'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
          'Messages': [
            {
              "From": {
                "Email": os.environ.get("EMAIL_SENDER_ADDRESS"),
                "Name": os.environ.get("EMAIL_SENDER_NAME")
              },
              "To": [
                {
                  "Email": to
                }
              ],
              "Subject": "Fluency verification code",
              "TextPart": "Please do not share this code to anyone!",
              "HTMLPart": verification_html_template.to_html(code),
              "CustomID": "AppGettingStartedTest"
            }
          ]
        }
        result = mailjet.send.create(data=data)
        print(result.json())

        return True, None