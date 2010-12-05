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
		#print dir(ev)
		for e in graph.query(""" SELECT ?nm WHERE { ?ev me:Name ?nm . } """, initBindings={'ev': ev}):
			print e
		for e in graph.query(""" SELECT ?nm WHERE { ?ev me:Name ?nm . } """, initBindings={'ev': ev}):
			print e
		#event_list.append(graph.get(uri=i))
	#return render(request,'events/event_list.html', {'event_list' : event_list, 'graph' : graph})
	return render(request,'events/contact.html')