import argparse
import os
import json
from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.plugin import PluginException

# --- Helper: Detect RDF Format from File Extension ---
def detect_format(filename):
    ext = os.path.splitext(filename)[1].lower()
    return {
        ".ttl": "turtle",
        ".nt": "nt",
        ".n3": "n3",
        ".rdf": "xml",
        ".owl": "xml",
        ".xml": "xml",
        ".jsonld": "json-ld",
        ".trig": "trig",
        ".nq": "nquads"
    }.get(ext, None)

# --- Argument Parser ---
parser = argparse.ArgumentParser(description="Convert OWL2 RDF graph to D3-compatible JSON.")
parser.add_argument("--input", default="knowledge-graph.ttl", help="Input OWL2 file (Turtle, RDF/XML, etc.)")
parser.add_argument("--output", default="graph.json", help="Output JSON file for D3 graph")
args = parser.parse_args()

# --- Check if File Exists ---
if not os.path.exists(args.input):
    raise FileNotFoundError(f"Input file '{args.input}' does not exist.")

# --- Detect Format ---
rdf_format = detect_format(args.input)
if not rdf_format:
    raise ValueError(f"Unsupported or unrecognized file extension: {args.input}")

# --- Load RDF Graph ---
g = Graph()
try:
    g.parse(args.input, format=rdf_format)
except PluginException as pe:
    raise ValueError(f"RDFLib plugin error: {pe}")
except Exception as e:
    raise ValueError(f"Failed to parse RDF file '{args.input}': {e}")

# --- Optional OWL2 Check ---
if not any((s, RDF.type, OWL.Class) in g or (s, RDF.type, OWL.NamedIndividual) in g for s in g.subjects()):
    raise ValueError("File does not appear to contain OWL2 class or individual declarations.")

# --- Collect Labels ---
label_map = {}
type_map = {}

for s, _, o in g.triples((None, RDFS.label, None)):
    label_map[s] = str(o)

for s, _, o in g.triples((None, RDF.type, None)):
    if s not in type_map:
        type_map[s] = set()
    type_map[s].add(o)

# --- Build Nodes ---
nodes = {}
for s in set(type_map.keys()):
    label = label_map.get(s, str(s).split("/")[-1])
    rdf_types = list(type_map[s])
    nodes[str(s)] = {
        "id": str(s),
        "label": label,
        "types": [t.n3(g.namespace_manager) for t in rdf_types]
    }

# --- Build Links ---
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

# --- Output JSON ---
graph_data = {"nodes": list(nodes.values()), "links": links}
with open(args.output, "w", encoding="utf-8") as f:
    json.dump(graph_data, f, indent=2)

print(f"✅ Graph successfully exported to: {args.output}")
