from django.conf.urls import url
from django.contrib import admin

from .views import *
urlpatterns = [
    url(r'^about/$', about_us, name='profile'),
    url(r'^profile/(?P<slug>[-\w]+)/$', profile_view, name='pview'),
    url(r'^profile/(?P<slug>[-\w]+)/update/$', profile_update, name='pupdate'),
    url(r'^profile/(?P<slug>[-\w]+)/delete/$', profile_delete, name='pdelete'),
]
