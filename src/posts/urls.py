from django.conf.urls import url
from django.contrib import admin

#from .views import (
#	post_list,
#	post_create,
#	post_detail,
#	post_update,
#	post_delete,
#	)
from .views import *
urlpatterns = [
    url(r'^$', post_list, name='home'),
    url(r'^blog/$', post_list, name='list'),
    url(r'^blog/create/$', post_create),
    url(r'^blog/(\d{4,4})/$', yearview),
    url(r'^blog/(\d{4,4})/(\d{2,2})/$', monthview),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',post_detail,name='detail'),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/edit/$', post_update, name='update'),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/delete/$', post_delete, name='delete'),
    url(r'^like-blog/$', like_count_blog, name='like_count_blog'),
    url(r'^blog/archive/(\d{4,4})/$', yearview),
    url(r'^blog/archive/(\d{4,4})/(\d{2,2})/$', monthview),
    url(r'^blog/tag/([\w\-]+)/$', tagview),

]
