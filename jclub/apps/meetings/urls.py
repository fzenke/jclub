from django.conf.urls import patterns, url

from jclub.apps.meetings import views

urlpatterns = patterns('',
    url(r'^meetings/(?P<meeting_id>\d+)/$', views.detail, name='detail'),
    url(r'^meetings/$', views.meetings_index, name='meetings_index'),
    url(r'^$', views.index, name='index'),

    # presenters implied model
    url(r'^presenters/(?P<user_id>\d+)/$', views.presenters_detail, name='presenters_detail'),
)
