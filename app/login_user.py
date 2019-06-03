from handlers.request_handler import MainRequestHandler
from models.users import Users
from google.appengine.api import users


class LoginUser(MainRequestHandler):
    def get(self):
        #RENDER THE LOGIN PAGE
        self.render('login/login.html')

    def post(self):
        #GET THE VALUES FROM THE LOGIN PAGE
        email = self.request.get('email')
        password = self.request.get('password')
        #VALIDATE USERNAME AND PASSWORD
        user_id = Users.password_verification(email, password)
        if user_id:
            # CHECK IF USER IS LOGGED IN AND SEND COOKIE
            self.send_cookie(name='User', value=user_id)
            #GO TO PERSONAL HOME PAGE IF SUCCESSFUL
            self.redirect('/user_profile')
        else:
            #RETURN TO LOGIN PAGE IS UNSUCCESSFUL
            self.redirect('/login')

class LoginGUser(MainRequestHandler):
    def post(self, user_id):
        #user = users.get_current_user()

        if user_id:
            # CHECK IF USER IS LOGGED IN AND SEND COOKIE
            self.send_cookie(name='User', value=user_id)
            self.redirect('/account')

        else:
            self.redirect('/login')