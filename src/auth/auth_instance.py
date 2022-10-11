from flask_restful import Resource, request

class AuthInstance(Resource):
    def __init__(self):
        pass



    def get_temp_token(self):
        return request.headers.get('_temptoken')

    def check_header(self):
        temptoken = self.get_temp_token()

        if temptoken == None or len(temptoken) == 0:
            return {"message": "No token provided", "field": "token"}, 403