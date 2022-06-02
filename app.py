# Load env
from dotenv import load_dotenv
load_dotenv()

# Import init_credentials
from credentials.init_credentials import *

from flask import Flask
from flask_restful import Api

#Imports for the API
from src.Root.rootPoint import Root
from src.Auth.SignUpSession1 import SignUpSession1
from src.Auth.SignUpSession2 import SignUpSession2
from src.Auth.SignUpSession3 import SignUpSession3
from src.Auth.SignUpSession4 import SignUpSession4

app = Flask(__name__)
api = Api(app)

#Routes
api.add_resource(Root, '/')
api.add_resource(SignUpSession1, '/api/signup/1')
api.add_resource(SignUpSession2, '/api/signup/2')
api.add_resource(SignUpSession3, '/api/signup/3')
api.add_resource(SignUpSession4, '/api/signup/4')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)