from rdflib.graph import ConjunctiveGraph as Graph

from rdflib import Namespace, Literal, URIRef

class PowerGraph(Graph):
    
    def has_sth(self, url, f):
        if not isinstance(url,URIRef):
            url = URIRef(url)
        return bool(list(self.triples(f(url))))
    
    def has_subject(self, url):
        return self.has_sth(url, lambda url: (url, None, None))

    def has_object(self, url):
        return self.has_sth(url, lambda url: (None, None, url))

    def has_verb(self, url):
        return self.has_sth(url, lambda url: (None, url, None))