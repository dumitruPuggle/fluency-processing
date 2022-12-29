# Load env
from dotenv import load_dotenv
from init import Init

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

#Imports for the API
from src.root.root_point import Root
from src.auth.verify_session_1 import VerifyAccountSession1
from src.auth.verify_session_2 import VerifyAccountSession2
from src.auth.verify_session_3 import VerifyAccountSession3
from src.auth.verify_session_4 import VerifyAccountSession4
from src.auth.auth_is_user_verified import AuthIsUserVerified

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
api.add_resource(VerifyAccountSession1, '/api/verify/1')
api.add_resource(VerifyAccountSession2, '/api/verify/2')
api.add_resource(VerifyAccountSession3, '/api/verify/3')
api.add_resource(VerifyAccountSession4, '/api/verify/4')
api.add_resource(AuthIsUserVerified, '/api/is-user-verified')
