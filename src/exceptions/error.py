from flask_restful import Resource


def postError(message, status_code: int):
    class Error(Resource):
        def post(self):
            return message, status_code
    return Error