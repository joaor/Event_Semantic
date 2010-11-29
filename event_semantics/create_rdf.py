from datetime import datetime, timedelta
from rdflib import Namespace, Literal, URIRef

import settings, os, unicodedata, re
from django.core.management import setup_environ
setup_environ(settings)
from django_rdf import graph

from events.semantic import ontologies
from xml.dom.minidom import parseString
from pprint import pprint

def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

place_list = []
artist_list = []
events_folder = '/Users/joaorodrigues/Documents/5_ano/ws/Projecto/Projecto_WS/Data/events/'
artists_folder = '/Users/joaorodrigues/Documents/5_ano/ws/Projecto/Projecto_WS/Data/artists/'
albums_folder = '/Users/joaorodrigues/Documents/5_ano/ws/Projecto/Projecto_WS/Data/albums/'
repeat = False
album_number = 1

for filename in os.listdir(events_folder)[1:]:
	f = open("%s/%s" % (events_folder,filename), 'r')
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
					repeat = True
			else:		
				if not repeat:
					address = getText(description.getElementsByTagName("v:street-address")[0].childNodes)
					graph.add((place,ontologies['me']['Address'],Literal(address)))
					locality = getText(description.getElementsByTagName("v:locality")[0].childNodes)
					graph.add((place,ontologies['me']['Locality'],Literal(locality)))
					country = getText(description.getElementsByTagName("v:country-name")[0].childNodes)
					graph.add((place,ontologies['me']['Country'],Literal(country)))
					postal = getText(description.getElementsByTagName("v:postal-code")[0].childNodes)
					graph.add((place,ontologies['me']['Postal'],Literal(postal)))
					graph.add((event,ontologies['me']['takes_place'],place))
				else:
					repeat = False
		elif description.getAttribute("rdf:about")[:33] == "http://lastfm.rdfize.com/artists/":
			try:
				artist_id = str(strip_accents(getText(description.getElementsByTagName("rdfs:label")[0].childNodes)).replace(' ','+'))
				artist = ontologies['me'][artist_id]
				artist_list.append(artist)
				graph.add((artist,ontologies['rdf']['type'],ontologies['me']['Performer']))
				graph.add((event,ontologies['me']['performed_by'],artist))
			except:
				pass
			
for filename in os.listdir(artists_folder)[1:]:
	f = open("%s/%s" % (artists_folder,filename), 'r')
	rdf = ''
	for line in f:
		rdf +=line
	i = rdf.index('<summary>')
	j = rdf.index('</summary>')
	summary = rdf[i+9:j]
	summary = summary.replace("]]>",'')
	summary = summary.replace("<![CDATA[",'')
	summary = re.sub("<.*?>.*?</.*?>",'', summary)
	rdf = rdf[:i+9] + summary + rdf[j:]
	i = rdf.index('<content>')
	j = rdf.index('</content>')
	content = rdf[i+9:j]
	content = content.replace("]]>",'')
	content = content.replace("<![CDATA[",'')
	content = re.sub("<.*?>.*?</.*?>",'', content)
	content = re.sub("</.*?>",'', content)
	rdf = rdf[:i+9] + content + rdf[j:]
	xml = parseString(rdf)
	lfm = xml.getElementsByTagName("lfm")[0]
	art = lfm.getElementsByTagName("artist")[0]
	artist_name = getText(art.getElementsByTagName("name")[0].childNodes).replace('\"','\'')
	artist_id = str(strip_accents(artist_name).replace(' ','+'))
	artist = ontologies['me'][artist_id]
	if artist in artist_list:
		graph.add((artist,ontologies['me']['Name'],Literal(artist_name)))
		tags = art.getElementsByTagName("tags")[0]
		for tag in tags.getElementsByTagName("tag"):
			artist_genre = getText(tag.getElementsByTagName("name")[0].childNodes)
			graph.add((artist,ontologies['me']['Genre'],Literal(artist_genre)))
		bio = art.getElementsByTagName("bio")[0]
		summary = getText(bio.getElementsByTagName("summary")[0].childNodes)
		graph.add((artist,ontologies['me']['Summary'],Literal(summary)))
		description = getText(bio.getElementsByTagName("content")[0].childNodes)
		graph.add((artist,ontologies['me']['Description'],Literal(description)))

for filename in os.listdir(albums_folder)[1:]:
	f = open("%s/%s" % (albums_folder,filename), 'r')
	jso = ''
	for line in f:
		jso +=line
	info = eval(jso)
	artist_id = str(info['Artist']['Name'])
	artist = ontologies['me'][artist_id]
	if artist in artist_list:
		for alb in info['Artist']['Albums'].keys():
			try:
				album = ontologies['me'][str(album_number)] 
				graph.add((album,ontologies['rdf']['type'],ontologies['me']['Album']))
				album_name = str(alb)
				graph.add((album,ontologies['me']['Name'],Literal(album_name)))
				album_label = str(info['Artist']['Albums'][alb])
				graph.add((album,ontologies['me']['Label'],Literal(album_label)))
				graph.add((artist,ontologies['me']['recorded'],album))
				album_number += 1
			except:
				continue
		
pprint(list(graph))


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
