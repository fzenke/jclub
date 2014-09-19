from django.conf.urls import patterns, url
from jclub.apps.meetings import views

urlpatterns = patterns('',
	# landing page
    url(r'^$', views.index, name='index'),

    # calendar feed
    url(r'^calendar$', views.calendar_index, name='calendar_index'),
    url(r'^calendar.ics$', views.calendar_ics, name='calendar_ics'),

    # meetings
    url(r'^meetings/(?P<meeting_id>\d+)/$', views.detail, name='meetings_detail'),
    url(r'^meetings/$', views.meetings_index, name='meetings_index'),    
    
    # presenters implied model
    url(r'^presenters/$', views.presenters_index, name='presenters_index'),
    url(r'^presenters/(?P<user_id>\d+)/$', views.presenters_detail, name='presenters_detail'),
)
