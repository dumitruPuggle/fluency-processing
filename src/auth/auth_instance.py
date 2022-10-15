from flask_restful import Resource, request
import json
import copy

class AuthInstance(Resource):
    def __init__(self):
        pass

    @property
    def get_temp_token(self):
        return request.headers.get('_temptoken')

    @property
    def get_no_temp_token_header_exception(self):
        return {"message": "No token provided", "field": "token"}, 403

    def check_temptoken(self):
        temp_token = self.get_temp_token

        if temp_token is None or len(temp_token) == 0:
            return False

        return True

    @property
    def get_req_body(self):
        return request.get_json()

    def validate_req_body(self, schema: dict, json_data: dict):
        compare_schema = copy.deepcopy(schema)
        compare_json_data = copy.deepcopy(json_data)

        empty = len(compare_json_data.items()) == 0 or len(compare_schema.items()) == 0

        if empty:
            return False

        for key, value in compare_schema.items():
            compare_json_data[key] = str(type(value))

        for key, value in compare_json_data.items():
            compare_schema[key] = str(type(value))

        return compare_schema == compare_json_data

    def get_invalid_schema_request_message(self):
        return {
            'message': f'Your request does not meet the required standards. Please refer to the API documentation.',
            'field': 'request'
        }, 400
