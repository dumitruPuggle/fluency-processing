# Load env
from dotenv import load_dotenv
from init import Init

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

#Imports for the API
from src.root.root_point import Root
from src.auth.signup_session_one import SignUpSession1
from src.auth.signup_session_two import SignUpSession2
from src.auth.signup_session_three import SignUpSession3
from src.auth.signup_session_four import SignUpSession4

from src.status.status import Status

init = Init()
init.init_firebase_admin()

load_dotenv()
app = Flask(__name__)
CORS(app)
api = Api(app)

#Routes
api.add_resource(Root, '/')
api.add_resource(Status, '/status')
api.add_resource(SignUpSession1, '/api/signup/1')
api.add_resource(SignUpSession2, '/api/signup/2')
api.add_resource(SignUpSession3, '/api/signup/3')
api.add_resource(SignUpSession4, '/api/signup/4')