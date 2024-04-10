import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, SKOS

# Note: To update the input data, you can update the googlesheet and the code will automatically update the output file.
# See here for the googlesheet: https://docs.google.com/spreadsheets/d/1NhOt3NL6n4gAghnUGyPJpqOqGquy7e0FZsXpt94UpVk/edit#gid=0

# URL of the Google Sheet in CSV format published to the web
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS7cXXTu71hmQVbt5zvtLJAEqyI4t1zhEzGBGXTH38o-QlBEflNXY1PugOC2iJ4J0BN1Ocp6hODzrW1/pub?gid=0&single=true&output=csv"

# Read the data from the URL into a pandas DataFrame
df = pd.read_csv(url)

# Define the namespaces to be used in the RDF graph
namespaces = {
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    "owl": Namespace("http://www.w3.org/2002/07/owl#"),
    "xml": Namespace("http://www.w3.org/XML/1998/namespace"),
    "xsd": Namespace("http://www.w3.org/2001/XMLSchema#"),
    "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
    "skos": Namespace("http://www.w3.org/2004/02/skos/core#"),
}

# Create a new RDF graph
g = Graph()

# Bind the namespaces to the graph
for prefix, namespace in namespaces.items():
    g.bind(prefix, namespace)

# Iterate over the DataFrame rows
for _, row in df.iterrows():
    # Create a URI for each class, replacing spaces in the name with underscores
    class_uri = URIRef(f"http://example.org/{row['Name'].replace(' ', '_')}")

    # Add the class to the graph
    g.add((class_uri, RDF.type, namespaces["owl"].Class))

    # Add the name of the class as a label
    g.add((class_uri, RDFS.label, Literal(row["Name"])))

    # Add the definition of the class
    g.add((class_uri, SKOS.definition, Literal(row["Definition"])))

# Serialize the graph in Turtle format
turtle_data = g.serialize(format="turtle")

# Write the serialized data to a .ttl file
with open("../outputs/sdm_vocab.ttl", "w") as f:
    f.write(turtle_data)
