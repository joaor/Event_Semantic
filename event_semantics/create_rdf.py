from datetime import datetime, timedelta
from rdflib import Namespace, Literal, URIRef

import settings, os
from django.core.management import setup_environ
setup_environ(settings)
from django_rdf import graph

from events.semantic import ontologies
from xml.dom.minidom import parseString

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

place_list = []
folder = '/Users/joaorodrigues/Documents/5_ano/ws/Projecto/Projecto_WS/Data/events/'

for filename in os.listdir(folder)[1:]:
	f = open("%s/%s" % (folder,filename), 'r')
	rdf = ''
	for line in f:
		rdf +=line
	xml = parseString(rdf)
	descriptions = xml.getElementsByTagName("rdf:RDF")[0]
	for description in descriptions.getElementsByTagName("rdf:Description"):
		if description.getAttribute("rdf:about")[:32] == "http://lastfm.rdfize.com/events/":
			event_id = description.getAttribute("rdf:about")[32:]
			event = ontologies['me'][event_id]	
			graph.add((event,ontologies['rdf']['type'],ontologies['me']['Event'])) 		
			event_name = getText(description.getElementsByTagName("rdfs:label")[0].childNodes).replace('\"',' ')
			graph.add((event,ontologies['me']['Name'],Literal(event_name)))
			event_date = getText(description.getElementsByTagName("terms:date")[0].childNodes)
			graph.add((event,ontologies['me']['Date'],Literal(event_date)))
			d = description.getElementsByTagName("terms:description")
			if len(d):
				event_description = getText(d[0].childNodes)
				graph.add((event,ontologies['me']['Description'],Literal(event_description)))
		elif description.getAttribute("rdf:about")[:32] == "http://lastfm.rdfize.com/venues/":
			if description.getAttribute("rdf:about")[-7:] != 'address':
				place_id = description.getAttribute("rdf:about")[32:]
				place = ontologies['me'][place_id]
				if place not in place_list:
					place_list.append(place)			
					graph.add((place,ontologies['rdf']['type'],ontologies['me']['Place']))
					place_name = getText(description.getElementsByTagName("rdfs:label")[0].childNodes)
					graph.add((place,ontologies['me']['Name'],Literal(place_name)))
					lat = getText(description.getElementsByTagName("geo:lat")[0].childNodes)
					graph.add((place,ontologies['me']['Lat'],Literal(float(lat))))
					lng = getText(description.getElementsByTagName("geo:long")[0].childNodes)
					graph.add((place,ontologies['me']['Long'],Literal(float(lng))))
				else:
					graph.add((event,ontologies['me']['takes_place'],place))
					break
			else:		
				address = getText(description.getElementsByTagName("v:street-address")[0].childNodes)
				graph.add((place,ontologies['me']['Address'],Literal(address)))
				locality = getText(description.getElementsByTagName("v:locality")[0].childNodes)
				graph.add((place,ontologies['me']['Locality'],Literal(locality)))
				country = getText(description.getElementsByTagName("v:country-name")[0].childNodes)
				graph.add((place,ontologies['me']['Country'],Literal(country)))
				postal = getText(description.getElementsByTagName("v:postal-code")[0].childNodes)
				graph.add((place,ontologies['me']['Postal'],Literal(postal)))
				graph.add((event,ontologies['me']['takes_place'],place))
				break
				
#graph.add((ontologies['me']['artist1'],ontologies['rdf']['type'],ontologies['me']['Artist']))
#graph.add((ontologies['me']['artist1'],ontologies['me']['Description'],Literal('ola, sou o artista1')))

#graph.add((ontologies['me']['event1'],ontologies['me']['performed_by'],ontologies['me']['artist1']))

#from pprint import pprint
#pprint(list(graph))


# just think .whatever((s, p, o))
# here we report on what we know

#pprint(list(graph.subjects()))
#pprint(list(graph.predicates()))
#pprint(list(graph.objects()))

# and other things that make sense

# what do we know about pat?
#pprint(list(graph.predicate_objects(ontologies['me']['event1'])))

# who is what age?
#pprint(list(graph.subject_objects(ontologies['me']['description'])))	

print list(graph.query(""" SELECT ?cenas WHERE { ?cenas me:takes_place ?a . ?a me:Name "MusicBox" . } """, initNs=ontologies))

#graph.commit()
