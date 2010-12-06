from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',

	url(r'^$', 'home', name="home"),
	url(r'^contact/$', 'contact', name="contact"),
	url(r'^events/$', 'events', name="events"),
	url(r'^artist/(?P<artist_id>.+)/$', 'artist_detail', name="artist-detail"),
	url(r'^event/(?P<event_id>.+)/$', 'event_detail', name="event-detail"),
)