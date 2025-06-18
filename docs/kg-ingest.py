import json
from rdflib import Graph, RDF, RDFS, OWL, URIRef

g = Graph()
g.parse("your_file.ttl", format="ttl")  # Replace with your TTL file

label_map = {}
type_map = {}

# Collect labels
for s, _, o in g.triples((None, RDFS.label, None)):
    label_map[s] = str(o)

# Collect types
for s, _, o in g.triples((None, RDF.type, None)):
    if s not in type_map:
        type_map[s] = set()
    type_map[s].add(o)

# Node assembly
nodes = {}
for s in set(type_map.keys()):
    label = label_map.get(s, str(s).split("/")[-1])
    rdf_types = list(type_map[s])
    nodes[str(s)] = {
        "id": str(s),
        "label": label,
        "types": [t.n3(g.namespace_manager) for t in rdf_types]
    }

# Edge assembly
links = []
for s, p, o in g.triples((None, None, None)):
    if isinstance(p, URIRef) and isinstance(o, URIRef):
        if (p, RDF.type, OWL.ObjectProperty) in g:
            p_type = "ObjectProperty"
        elif (p, RDF.type, OWL.DatatypeProperty) in g:
            p_type = "DatatypeProperty"
        elif (p, RDF.type, OWL.AnnotationProperty) in g:
            p_type = "AnnotationProperty"
        else:
            continue

        links.append({
            "source": str(s),
            "target": str(o),
            "label": label_map.get(p, p.split("/")[-1]),
            "iri": str(p),
            "type": p_type
        })

graph_data = {
    "nodes": list(nodes.values()),
    "links": links
}

with open("graph.json", "w", encoding="utf-8") as f:
    json.dump(graph_data, f, indent=2)
