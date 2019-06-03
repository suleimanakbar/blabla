from webapp2 import WSGIApplication
from webapp2 import Route



app = WSGIApplication(
    routes=[
        Route('/', handler='app.home.Home'),
        Route('/register', handler='app.register_user.RegisterUser'),
        Route('/register/gmail', handler='app.register_user.RegisterGmailUser'),
        Route('/register/gmaillogout', handler='app.register_user.LogoutGmailUser'),
        Route('/user_profile/<user_id:[a-z0-9]+>/confirm/<confirmation_code:[a-z0-9]+>',
              handler='app.register_user.ConfirmUser'),
        Route('/login', handler='app.login_user.LoginUser'),

        Route('/user_profile', handler='app.user_profile.UserAccount'),

        Route('/user_profile/post-message', handler='app.user_profile.PostMessage'),
        Route('/user_profile/new-topic', handler='app.user_profile.PostTopic'),

        Route('/search', handler='app.search_results.MainMessages'),
        Route('/message/<message_id:[0-9]+>', handler='app.message.MessagePage'),
        Route('/topic/<topic_id:[0-9]+>', handler='app.topic.TopicPage'),


        Route('/mail/<key:[a-z0-9]+>', handler='app.mail.SendMail'),
        Route('/mail', handler='app.mail.SendMail'),

        Route('/reply/<message_id:[a-z0-9]+>', handler='app.message.CreateReply'),
        Route('/reply', handler='app.message.CreateReply'),
    ]
)

