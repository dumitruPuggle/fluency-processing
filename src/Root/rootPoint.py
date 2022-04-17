from flask_restful import Resource

class Root(Resource):
    def get(self):
        return {'status': '200OK!'}