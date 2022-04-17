#Import init_credentials
import os.path
import firebase_admin
from firebase_admin import credentials

# Create a variable dirname
dirname = os.path.dirname(__file__)

# Add the full location of the credential name
credential_file = os.path.join(dirname, 'credentials.json')

cred = credentials.Certificate(credential_file)
firebase_admin.initialize_app(cred)