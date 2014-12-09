from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView, DeleteView, CreateView
from session_csrf import anonymous_csrf
from google.appengine.api import users
from blog.models import Post
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
        post = self.model.objects.get(slug=slug)
        return render(request, self.template_name, {
            'post': post
        })


class PostAddView(LoginRequiredMixin, View):
    template_name = 'blog/add.html'
    form_class = PostForm
    success_url = '/thanks/'

    def get(self, request):
        form = self.form_class(label_suffix='')
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.author = request.user
            newform.save()
            return HttpResponseRedirect(reverse('index'))

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
