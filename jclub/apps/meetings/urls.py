from django.conf.urls import patterns, url

from jclub.apps.meetings import views

urlpatterns = patterns('',
    url(r'^meetings/(?P<meeting_id>\d+)/$', views.detail, name='meetings_detail'),
    url(r'^meetings/$', views.meetings_index, name='meetings_index'),
    url(r'^$', views.index, name='index'),
)
