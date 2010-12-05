from django_rdf import graph
from events.semantic import ontologies


class RDFObject(object):
	"""docstring for RDFObject"""
	def __init__(self, uri):
		super(RDFObject, self).__init__()
		self.uri = uri
		self.id = str(uri)[46:]
		
	def get_name(self):
		name = self.simple_query("Name",str)
		if not name:
			return self.id.replace('+',' ')
		return name

	def get_description(self):
		return self.simple_query("Description",str)
			
	def simple_query(self,prop,func):
		for p in graph.query(""" SELECT ?prop WHERE { ?inst me:%s ?prop . } """ % prop, initBindings={'inst': self.uri}):
			return func(p) 

	def __str__(self):
		return self.get_name()

class Event(RDFObject):
	def get_date(self):
		return self.simple_query("Date",str)
	
	def get_place(self):
		return self.simple_query("takes_place",Place)
			
	def get_artists(self):
		return map(lambda a: Artist(a), graph.query(""" SELECT ?art WHERE { ?ev me:performed_by ?art . } """, initBindings={'ev': self.uri}))
	
	def get_main_artist(self):
		return self.simple_query("performed_by",Artist)
		
	def has_more_artists(self):
		return len(graph.query(""" SELECT ?art WHERE { ?ev me:performed_by ?art . } """, initBindings={'ev': self.uri})) > 1
		
class Artist(RDFObject):
	pass

class Place(RDFObject):
	pass