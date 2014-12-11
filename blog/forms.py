from django import forms
from blog.models import Post, Tag
from blog.search import index


class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass


class PostForm(forms.ModelForm):

    tags = MultipleChoiceFieldNoValidation(
        widget=forms.SelectMultiple(attrs={
            'data-role': 'tagsinput'
        }),
        required=False
    )

    class Meta:
        model = Post
        fields = ('title', 'slug', 'content_markdown', 'draft', 'tags', 'author')

        labels = {
            'title': 'Title',
            'slug': 'URL',
            'content_markdown': 'Content'
        }

        help_texts = {
            'slug': 'This is a unique identifier for your post.',
            'content_markdown': 'Markdown is supported.',
            'draft': 'Drafts are only visible to their authors.',
            'tags': 'Type a tag and press Enter.'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['author'].initial = self.request.user.pk
        self.label_suffix = ''

        # When editing a post, prepopulate the tags field with the tags
        # assigned to the post.
        if self.instance and self.instance.id:
            tags = self.instance.tagobjs.all()
            self.fields['tags'].choices = [(x.name, x.name) for x in tags]

    def save(self, *args, **kwargs):
        post = super(PostForm, self).save(*args, **kwargs)

        # Create tags if necessary and assign them to posts.
        # TODO: Investigate if it's possible to use bulk queries
        # instead of a loop.
        taglist = self.cleaned_data['tags']
        post.tagobjs.clear()
        for tag in taglist:
            tag_obj, _ = Tag.objects.get_or_create(name=tag)
            post.tagobjs.add(tag_obj)
            post.save()

        index.put(post)

        return post