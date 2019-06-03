from google.appengine.ext import ndb
from google.appengine.api import search


class Topics(ndb.Model):
    user = ndb.KeyProperty(kind='Users')
    topic_title = ndb.StringProperty(required=True)

    @classmethod
    def add_new_topic(cls, user_key, topic):

        if user_key:
            user_id = str(user_key.id())

        topic_key = cls(
            user=user_key,
            topic_title=topic,
        ).put()

        # SEARCH INDEX FOR TOPICS
        index = search.Index('topics')
        topic_index_doc = search.Document(
            doc_id=str(topic_key.id()),
            fields=[
                search.TextField(name='user_id', value=user_id),
                search.TextField(name='topic', value=topic),
            ]
        )
        index.put(topic_index_doc)


    @classmethod
    def ret_all_topics_by_user(cls, user_id):
        index = search.Index('topics')
        query = 'user_id: (%s)' % user_id
        results = index.search(query)
        return results.results
