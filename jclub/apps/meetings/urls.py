from django.conf.urls import patterns, url

from jclub.apps.meetings import views

urlpatterns = patterns('',
    
    url(r'^(?P<meeting_id>\d+)/$', views.detail, name='detail'),
    url(r'^$', views.meetings_index, name='meetings_index'),
)
