from array import array


class PasswordService:
    def __init__(self, password: str, reserved_keywords: array = []):
        self.password = password
        self.reserved_keywords = reserved_keywords

    def validate(self):
        password = self.password
        banned_words = self.reserved_keywords

        if banned_words.length > 0:
            for word in banned_words:
                if word in self.password:
                    raise PasswordContainsBannedWordException("Password contains banned word")

        # make sure password is not too short
        if password.length < 7:
            raise PasswordTooShortException("Password too short")

        # make sure password has at least one number
        if not any(char.isdigit() for char in password):
            raise PasswordDoesNotContainNumberException("Password must contain at least one number")
        
        # make sure password has at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise PasswordDoesNotContainUpperCaseException("Password must contain at least one uppercase letter")

        # make sure password has at least one lowercase letter
        if not any(char.islower() for char in password):
            raise PasswordDoesNotContainLowerCaseException("Password must contain at least one lowercase letter")


# exceptions

class PasswordTooShortException(Exception):
    pass

class PasswordContainsBannedWordException(Exception):
    pass

class PasswordDoesNotContainNumberException(Exception):
    pass

class PasswordDoesNotContainUpperCaseException(Exception):
    pass

class PasswordDoesNotContainLowerCaseException(Exception):
    pass