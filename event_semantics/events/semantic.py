from rdflib import Namespace,URIRef
from django_rdf import graph

ontologies = {
    'rdf':Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    'me':Namespace("http://www.owl-ontologies.com/MusicEvents.owl#")
}

graph.register_ontology(ontologies)