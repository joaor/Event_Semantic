import urllib
import urllib2
import unicodedata
from xml.dom.minidom import parseString

event_list = []
artist_list = []
rdf_event_list = []
rdf_artist_list = []
radius = 130
coord = [(40.697299,-7.833252),(39.40224434029275, -8.118896484375),(38.71980474264237, -8.5693359375),(37.588119,-8.360596)]
license_key = 'b25b959554ed76058ac220b7b2e0a026'
get_url_event = lambda lt,lg,p: 'http://ws.audioscrobbler.com/2.0/?method=geo.getevents&lat=%f&long=%f&distance=%d&page=%d&api_key=%s' % (lt,lg,radius,p,license_key)
get_rdf_event = lambda idt: 'http://lastfm.rdfize.com/?eventID=%d&output=rdf-xml' % (idt)
get_rdf_artist = lambda artist: 'http://lastfm.rdfize.com/?username=&eventID=&artistName=%s&venueID=&output=rdf-xml' % (artist)

def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def get_ids(lt,lg,pages):
	l = []
	url = get_url_event(lt,lg,pages)
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	html = response.read()
	xml = parseString(html)	
	for event in xml.getElementsByTagName("event"):	
		l.append(int(getText(event.getElementsByTagName("id")[0].childNodes)))	
	if pages==1:	
		return (l,int(xml.getElementsByTagName("events")[0].getAttribute("totalpages")))
	return (l,0)

if __name__ == '__main__':   	
	for (lat,lng) in coord: 	
		l,total_pages = get_ids(lat,lng,1)	
		event_list += l 	
		for page in range(2,total_pages+1):	
			event_list += get_ids(lat,lng,page)[0]

	for idt in event_list:
		url = get_rdf_event(idt)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		html = response.read()
		rdf_event_list.append(html)

		xml = parseString(html)		
		descriptions = xml.getElementsByTagName("rdf:RDF")[0]
		for description in descriptions.getElementsByTagName("rdf:Description"):
			if description.getAttribute("rdf:about")[:33] == "http://lastfm.rdfize.com/artists/":
				artist = strip_accents(getText(description.getElementsByTagName("rdfs:label")[0].childNodes))
				if artist not in artist_list: 
					artist_list.append(artist)
				
	for artist in artist_list:
		try:
			url = get_rdf_artist(artist)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			html = response.read()
			rdf_artist_list.append(html)
		except:
			continue
	
	for i in range(len(rdf_event_list)):
		f = open('/Users/joaorodrigues/Desktop/Events/event%i.rdf' % (i+1), 'w')	
		f.write(rdf_event_list[i])
		f.close()
	
	for i in range(len(rdf_artist_list)):
		f = open('/Users/joaorodrigues/Desktop/Artists/artist%i.rdf' % (i+1), 'w')	
		f.write(rdf_artist_list[i])
		f.close()
		
		
		
		
		
		
		
		
		
		
		
		
