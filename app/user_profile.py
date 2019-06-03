from handlers.request_handler import MainRequestHandler
from lib.cloudstorage import cloudstorage_api
from google.appengine.api import blobstore
from google.appengine.api import images
from google.appengine.api import app_identity
from models.messages import Messages
from models.topics import Topics
import os
import logging
import webapp2


class UserAccount(MainRequestHandler):
    # ALLOW ACCESS TO LOGGED IN USERS
    @MainRequestHandler.require_authentication
    def get(self):
        #GET THE CURRENT USER ID
        user_id = self.logged_in_user_status.key.id()
        #GET ALL THE MESSAGES FOR THE USER
        messages = Messages.ret_all_messages_by_user(user_id)
        #GET ALL THE TOPICS FOR THE USER
        topics = Topics.ret_all_topics_by_user(user_id)
        #PARSING THE MESSAGES AND TOPICS TO THE TEMPLATE
        display_values = {
            'messages': messages,
            'topics': topics
        }
        #RENDER THE PERSONAL HOME PAGE
        self.render('user_profile/account_home.html', **display_values)


# # RECHECK FUNCTION
# class ConfirmUser(MainRequestHandler):
#     def get(self, confirmation_code):
#         print('hello')
#         # print(confirmation_code)
#         self.render('account/account_home.html')

# POST TOPIC HANDLER
class PostTopic(MainRequestHandler):
    @MainRequestHandler.require_authentication
    def get(self):
        #RENDER THE FORM USED TO POST A TOPIC
        self.render('user_profile/post_topic.html')

    @MainRequestHandler.require_authentication
    def post(self):
        #GET THE CURRENT LOGGED IN USER KEY
        user_key = self.logged_in_user_status.key
        #GET THE TOPIC TO BE POSTED FROM THE FORM
        topic = self.request.get('topic')
        #ADD THE TOPIC TO THE DATASTORE
        Topics.add_new_topic(
            user_key=user_key,
            topic=topic,
        )
        #RETURN TO THE PERSONAL HOME PAGE
        self.redirect('/user_profile')

# POST MESSAGE HANDLER
class PostMessage(MainRequestHandler):
    @MainRequestHandler.require_authentication
    def get(self):
        #RENDER THE FORM TO POST A NEW MESSAGE
        self.render('user_profile/post_message.html')

    # POST MESSAGE
    @MainRequestHandler.require_authentication
    def post(self):
        #GET THE CURRENT LOGGED IN USER
        user_key = self.logged_in_user_status.key
        #GET THE MESSAGE VALUES FROM THE FORM
        title = self.request.get('title')
        topic = self.request.get('topic')
        content = self.request.get('content')
        photo = self.request.POST['image']
        if photo:
            saved_photo = self.save_image(photo, user_key)
            #ADD THE MESSAGE TO THE DATASTORE
            Messages.new_message(
                user_key=user_key,
                title=title,
                topic=topic,
                content=content,
                photo_key=saved_photo['blobstore_key'],
                photo_url=saved_photo['serving_url']
            )
        else:
            Messages.new_message(
                user_key=user_key,
                title=title,
                topic=topic,
                content=content,
                photo_key=None,
                photo_url=''
            )
        #RETURN TO THE PERSONAL HOME PAGE
        self.redirect('/user_profile')

    # SAVE IMAGE HELPER -- FROM GOOGLE DOCUMENTATION
    @classmethod
    def save_image(cls, photo, user_key):

        img_title = photo.filename
        img_content = photo.file.read()
        img_type = photo.type

        cloud_storage_path = '' % (user_key.id(), img_title)
        blobstore_key = blobstore.create_gs_key(cloud_storage_path)

        cloud_storage_file = cloudstorage_api.open(
            filename=cloud_storage_path[3:],
            mode='w',
            content_type=img_type
        )
        cloud_storage_file.write(img_content)
        cloud_storage_file.close()

        blobstore_key = blobstore.BlobKey(blobstore_key)
        serving_url = images.get_serving_url(blobstore_key)

        return {
            'serving_url': serving_url,
            'blobstore_key': blobstore_key
        }


