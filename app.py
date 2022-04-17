# Load env
from dotenv import load_dotenv
load_dotenv()

#Import init_credentials
from credentials.init_credentials import *

from flask import Flask
from flask_restful import Api

#Imports for the API
from src.Root.rootPoint import Root
from src.Auth.SignUp import SignUp

app = Flask(__name__)
api = Api(app)

#Routes
api.add_resource(Root, '/')
api.add_resource(SignUp, '/api/signup')

if __name__ == '__main__':
    app.run(debug=True)