# Load env
from dotenv import load_dotenv
load_dotenv()

#Import init_credentials
from credentials.init_credentials import *

from flask import Flask
from flask_restful import Api

#Imports for the API
from src.Root.rootPoint import Root
from src.Auth.SignUpSession1 import SignUpSession1

app = Flask(__name__)
api = Api(app)

#Routes
api.add_resource(Root, '/')
api.add_resource(SignUpSession1, '/api/signup/1')


if __name__ == '__main__':
    app.run(debug=True)