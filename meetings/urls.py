from django.conf.urls import patterns, url

from meetings import views

urlpatterns = patterns('',
    
    url(r'^(?P<meeting_id>\d+)/$', views.detail, name='detail'),
    url(r'^$', views.index, name='index'),
)
