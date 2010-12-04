from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',

	url(r'^$', 'home', name="home"),
	url(r'^contact/$', 'contact', name="contact"),
)