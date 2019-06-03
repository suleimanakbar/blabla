from handlers.request_handler import MainRequestHandler
from google.appengine.api import search


class MainMessages(MainRequestHandler):
    def get(self):
        #ALLOWS USERS TO SEARCH THROUGH ALL THE MESSAGES IN THE DATASTORE
        search_query = self.request.get('q')
        #CHECK IF THERE IS A SEARCH QUERY
        if search_query == '':
            self.redirect('/')
        else:
            #SPECIFY THAT THE SEARCH WILL BE DONE ON THE MESSAGES AND THEIR CONTENT
            index = search.Index('messages')
            #GENERATE THE SEARCH QUERY
            snippet = 'snippet("%s", content, 140)' % search_query
            query_options = search.QueryOptions(
                returned_expressions=[
                    search.FieldExpression(name='snippet', expression=snippet)
                ]
            )
            results = index.search(
                query=search.Query(
                    query_string=search_query,
                    options=query_options
                )

            )
            #CREATE AN ARRAY FOR THE SEARCH RESULTS
            messages = []
            if results:
                messages = results.results

            display_values = {
                'messages': messages,
                'query': search_query
            }
            #DISPLAY THE RESULTS FOUND IN THE SEARCH RESULTS PAGE
            self.render('search_results/search_results.html', **display_values)
