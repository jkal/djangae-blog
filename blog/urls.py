from django.conf.urls import patterns, include, url
from blog.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', logout_redirect, name='logout'),
    url(r'^posts/add/$', PostAddView.as_view(), name='post-add'),
    url(r'^posts/(?P<slug>[\w-]+)/$', PostView.as_view(), name='post'),
    url(r'^posts/(?P<slug>[\w-]+)/delete/$', PostDeleteView.as_view(), name='post-delete'),
    url(r'^posts/(?P<slug>[\w-]+)/edit/$', PostEditView.as_view(), name='post-edit'),
    url(r'^tags/$', TagIndexView.as_view(), name='tag-index'),
    url(r'^tag/(?P<name>[\w-]+)/$', TagView.as_view(), name='tag'),
    url(r'^search/$', SearchView.as_view(), name='search'),
)