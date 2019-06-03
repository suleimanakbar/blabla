from google.appengine.ext import ndb
from google.appengine.api import search


class Messages(ndb.Model):
    user = ndb.KeyProperty(kind='Users')
    title = ndb.StringProperty(required=True)
    topic = ndb.StringProperty(required=True)
    content = ndb.StringProperty()
    photo_key = ndb.BlobKeyProperty()
    photo_url = ndb.StringProperty()

    @classmethod
    def new_message(cls, user_key, title, topic, content, photo_key, photo_url):
        if user_key:
            user_id = str(user_key.id())

        message_key = cls(
            user=user_key,
            title=title,
            topic=topic,
            content=content,
            photo_key=photo_key,
            photo_url=photo_url
        ).put()

        # SEARCH INDEX FOR MESSAGES
        index = search.Index('messages')
        messages_index_doc = search.Document(doc_id=str(message_key.id()),
                                             fields=[
                                                 search.TextField(name='user_id', value=user_id),
                                                 search.TextField(name='title', value=title),
                                                 search.TextField(name='topic', value=topic),
                                                 search.TextField(name='content', value=content),
                                                 search.TextField(name='photo_url', value=photo_url)
                                             ]
                                             )

        index.put(messages_index_doc)

    @classmethod
    def ret_all_messages_by_user(cls, user_id):
        index = search.Index('messages')
        query = 'user_id: (%s)' % user_id
        results = index.search(query)
        return results.results

    @classmethod
    def ret_all_messages_by_topic(cls, topic):
        index = search.Index('messages')
        query = 'topic: (%s)' % topic
        results = index.search(query)
        return results.results
