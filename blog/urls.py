from django.conf.urls import patterns, include, url
from blog.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', logout_redirect, name='logout'),
    url(r'^(?P<slug>[\w-]+)/$', PostView.as_view(), name='post'),
    url(r'^posts/add/$', PostAddView.as_view(), name='post-add'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteView.as_view(), name='post-delete'),
)