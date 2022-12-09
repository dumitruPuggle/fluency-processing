from lang.translate import Translate
from src.auth.auth_instance import AuthInstance
from src.auth.users.user import User
from src.constant.constants_vars import DEFAULT_LANGUAGE


class AuthIsUserVerified(AuthInstance):
    schema = {
        'email': 'String'
    }

    def __init__(self):
        self.json_data = self.get_req_body
        self.lang = self.json_data.get('lang', DEFAULT_LANGUAGE)
        self.translate = Translate(self.lang)

    def post(self):
        # validate req body
        valid_req_body = self.validate_req_body(self.schema, self.json_data)

        if not valid_req_body:
            return self.get_invalid_schema_request_message()

        try:
            is_valid = User.validate(email=self.json_data.get('email'))
        except Exception as e:
            print(e)
            return {
                'isValid': None,
                'success': False
            }, 400
        else:
            return {
                'isValid': is_valid,
                'success': True
            }, 200
