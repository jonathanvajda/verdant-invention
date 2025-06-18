import json
from rdflib import Graph, RDF, RDFS, OWL, URIRef

# Load RDF data
g = Graph()
g.parse("your_file.ttl", format="ttl")  # <-- Replace with your TTL file path

# Label map
label_map = {}
for s, p, o in g.triples((None, RDFS.label, None)):
    if isinstance(o, str):
        label_map[s] = str(o)

# Extract nodes
nodes = {}
for s in g.subjects(RDF.type, OWL.NamedIndividual):
    nodes[str(s)] = {
        "id": str(s),
        "label": label_map.get(s, str(s).split("/")[-1]),
    }

# Extract links (object properties between individuals)
links = []
for s, p, o in g.triples((None, None, None)):
    if (s, RDF.type, OWL.NamedIndividual) in g and (o, RDF.type, OWL.NamedIndividual) in g:
        if (p, RDF.type, OWL.ObjectProperty) in g:
            links.append({
                "source": str(s),
                "target": str(o),
                "label": label_map.get(p, str(p).split("/")[-1])
            })

# Assemble JSON
graph_data = {
    "nodes": list(nodes.values()),
    "links": links
}

# Output to file
with open("graph.json", "w", encoding="utf-8") as f:
    json.dump(graph_data, f, indent=2)
