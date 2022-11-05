from firebase_admin import auth
import requests
from random import randrange

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
        
    def send_code(self, to, code):
        # simulate some level of abstraction
        return True, None