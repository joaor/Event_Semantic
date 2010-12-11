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

obj_dic = {'Performer': ('performed_by','?art',Artist),'Date' : ('starts_at','?d',Date) , 'Event': ('','?ev',Event), 'Place': ('takes_place','?p',Place)}

# Helper
def render(request, template, opts = {}):
	return render_to_response(template, opts, context_instance=RequestContext(request))
    
def home(request):
	return render(request,'events/home.html')
	
def contact(request):
	return render(request,'events/contact.html')
	
def events(request):
	event_list = get_objects('Event', {} )
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
def artist_detail(request,artist_id):
	artist = Artist(ontologies['me'][artist_id])
	return render(request,'events/artist.html', {'artist' : artist})
	
def event_detail(request,event_id):
	event = Event(ontologies['me'][event_id])
	return render(request,'events/event.html', {'event' : event})

def event_genre(request,genre_id):
	f = 'FILTER (regex(?g, "^%s+?", "i"))' % genre_id
	event_list = get_objects('Event', {'Performer' : [('Genre','?g',f)] } )
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
def event_date(request,date_id):
	now = datetime.datetime.now()
	if date_id == 'past':
		timestp = int(time.time())
		f = 'FILTER (?t < %d)' % timestp
		event_list = get_objects('Event', {'Date' : [('Timestamp','?t',f)] } )
	elif date_id == 'week':
		week_number = now.isocalendar()[1]
		event_list = get_objects('Event', {'Date' : [('Year',str(now.year)),('WeekNumber',str(week_number))] } )
	elif date_id == 'this_month':	
		event_list = get_objects('Event', {'Date' : [('Year',str(now.year)),('MonthNumber',str(now.month))] } )
	elif date_id == 'next_month':
		month = now.month + 1
		year = now.year
		if month == 13:
			month = 1
			year += 1
		event_list = get_objects('Event', {'Date' : [('Year',str(year)),('MonthNumber',str(month))] } )
	elif date_id == 'year':
		event_list = get_objects('Event', {'Date' : [('Year',str(now.year))] } )
	return render(request,'events/event_list.html', {'event_list' : event_list})

def event_zone(request,zone_id):
	lat_north = 41
	lat_south = 39
	if zone_id == 'north':
		lat_filter = 'FILTER (?l > %d)' % lat_north
	elif zone_id == 'center':
		lat_filter = 'FILTER (?l < %d && ?l > %d)' %  (lat_north,lat_south)
	elif zone_id == 'south':
		lat_filter = 'FILTER (?l < %d)' % lat_south
	event_list = get_objects('Event', {'Place' : [('Lat','?l',lat_filter)] } )
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
def get_objects(tp,dic):
	l = []
	q = ['%s rdf:type me:%s' % (obj_dic[tp][1],tp)]
	for k in dic.keys():
		if k != tp:
			q.append('%s me:%s %s' % (obj_dic[tp][1],obj_dic[k][0],obj_dic[k][1]) )
			q.append('%s rdf:type me:%s' % (obj_dic[k][1],k) )	
		for i in dic[k]:
			q.append('%s me:%s %s' % (obj_dic[k][1],i[0],i[1]))
			if len(i) == 3: #Filter
				q.append(i[2])
	s = " . ".join(q)
	qy = """ SELECT %s WHERE { %s . } """ % (obj_dic[tp][1],s)
	print qy
	for inst in graph.query(qy):
		l.append(obj_dic[tp][2](inst))
	return l

def event_search(request):
	event_list = []
	d = {'artist':(['Performer','Name','?an'],[]),'event':(['Event','Name','?en'],[]),'day':(['Date','DayNumber','?dn'],[]),'month':(['Date','MonthName','?mn'],[]),'year':(['Date','Year','?y'],[]),'hour':(['Date','Hour','?h'],[]),'locality':(['Place','Locality','?lo'],[]),'genre':(['Performer','Genre','?g'],[])}
	ambiguous = []
	l = []
	words = request.GET['search_words'].split()
	for word in words:
		if l:
			if l[0] in d.keys():
				d[l[0]][1].append(word)
				l.pop()
			elif word in d.keys():
				d[word][1].append(l[0])
				l.pop()
			else:
				ambiguous.append(l.pop())
				l.append(word)
		else:
			l.append(word)
	if l:
		ambiguous.append(l.pop())	
	query_dic = {}
	for i in d.keys():
		if d[i][1]:
			if i in ['day','year','hour']:
				prop = (d[i][0][1],d[i][1][0])
			else:
				f = 'FILTER (regex(%s, "^%s+?", "i"))' % (d[i][0][2],d[i][1][0])
				prop = (d[i][0][1],d[i][0][2],f)
				
			if d[i][0][0] in query_dic.keys():
				query_dic[d[i][0][0]].append(prop)
			else:
				query_dic[d[i][0][0]] = [prop]
				
				
	print query_dic
	event_list = get_objects('Event', query_dic )
	print d
	print ambiguous
	#TODO: artist: lady gaga,joana ; hour: 5 artist
	return render(request,'events/event_list.html', {'event_list' : event_list})
	
		


	
	
	