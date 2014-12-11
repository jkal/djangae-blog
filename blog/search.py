from google.appengine.api import search


class PostIndex(object):
    """
    Simple wrapper over App Engine's search API.

    TODO: Indexing should be done in batch using a task queue
    but this will have to do for now.
    """

    def __init__(self, name):
        self.index = search.Index(name=name)

    def put(self, post):
        try:
            doc = search.Document(doc_id=str(post.id), fields=[
                search.TextField(name='slug', value=post.slug),
                search.TextField(name='title', value=post.title),
                search.TextField(name='author', value=post.author.email),
                search.HtmlField(name='content', value=post.content_markup),
            ])
            self.index.put(doc)
        except search.Error:
            pass

    def search(self, query):
        results = []
        if query:
            results = [{
                'slug': r.fields[0].value,
                'title': r.fields[1].value,
                'author': r.fields[2].value
            } for r in self.index.search(query)]
        return results

    def remove(self, post):
        self.index.delete([post.slug,])

index = PostIndex('posts')