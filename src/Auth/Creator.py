from src.Auth.User import User
from firebase_admin import auth
from firebase_admin import firestore

class Creator(User):
    def __init__(self, firstName, lastName, email, phoneNumber):
        super().__init__(firstName, lastName, email)
        self.role = "Creator"
        self.phoneNumber = phoneNumber
        self.db = firestore.client()

    def create_user(self, password):
        user = auth.create_user(
            email=self.email,
            email_verified=False,
            phone_number=self.phoneNumber,
            password=password,
            display_name=f'{self.firstName} {self.lastName}',
            disabled=False
        )
        self.uid = user.uid

    def insert_user_firestore(self):
        # try to add the user to the cloud firestore
        if self.uid is None:
            return {"message": "User not created"}, 400

        try:
            self.db.collection('users').document(self.uid).set({
                'firstName': self.firstName,
                'lastName': self.lastName,
                'email': self.email,
                'role': self.role,
                'phoneNumber': self.phoneNumber
            })
        except self.db.exceptions.FirestoreError:
            return {"message": "Internal server error"}, 500
    
    def create_token(self):
        # create a new token
        return auth.create_custom_token(self.uid).decode('utf-8')