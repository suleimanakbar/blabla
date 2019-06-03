from webapp2 import RequestHandler
from webapp2 import cached_property
from google.appengine.api import users
import os
import jinja2


class MainRequestHandler(RequestHandler):
    template_directory = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
        'templates')

    jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_directory)
    )

    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/glogout')
        greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
            nickname, logout_url)
    else:
        login_url = users.create_login_url('/glogin')
        greeting = '<a href="{}">Sign in</a>'.format(login_url)

    def render(self, template, **kwargs):
        jinja_template = self.jinja_environment.get_template(template)
        html_from_template = jinja_template.render(kwargs)
        self.response.out.write(html_from_template)

    def json_resp(self, status_code=200, **kwargs):
        from json import dumps
        self.response.status = status_code
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(dumps(kwargs))

    # READ COOKIE FUNCTION TO CHECK COOKIE VAL
    def read_cookie(self, name):
        from handlers.cookie_handler import evaluate_cookie
        cookie_value = self.request.cookies.get(name)
        return evaluate_cookie(cookie_value)

    # SEND SIGNED COOKIE
    def send_cookie(self, name, value):
        from handlers.cookie_handler import sign_cookie
        signed_cookie_value = sign_cookie(value)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, signed_cookie_value))

    #A CACHED PROPERTY TO BE USED ON REQUESTS TO CHECK THE AUTHENTICATION STATUS OF THE USER
    @cached_property
    def logged_in_user_status(self):
        if self.request.cookies.get('User'):
            #GET THE COOKIE VALUE
            id = self.read_cookie('User')
            #CHECK THE STATUS OF THE COOKIE
            if id:
                from models.users import Users
                #RETURN THE USER
                return Users.get_by_id(int(id))
            else:
                return None
        return None

    # LOGIN REQUIRED WRAPPER
    @staticmethod
    def require_authentication(handler):
        #CREATE A CHECK TO BE ADDED AT THE BEGINNING OF REQUEST METHODS TO CHECK THE LOGIN STATUS
        def login_status(self, *args, **kwargs):
            if self.logged_in_user_status:
                return handler(self, *args, **kwargs)
            else:
                return self.redirect('/login')

        return login_status
