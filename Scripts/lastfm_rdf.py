import urllib
import urllib2
from xml.dom.minidom import parseString

id_list = []
rdf_list = []
radius = 130
license_key = 'b25b959554ed76058ac220b7b2e0a026'
coord = [(40.697299,-7.833252),(39.40224434029275, -8.118896484375),(38.71980474264237, -8.5693359375),(37.588119,-8.360596)]
get_url_ids = lambda lt,lg,p: 'http://ws.audioscrobbler.com/2.0/?method=geo.getevents&lat=%f&long=%f&distance=%d&page=%d&api_key=%s' % (lt,lg,radius,p,license_key)
get_url_rdf = lambda idt: 'http://lastfm.rdfize.com/?eventID=%d&output=rdf-xml' % (idt)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def get_ids(lt,lg,pages):
	l = []
	url = get_url_ids(lt,lg,pages)
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
		id_list += l
		for page in range(2,total_pages+1):
			id_list += get_ids(lat,lng,page)[0]
			
	for idt in id_list:
		url = get_url_rdf(idt)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		rdf_list.append(response.read())
