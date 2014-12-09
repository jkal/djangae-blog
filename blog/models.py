from django.core.urlresolvers import reverse
from django.db import models
from djangae.contrib.gauth.models import GaeDatastoreUser
import markdown

class Post(models.Model) :
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content_markdown = models.TextField()
    content_markup = models.TextField(editable=False)
    published = models.DateTimeField(auto_now_add=True)

    # Drafts are only visible to their author.
    draft = models.BooleanField(default=False)

    author = models.ForeignKey(GaeDatastoreUser)

    class Meta:
        app_label = 'blog'
        ordering = ['-published']

    def save(self):
        self.content_markup = markdown.markdown(self.content_markdown)
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse('post', args=[self.slug,])

    def __unicode__(self):
        return "%s" % (self.title,)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __unicode__(self):
        return self.name


class TaggedPost(models.Model):
    """Relationship between a tag and a post."""

    tag = models.ForeignKey(Tag, related_name='items')
    post = models.ForeignKey(Post)
    
    def __unicode__(self):
        return u'%s [%s]' % (self.object, self.tag)