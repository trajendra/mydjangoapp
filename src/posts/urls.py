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
	url(r'^$', post_list, name='list'),
    url(r'^post/create/$', post_create),
    url(r'^post/(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^post/(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
	#url(r'^myview1/$', myview1),
    #url(r'^blog/blog/$', frontpage),
    #url(r'^blog/(\d{4,4})/(\d{2,2})/([\w\-]+)/$', singlepost),
    url(r'^archive/(\d{4,4})/$', yearview),
    url(r'^archive/(\d{4,4})/(\d{2,2})/$', monthview),
    url(r'^tag/([\w\-]+)/$', tagview),
	url(r'^about/', about, name='about'),
	url(r'^contact/', contact, name='contact'),
]
