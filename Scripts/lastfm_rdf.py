import urllib
import urllib2
from xml.dom.minidom import parseString

id_list = []
rdf_list = []
country = 'portugal'
license_key = 'b25b959554ed76058ac220b7b2e0a026'
get_url_artist = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=%s&api_key=%s' % (country,license_key)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

if __name__ == '__main__':	
	l = []
	url = get_url_artist
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	html = response.read()
	xml = parseString(html)
	for artist in xml.getElementsByTagName("artist"):
		l.append(getText(artist.getElementsByTagName("name")[0].childNodes))
	print l
