from google.appengine.ext import ndb
from hashlib import sha256
from base64 import b64encode
from os import urandom
import uuid
from google.appengine.api import users


# USER DATASTORE STRUCTURE
class Users(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    confirmation_code = ndb.StringProperty(required=True)
    confirmed_email = ndb.BooleanProperty(default=False)

    # ADD NEW USER
    @classmethod
    def add_new_user(cls, name, email, password):
        user = cls.existing_email(email)

        if not user:
            # ENCRYPT NEW USER PASSWORDS AND GENERATE ACCOUNT CONFIRM CODE
            random_bytes = urandom(64)
            salt = b64encode(random_bytes).decode('utf-8')
            hashed_password = salt + sha256(salt + password).hexdigest()

            confirm_code = str(uuid.uuid4().get_hex())

            # ENTER USER INTO DATASTORE
            new_user_key = cls(
                name=name,
                email=email,
                password=hashed_password,
                confirmation_code=confirm_code
            ).put()

            # RETURN NEW USER ID AND CONFIRMATION CODE
            return {
                'created': True,
                'user_id': new_user_key.id(),
                'confirmation_code': confirm_code
            }
        # IN CASE OF ERROR
        else:
            return {
                'created': False,
                'title': 'This email is in use!',
                'message': 'Please use another user_profile.'
            }

    # CHECK IF USER EMAIL ALREADY EXISTS
    @classmethod
    def existing_email(cls, email):
        return cls.query(cls.email == email).get()

    # GET USER METHOD
    @classmethod
    def get_user(cls, user_id):
        return cls.query(cls.ID == user_id)

    # CHECK PASSWORD
    @classmethod
    def password_verification(cls, email, password):
        #CHECK THE VALIDITY OF THE REQUESTED EMAIL ADDRESS
        user = cls.existing_email(email)
        if user:
            h_password = user.password
            noise = h_password[:88]

            check_password = noise + sha256(noise + password).hexdigest()
            if check_password == h_password:
                return user.key.id()
            else:
                return None
        else:
            return None

    @classmethod
    def check_gmail(cls, email):
        user = cls.existing_email(email)
        if user:
            return user.key.id()
        else:
            return None