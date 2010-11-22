from datetime import datetime, timedelta
from rdflib import Namespace, Literal, URIRef

import settings
from django.core.management import setup_environ
setup_environ(settings)
from django_rdf import graph

from events.semantic import ontologies

graph.add((ontologies['me']['event1'],ontologies['rdf']['type'],ontologies['me']['Event']))
graph.add((ontologies['me']['event1'],ontologies['me']['Description'],Literal('ola, sou o evento1')))

graph.add((ontologies['me']['artist1'],ontologies['rdf']['type'],ontologies['me']['Artist']))
graph.add((ontologies['me']['artist1'],ontologies['me']['Description'],Literal('ola, sou o artista1')))

graph.add((ontologies['me']['event1'],ontologies['me']['performed_by'],ontologies['me']['artist1']))


from pprint import pprint
pprint(list(graph))


# just think .whatever((s, p, o))
# here we report on what we know

pprint(list(graph.subjects()))
pprint(list(graph.predicates()))
pprint(list(graph.objects()))

# and other things that make sense

# what do we know about pat?
pprint(list(graph.predicate_objects(ontologies['me']['event1'])))

# who is what age?
pprint(list(graph.subject_objects(ontologies['me']['description'])))	

print list(graph.query(""" SELECT ?cenas WHERE { ?cenas me:Description ?descri . } """, initNs=ontologies))

graph.commit()
