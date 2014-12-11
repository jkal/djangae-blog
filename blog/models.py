from django.core.urlresolvers import reverse
from django.db import models
from djangae.contrib.gauth.models import GaeDatastoreUser
from djangae.fields import RelatedSetField
import markdown


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Post(models.Model) :
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content_markdown = models.TextField()
    content_markup = models.TextField(editable=False)
    published = models.DateTimeField(auto_now_add=True)

    # Drafts are only visible to their author.
    draft = models.BooleanField(default=False)

    author = models.ForeignKey(GaeDatastoreUser)
    tagobjs = RelatedSetField(Tag)

    class Meta:
        ordering = ['-published']

    def save(self):
        self.content_markup = markdown.markdown(self.content_markdown)
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse('post', args=(self.slug,))

    def __unicode__(self):
        return self.title

