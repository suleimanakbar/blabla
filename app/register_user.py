from handlers.request_handler import MainRequestHandler
from models.users import Users
from google.appengine.api import mail
from os import environ
from google.appengine.api import users
import re


# REGISTER USER HANDLER - CHECK USER DATA AND ADDS USER
class RegisterUser(MainRequestHandler):

    def post(self):
        #GET THE VALUES FROM THE REGISTER FORM
        name = self.request.get('name')
        email = self.request.get('email')
        password = self.request.get('password')

        # DEFAULT STATUS
        user_status = 200

        if name and email and password:
            # USER EMAIL PATTERNS ALLOWED USING RE LIBRARY
            re_pattern_email = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

            # MATCH EMAIL PATTERNS
            if re.match(re_pattern_email, email):

                # USER ADDED
                user = Users.add_new_user(name, email, password)

                if user['created']:

                    # RETURN REGISTRATION CONFIRMATION AND SEND EMAIL
                    html = self.jinja_environment.get_template('register/register_success.html').render()
                    json_response = {
                        'html': html
                    }
                    self.acc_conf_email(to=email, name=name, user_id=user['user_id'],
                                        confirmation_code=user['confirmation_code'])

                else:
                    # RETURN USER
                    user_status = 400
                    json_response = user

                    # EMAIL PATTERN ERROR
            else:
                user_status = 400
                json_response = {
                    'created': False,
                    'title': 'The email is not valid',
                    'message': 'Please enter a valid email'
                }

                # REGISTRATION ERRORS
        else:
            user_status = 400
            json_response = {}

            if not name:
                json_response.update({
                    'title': 'The name field is required',
                    'message': 'Please fill in name !'
                })
            if not email:
                json_response.update({
                    'title': 'The email field is required',
                    'message': 'Please supply a valid email!'
                })
            if not password:
                json_response.update({
                    'title': 'Password required',
                    'message': 'Please supply a valid password!'
                })
        self.json_resp(status_code=user_status, **json_response)

    # SEND EMAIL TO CONFIRM USER REGISTRATION
    @classmethod
    def acc_conf_email(cls, to, name, user_id, confirmation_code):
        email_obj = mail.EmailMessage(
            sender='noreply@testproj-197311.appspotmail.com',
            subject='Confirm your BlaBla user_profile',
            to=to
        )

        # EMAIL PARAMETERS PERTAINING TO BOTH LOCAL ENV AND APP ENGINE
        email_params = {
            'domain': 'http://localhost:8080' if environ['SERVER_SOFTWARE'].startswith(
                'Development') else 'http://testproj-197311.appspot.com',
            'name': name,
            'user_id': user_id,
            'confirmation_code': confirmation_code
        }

        # SEND EMAIL USING HTML TEMPLATE
        email_obj.html = cls.jinja_environment.get_template('email/confirmation_email.html').render(email_params)
        email_obj.send()

class RegisterGmailUser(MainRequestHandler):
    def get(self):
        user = users.get_current_user()

        verified_user = Users.check_gmail(user.email())
        id = verified_user
        print(id)

        if verified_user:
            self.send_cookie(name='User', value=id)
        else:
            None
        self.redirect('/')


class LogoutGmailUser(MainRequestHandler):
    def get(self):
        print('this is the cookie logout')
        self.response.headers.add_header('Set-Cookie', 'User=%d; Path=/' % (0))
        self.redirect('/')


# CONFIRM USER HANDLER
class ConfirmUser(MainRequestHandler):

    def get(self, user_id, confirmation_code):
        user = Users.get_by_id(int(user_id))

        if user.confirmation_code == confirmation_code:
            user.confirmed_email = True
            user.put()

        self.render('user_profile/account_home.html')
