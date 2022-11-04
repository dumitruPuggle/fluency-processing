from random import randrange


class AuthProviderEmail:
    def __init__(self, email):
        self.email = email

    def generate_code(self):
        return randrange(100000, 999999)