from firebase_admin import auth, firestore
from src.constant.constants_vars import PHONE_PROVIDER, EMAIL_PROVIDER
from time import time
import os
import jwt


class User:
    def __init__(self, provider_type, verified, firstName, lastName, email, phone_number=None, user_type=None, other_data=None):
        self.provider_type = provider_type
        self.verified = verified
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone_number = phone_number
        self.user_type = user_type
        self.other_data = other_data

        self.db = firestore.client()

    def create_user(self, password):
        user = auth.create_user(
            email=self.email,
            email_verified=self.provider_type == EMAIL_PROVIDER and self.verified,
            phone_number=self.phone_number,
            password=password,
            display_name=f'{self.firstName} {self.lastName}',
            disabled=False
        )
        self.uid = user.uid
        self.__insert_user_firestore__()

    def update_user(self, uid, password):
        user = auth.update_user(
            uid,
            email=self.email,
            phone_number=self.phone_number,
            email_verified=self.provider_type == EMAIL_PROVIDER and self.verified,
            password=password,
            display_name=f'{self.firstName} {self.lastName}',
            disabled=False)
        self.uid = user.uid
        self.__insert_user_firestore__()

    def __compute_user_verified_trust_token__(self):
        jwt_key = os.environ.get('COMPUTE_ACCOUNT_VERIFICATION')
        server_id = os.environ.get('SERVER_ID')
        contents = {
            "computed_at": time(),
            "valid": True,
            "server": server_id
        }
        token = jwt.encode(contents, jwt_key, algorithm='HS256')
        return token

    def __insert_user_firestore__(self):
        # try to add the user to the cloud firestore
        if self.uid is None:
            raise Exception("self.uid is None")

        user_data = {
            'verification_certificate_jwt': self.__compute_user_verified_trust_token__()
        }

        if self.phone_number is not None and self.provider_type == PHONE_PROVIDER:
            user_data['phoneNumber'] = self.phone_number

        self.db.collection('users').document(self.uid).set(user_data)

    @staticmethod
    def validate(email: str) -> bool:
        db = firestore.client()
        uid = auth.get_user_by_email(email).uid
        jwt_key = os.environ.get('COMPUTE_ACCOUNT_VERIFICATION')

        try:
            user_doc_ref = db.collection('users').document(uid)
            verification_certificate_jwt = user_doc_ref.get(
            ).to_dict().get('verification_certificate_jwt')
        except Exception as e:
            print(e)
            return False

        try:
            jwt.decode(verification_certificate_jwt,
                       jwt_key, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError or jwt.exceptions.DecodeError:
            return False
        except Exception as e:
            return False
        else:
            return True

    @staticmethod
    def insert_user_type(uid: str, user_type) -> bool:
        db = firestore.client()

        try:
            user_doc_ref = db.collection('users').document(uid)
            indexed_user_type = user_doc_ref.to_dict().get('user_type')

            if indexed_user_type == None:
                return False
            
            user_doc_ref.set({
                u'user_type': user_type
            })
        except Exception:
            return False
        else:
            return True
