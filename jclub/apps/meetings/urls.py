from django.conf.urls import patterns, url

from jclub.apps.meetings import views

from django.contrib import admin
from django_tequila.admin import TequilaAdminSite

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^meetings/(?P<meeting_id>\d+)/$', views.detail, name='meetings_detail'),
    url(r'^meetings/$', views.meetings_index, name='meetings_index'),
    url(r'^$', views.index, name='index'),

    # presenters implied model
    url(r'^presenters/$', views.presenters_index, name='presenters_index'),
    url(r'^presenters/(?P<user_id>\d+)/$', views.presenters_detail, name='presenters_detail'),
)
