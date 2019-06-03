from handlers.request_handler import MainRequestHandler
from models.messages import Messages
from models.topics import Topics


class TopicPage(MainRequestHandler):
    def get(self, topic_id):
        #HANDLE THE REQUEST TO DISPLAY ALL MESSAGES WITH A CERTAIN TOPIC
        topic = Topics.get_by_id(int(topic_id))
        #GET ALL MESSAGES WITH THE SAME TOPIC
        messages = Messages.ret_all_messages_by_topic(topic.topic_title)
        #GENERATE THE VALUES TO BE DISPLAYED
        display_values = {
            'messages': messages,
            'topic': topic
        }

        self.render('message-page/topic-page.html', **display_values)
