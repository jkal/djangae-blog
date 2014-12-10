from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from session_csrf import anonymous_csrf
from google.appengine.api import users
from blog.models import Post, Tag
from blog.forms import PostForm


class LoginRequiredMixin(object):
    """ 
    Wrapper around the `login_required` decorater for use with class based views.
    """
    redirect_field_name = REDIRECT_FIELD_NAME
    login_url = None

    @method_decorator(login_required(redirect_field_name=redirect_field_name, login_url=login_url))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class IndexView(View):
    template_name = 'blog/index.html'

    def get(self, request):
        posts = Post.objects.filter(draft=False)
        drafts = []
        if request.user.is_authenticated():
            drafts = Post.objects.filter(draft=True, author=request.user)
        return render(request, self.template_name, {
            'posts': posts,
            'drafts': drafts
        })


class PostView(View):
    template_name = 'blog/post.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        show_edit = False
        if request.user.is_authenticated() and post.author == request.user:
            show_edit = True
        return render(request, self.template_name, {
            'post': post,
            'show_edit': show_edit
        })


class TagView(View):
    template_name = 'blog/tag.html'

    def get(self, request, name):
        tag = get_object_or_404(Tag, name=name)
        posts = tag.post_set.all()
        return render(request, self.template_name, {
            'tag': tag,
            'posts': posts
        })


class TagIndexView(View):
    template_name = 'blog/tag_index.html'

    def get(self, request):
        tags = Tag.objects.all()
        return render(request, self.template_name, {
            'tags': tags,
        })


class PostAddView(LoginRequiredMixin, View):
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def get(self, request):
        form = self.form_class(request=request, label_suffix='')
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = self.form_class(request.POST, request=request, label_suffix='')
        if form.is_valid():
            newpost = form.save()
            return HttpResponseRedirect(reverse('post', args=[newpost.slug,]))

        return render(request, self.template_name, {
            'form': form
        })

class PostEditView(LoginRequiredMixin, View):
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.author != request.user:
            raise PermissionDenied

        form = self.form_class(request=request, instance=post,label_suffix='')
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = self.form_class(request.POST, instance=post, request=request, label_suffix='')
        if post.author != request.user:
            raise PermissionDenied

        if form.is_valid():
            newpost = form.save()
            return HttpResponseRedirect(reverse('post', args=[newpost.slug,]))
        return render(request, self.template_name, {
            'form': form
        })


class PostDeleteView(LoginRequiredMixin, View):

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        if self.post.author != request.user:
            raise PermissionDenied
        post.delete()
        return HttpResponseRedirect(reverse('index'))


def logout_redirect(request):
    return HttpResponseRedirect(
        users.create_logout_url(dest_url=request.GET.get('next'))
    )
