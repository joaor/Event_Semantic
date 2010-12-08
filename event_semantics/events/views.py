from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.conf import settings

from django_rdf import graph
from events.semantic import ontologies

from events.get_rdf import *

# Helper
def render(request, template, opts = {}):
	return render_to_response(template, opts, context_instance=RequestContext(request))
    
def home(request):
	return render(request,'events/home.html')
	
def contact(request):
	return render(request,'events/contact.html')
	
def events(request):
	event_list = []
	for ev in graph.query(""" SELECT ?event WHERE { ?event rdf:type me:Event . } """):
		event_list.append(Event(ev))
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
def artist_detail(request,artist_id):
	artist = Artist(ontologies['me'][artist_id])
	return render(request,'events/artist.html', {'artist' : artist})
	
def event_detail(request,event_id):
	event = Event(ontologies['me'][event_id])
	return render(request,'events/event.html', {'event' : event})

def genre(request,genre_id):
	artist_list = []
	event_list = []
	for pf in graph.query(""" SELECT ?art WHERE { ?art rdf:type me:Performer . ?art me:Genre ?g . FILTER (regex(?g, "^%s+?", "i")) } """ % genre_id):
		artist_list.append(Artist(pf))
	for pf in artist_list:
		event_list += pf.get_event_list()
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
def event_date(request,date_id):
	now = datetime.datetime.now()
	if date_id == 'past':
		pass
	elif date_id == 'week':
		week_number = now.isocalendar()[1]
		event_list = []
		for dt in graph.query(""" SELECT ?d WHERE { ?d rdf:type me:Date . ?d me:WeekNumber %d . } """ % week_number ):
			for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:starts_at ?d . } """, initBindings={'d': dt} ):
				event_list.append(Event(ev))
	elif date_id == 'this_month':
		pass
	elif date_id == 'next_month':
		pass
	elif date_id == 'year':
		pass
	else:
		return render(request,'events/home.html')
	return render(request,'events/event_list.html', {'event_list' : event_list})

	
	
	