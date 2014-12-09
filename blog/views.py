from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
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
    model = Post

    def get(self, request):
        posts = self.model.objects.filter(draft=False)
        return render(request, self.template_name, {
            'posts': posts
        })


class PostView(View):
    template_name = 'blog/post.html'
    model = Post

    def get(self, request, slug):
        post = get_object_or_404(self.model, slug=slug)
        return render(request, self.template_name, {
            'post': post
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
        form = self.form_class(request=request, instance=post,label_suffix='')
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = self.form_class(request.POST, instance=post, request=request, label_suffix='')
        if form.is_valid():
            newpost = form.save()
            return HttpResponseRedirect(reverse('post', args=[newpost.slug,]))
        return render(request, self.template_name, {
            'form': form
        })


class PostDeleteView(LoginRequiredMixin, View):

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        return HttpResponseRedirect(reverse('index'))


def logout_redirect(request):
    return HttpResponseRedirect(
        users.create_logout_url(dest_url=request.GET.get('next'))
    )
