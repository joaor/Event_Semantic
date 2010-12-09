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

import time

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

def event_genre(request,genre_id):
	artist_list = []
	event_list = []
	for pf in graph.query(""" SELECT ?art WHERE { ?art rdf:type me:Performer . ?art me:Genre ?g . FILTER (regex(?g, "^%s+?", "i")) } """ % genre_id):
		artist_list.append(Artist(pf))
	for pf in artist_list:
		event_list += pf.get_event_list()
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
def event_date(request,date_id):
	event_list = []
	now = datetime.datetime.now()
	if date_id == 'past':
		timestp = int(time.time())
		for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:starts_at ?d . ?d rdf:type me:Date . ?d me:Timestamp ?t . FILTER (?t < %d) . } """ % timestp ):
			event_list.append(Event(ev))
	elif date_id == 'week':
		week_number = now.isocalendar()[1]
		event_list = get_events_by_date(now.year,'WeekNumber',week_number)
	elif date_id == 'this_month':	
		event_list = get_events_by_date(now.year,'MonthNumber',now.month)
	elif date_id == 'next_month':
		month = now.month + 1
		year = now.year
		if month == 13:
			month = 1
			year += 1
		event_list = get_events_by_date(year,'MonthNumber',month)
	elif date_id == 'year':
		event_list = get_events_by_date(now.year)
	return render(request,'events/event_list.html', {'event_list' : event_list})

def get_events_by_date(*args):
	event_list = []
	if len(args) == 1:
		for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:starts_at ?d . ?d rdf:type me:Date . ?d me:Year %d . } """ % args[0]):
			event_list.append(Event(ev))
	elif len(args) == 3:
		for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:starts_at ?d . ?d rdf:type me:Date . ?d me:Year %d . ?d me:%s %d . } """ % (args[0],args[1],args[2]) ):
			event_list.append(Event(ev))
	return event_list
			
def event_zone(request,zone_id):
	event_list = []
	lat_north = 41
	lat_south = 39
	if zone_id == 'north':
		for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:takes_place ?p . ?p rdf:type me:Place . ?p me:Lat ?l . FILTER (?l > %d) . } """ % lat_north ):
			event_list.append(Event(ev))
	elif zone_id == 'center':
		for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:takes_place ?p . ?p rdf:type me:Place . ?p me:Lat ?l . FILTER (?l < %d && ?l > %d) . } """ % (lat_north,lat_south) ):
			event_list.append(Event(ev))
	elif zone_id == 'south':
		for ev in graph.query(""" SELECT ?ev WHERE { ?ev rdf:type me:Event . ?ev me:takes_place ?p . ?p rdf:type me:Place . ?p me:Lat ?l . FILTER (?l < %d) . } """ % lat_south ):
			event_list.append(Event(ev))
	return render(request,'events/event_list.html', {'event_list' : event_list})

def event_search(request):
	event_list = []
	words = request.GET['search_words'].split()
	#TODO: semantic search
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
		


	
	
	