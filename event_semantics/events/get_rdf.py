from django_rdf import graph
from events.semantic import ontologies


class RDFObject(object):
	def __init__(self, uri):
		super(RDFObject, self).__init__()
		self.uri = uri
		self.id = unicode(self.uri)[46:]
		
	def get_name(self):
		name = self.single_query("Name",unicode)
		if not name:
			return self.id.replace('+',' ')
		return name

	def get_description(self):
		try:
			desc = self.single_query("Description",unicode)
		except:
			return u'No description avaiable'
		return desc
			
	def single_query(self,prop,func):
		for p in graph.query(""" SELECT ?prop WHERE { ?inst me:%s ?prop . } """ % prop, initBindings={'inst': self.uri}):
			return func(p)
	
	def multiple_query(self,prop,func):
		return map(lambda a: func(a), graph.query(""" SELECT ?art WHERE { ?ev me:%s ?art . } """ % prop, initBindings={'ev': self.uri}))

	def inverse_multiple_query(self,prop,func):
		return map(lambda a: func(a), graph.query(""" SELECT ?ev WHERE { ?ev me:%s ?art . } """ % prop, initBindings={'art': self.uri}))

	def __str__(self):
		return self.get_name()

class Event(RDFObject):
	def get_name(self):
		return u'%s @ %s' % (super(Event,self).get_name(),self.get_place().get_name())
			
	def get_date(self):
		return self.single_query("Date",unicode)
	
	def get_place(self):
		return self.single_query("takes_place",Place)
			
	def get_artists(self):
		return self.multiple_query("performed_by",Artist)
	
	def get_main_artist(self):
		return self.single_query("performed_by",Artist)
		
	def has_more_artists(self):
		return len(graph.query(""" SELECT ?art WHERE { ?ev me:performed_by ?art . } """, initBindings={'ev': self.uri})) > 1
		
class Artist(RDFObject):
	def get_genre_list(self):
		return u', '.join(self.multiple_query("Genre",unicode))

	def get_album_list(self):
		return u', '.join(map(lambda a: a.get_name(), self.multiple_query("recorded",Album)))

	def get_event_list(self):
		return self.inverse_multiple_query("performed_by",Event)
		
	def get_summary(self):
		return self.single_query("Summary",unicode)

class Place(RDFObject):
	def get_address(self):
		return self.single_query("Address",unicode)
		
	def get_postal(self):
		return self.single_query("Postal",unicode)
		
	def get_locality(self):
		return self.single_query("Locality",unicode)
		
	def get_country(self):
		return self.single_query("Country",unicode)
		
	def get_complete_address(self):
		return u'%s, %s %s, %s' % (self.get_address(),self.get_postal(),self.get_locality(),self.get_country())

class Album(RDFObject):
	pass