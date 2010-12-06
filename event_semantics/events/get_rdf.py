from django_rdf import graph
from events.semantic import ontologies


class RDFObject(object):
	"""docstring for RDFObject"""
	def __init__(self, uri):
		super(RDFObject, self).__init__()
		self.uri = uri
		self.id = str(uri)[46:]
		
	def get_name(self):
		name = self.single_query("Name",str)
		if not name:
			return self.id.replace('+',' ')
		return name

	def get_description(self):
		return self.single_query("Description",str).replace('\\n','</br>')
			
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
	def get_date(self):
		return self.single_query("Date",str)
	
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
		return ", ".join(self.multiple_query("Genre",str))

	def get_album_list(self):
		return ", ".join(map(lambda a: a.get_name(), self.multiple_query("recorded",Album)))

	def get_event_list(self):
		return self.inverse_multiple_query("performed_by",Event)
		
	def get_summary(self):
		return self.single_query("Summary",str).replace('\\n','</br>')

class Place(RDFObject):
	pass

class Album(RDFObject):
	pass