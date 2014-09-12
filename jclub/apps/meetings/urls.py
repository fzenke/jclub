from django.conf.urls import patterns, url

from jclub.apps.meetings import views

from django.contrib import admin
from django_tequila.admin import TequilaAdminSite

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^(?P<meeting_id>\d+)/$', views.detail, name='detail'),
    url(r'^$', views.index, name='jclub_index'),
)
