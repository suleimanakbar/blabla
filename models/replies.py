from google.appengine.ext import ndb
from google.appengine.api import search


class Replies(ndb.Model):
    user = ndb.KeyProperty(kind='Users')
    message_id = ndb.KeyProperty(required=True)
    content = ndb.StringProperty(required=True)

    @classmethod
    def new_reply(cls, user_key, message_key, content):
        if user_key:
            user_id = str(user_key.id())
        if message_key:
            message_id = str(message_key.id())

        reply_key = cls(
            user=user_key,
            message_id=message_key,
            content=content
        ).put()

        # SEARCH INDEX FOR MESSAGES
        index = search.Index('replies')
        replies_index_doc = search.Document(doc_id=str(reply_key.id()),
                                             fields=[
                                                 search.TextField(name='user_id', value=user_id),
                                                 search.TextField(name='message_id', value=message_id),
                                                 search.TextField(name='content', value=content)
                                             ]
                                             )

        index.put(replies_index_doc)

    @classmethod
    def ret_all_replies_by_message(cls, message_id):
        index = search.Index('replies')
        query = 'message_id: (%s)' % message_id
        results = index.search(query)
        return results.results

    # @classmethod
    # def ret_all_messages_by_topic(cls, topic):
    #     index = search.Index('messages')
    #     query = 'topic: (%s)' % topic
    #     results = index.search(query)
    #     return results.results
