from django import forms
from blog.models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'slug', 'content_markdown', 'draft')

        labels = {
            'title': 'Title',
            'slug': 'URL',
            'content_markdown': 'Content'
        }

        help_texts = {
            'slug': 'This is a unique identifier for your post.',
            'content_markdown': 'Markdown is supported.',
            'draft': 'Drafts are only visible to their authors.'
        }
