from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',

	url(r'^$', 'home', name="home"),
	url(r'^contact/$', 'contact', name="contact"),
	url(r'^events/$', 'events', name="events"),
	url(r'^artist/(?P<artist_id>.+)/$', 'artist_detail', name="artist-detail"),
	url(r'^event/(?P<event_id>.+)/$', 'event_detail', name="event-detail"),
	url(r'^genre/(?P<genre_id>.+)/$', 'event_genre', name="genre"),
	url(r'^date/(?P<date_id>.+)/$', 'event_date', name="date"),
	url(r'^zone/(?P<zone_id>.+)/$', 'event_zone', name="zone"),
)