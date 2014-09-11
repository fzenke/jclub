from django.conf.urls import patterns, url

from meetings import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
