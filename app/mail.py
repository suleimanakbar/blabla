from handlers.request_handler import MainRequestHandler
from models.users import Users
from models.messages import Messages
from google.appengine.api import mail
from os import environ
import re

#ALLOWS USERS TO SEND EMAILS TO OTHER USERS USING THE GOOGLE
#APP ENGINE MAILING API

class SendMail(MainRequestHandler):
    @MainRequestHandler.require_authentication
    def get(self, key):
        #GET THE MESSAGE CLICKED ON BY THE USER
        message = Messages.get_by_id(int(key))
        #GET THE AUTHOR OF THAT MESSAGE
        author = message.user.get()
        display_values = {
            'author': author
        }
        # DISPLAY THE FORM TO SEND OTHER USERS AN EMAIL
        self.render('email/send_email.html', **display_values)

    @MainRequestHandler.require_authentication
    def post(self):
        #GET THE VALUES GENERATED BY THE EMAIL FORM
        email = self.request.get('user_email')
        subject = self.request.get('subject')
        content = self.request.get('message')
        #CHECK THE VALIDITY OF ALL THE VALUES
        if email and subject and content:
            self.send_email(email, content, subject)
        #RETURN BACK TO THE HOME DIRECTORY
        self.redirect('/')

    @classmethod
    def send_email(cls, to, content, subject):
        #SEND EMAIL FUNCTION TO SEND MESSAGES TO OTHER USERS ADDRESSES
        #USING THE GOOGLE MAIL API
        email_object = mail.EmailMessage(
            sender='noreply@ultra-water-197221.appspotmail.com',
            subject=subject,
            to=to
        )
        #GENERATE THE EMAIL PARAMETERS
        email_parameters = {
            'domain': 'http://localhost:8081' if environ['SERVER_SOFTWARE'].startswith(
                'Development') else 'http://ultra-water-197221.appspot.com',
            'subject': subject,
            'content': content
        }

        html_from_template = cls.jinja_environment.get_template('email/message_email.html').render(email_parameters)
        email_object.html = html_from_template
        email_object.send()
