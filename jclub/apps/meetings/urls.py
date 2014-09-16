from django.conf.urls import patterns, url

from jclub.apps.meetings import views

urlpatterns = patterns('',
    
    url(r'^meetings/(?P<meeting_id>\d+)/$', views.detail, name='detail'),
    url(r'^$', views.index, name='jclub_index'),
)
