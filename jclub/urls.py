from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jclub.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('jclub.apps.meetings.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

#from django_tequila.admin import TequilaAdminSite
#from django_tequila.urls import urlpatterns as django_tequila_urlpatterns
#urlpatterns += django_tequila_urlpatterns
#admin.site.__class__ = TequilaAdminSite
