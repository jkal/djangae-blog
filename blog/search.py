from google.appengine.api import search 
from blog.models import Post

class PostIndex(object):
    """
    Simple wrapper over App Engine's search API.

    TODO: Indexing should be done in batch using a task queue
    but this will have to do for now.
    """

    def __init__(self):
        self.index = search.Index(name='posts')

    def put(self, post):
        try:
            doc = search.Document(doc_id=post.slug, fields=[
                search.TextField(name='title', value=post.title),
                search.TextField(name='author', value=post.author.email),
                search.HtmlField(name='content', value=post.content_markup),
            ])
            self.index.put(doc)
        except search.Error:
            pass

    def search(self, query):
        results = [{
            'id': r.doc_id,
            'title': r.fields[0].value,
            'author': r.fields[1].value
        } for r in self.index.search(query)]
        return results

index = PostIndex()