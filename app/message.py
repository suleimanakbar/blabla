from handlers.request_handler import MainRequestHandler
from models.messages import Messages
from models.users import Users
from models.replies import Replies

#HANDLE THE REQUESTS PERTAINING TO THE MESSAGES MODEL
class MessagePage(MainRequestHandler):
    def get(self, message_id):
        #DISPLAY THE MESSAGE PAGE WITH THE MESSAGE SELECTED BY THE USER
        message = Messages.get_by_id(int(message_id))
        author = message.user.get()
        replies = Replies.ret_all_replies_by_message(int(message_id))
        message_display_values = {
            'message': message,
            'author': author,
            'message_id': message_id,
            'replies': replies
        }

        self.render('message-page/message-page.html', **message_display_values)

class CreateReply(MainRequestHandler):
    def get(self, message_id):
        #DISPLAY THE FORM THAT ALLOWS THE USER TO WRITE A REPLY
        reply_page_values = {
            'message_id': message_id
        }
        self.render('user_profile/post_reply.html', **reply_page_values)

    def post(self):
        #HANDLE THE REQUEST TO SUBMIT A REPLY TO A MESSAGE
        user_key = self.logged_in_user_status.key
        message_id = self.request.get('message_id')
        content = self.request.get('content')
        if message_id and content:
            #GET MESSAGE FROM MESSAGE ID
            message = Messages.get_by_id(int(message_id))
            #ADD THE REPLY TO THE DATASTORE TABLE
            Replies.new_reply(
                user_key=user_key,
                message_key=message.key,
                content=content
            )
            #RETURN BACK TO THE ORIGINAL MESSAGE PAGE
            self.redirect('/message/'+ message_id)