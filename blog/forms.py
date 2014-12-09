from django import forms
from blog.models import Post, Tag


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
        self.fields['author'].label = ''
        if self.request:
            self.fields['author'].initial = self.request.user.pk

    def save(self, *args, **kwargs):
        post = super(PostForm, self).save(*args, **kwargs)

        # Create tags if necessary and assign them to posts.
        # TODO: Investigate if it's possible to use bulk_create
        # instead of a loop.
        taglist = self.cleaned_data['tags']
        for tag in taglist:
            tag_obj, _ = Tag.objects.get_or_create(name=tag)
            post.tagobjs.add(tag_obj)
            post.save()

        return post