import os
import unicodedata
import urllib
import urllib2
from xml.dom.minidom import parseString

i = 1
folder = '/Users/joaorodrigues/Documents/5_ano/ws/Projecto/Projecto_WS/Scripts/events/'
license_key = 'b25b959554ed76058ac220b7b2e0a026'
get_artist_info = lambda artist: 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=%s&api_key=%s' % (artist,license_key)
get_artist_albuns = lambda artist: 'http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=%s&api_key=%s' % (artist,license_key)

artist_list = []

def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

if __name__ == '__main__': 
	for filename in os.listdir(folder)[1:]:
		f = open("%s/%s" % (folder,filename), 'r')
		rdf = ''
		for line in f:
			rdf +=line
		xml = parseString(rdf)		
		descriptions = xml.getElementsByTagName("rdf:RDF")[0]
		for description in descriptions.getElementsByTagName("rdf:Description"):
			if description.getAttribute("rdf:about")[:33] == "http://lastfm.rdfize.com/artists/":
				artist = strip_accents(getText(description.getElementsByTagName("rdfs:label")[0].childNodes)).replace(' ','+')
				if artist not in artist_list: 
					artist_list.append(artist)
					try:
						url = get_artist_info(artist)
						req = urllib2.Request(url)
						response = urllib2.urlopen(req)
						xml = response.read()
						f = open('/Users/joaorodrigues/Desktop/artists/artist%i.xml' % (i), 'w')	
						f.write(xml)
						f.close()							
					except:
						break					
					try:
						url = get_artist_albuns(artist)
						req = urllib2.Request(url)
						response = urllib2.urlopen(req)
						xml = response.read()							
					except:
						break		
					alb = parseString(xml)		
					lfm = alb.getElementsByTagName("lfm")[0]
					topalbums = lfm.getElementsByTagName("topalbums")[0]
					jso = {'Artist':{}}
					jso['Artist']['Name'] = artist
					jso['Artist']['Albums'] = {}
					for album in topalbums.getElementsByTagName("album"):
						album_name = getText(album.getElementsByTagName("name")[0].childNodes)
						album_url = getText(album.getElementsByTagName("url")[0].childNodes)
						try:
							req = urllib2.Request(album_url)
							response = urllib2.urlopen(req)
							html = response.read().replace('\"','\'')
							ind1 = html.index("<span class='albumLabel'>")
							html = html[ind1:]
							ind2 = html.index("</span>")
							html = html[:ind2+7]
							xml = parseString(html)
							label = getText(xml.getElementsByTagName("span")[0].getElementsByTagName("a")[0].childNodes)
							jso['Artist']['Albums'][album_name] = label	
						except:
							continue
					print i
					print artist
					print jso
					f = open('/Users/joaorodrigues/Desktop/albums/albums%i.json' % (i), 'w')	
					f.write("%s" % (str(jso)))
					f.close()
					i += 1
					break 
				


				
















