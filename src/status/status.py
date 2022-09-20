from flask_restful import Resource, request

class Status(Resource):
    def get(self):
        return {
            "message": "All systems functional"
        }, 200