from handlers.request_handler import MainRequestHandler
from google.appengine.api import users


class Home(MainRequestHandler):
    def get(self):
        user = users.get_current_user()
        print(user)
        if user:
            url = users.create_logout_url('/register/gmaillogout')
            url_linktext = 'G Logout'
        else:
            url = users.create_login_url('/register/gmail')
            url_linktext = 'G Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = self.jinja_environment.get_template('home/home.html')
        self.response.write(template.render(template_values))
        #RENDER THE HOME PAGE
        #self.render('home/home.html')
