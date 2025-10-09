# etl_ifc_to_ttl.py
# Converts IFC-extracted CSV → RDF triples aligned with SDT ontology

import csv
from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD
from pathlib import Path

# ---------- Input & Output ----------
csv_file = Path("NTU_Campus_Properties.csv")
ttl_file = Path("ntu_campus_sample2.ttl")

# ---------- Namespaces ----------
SDT = Namespace("http://builtinsight.io/ontology/sdt#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
PROV = Namespace("http://www.w3.org/ns/prov#")
IFC  = Namespace("http://ifcowl.openbimstandards.org/IFC4x3#")
XSD_NS = Namespace("http://www.w3.org/2001/XMLSchema#")

# ---------- Graph ----------
g = Graph()
g.bind("sdt", SDT)
g.bind("sosa", SOSA)
g.bind("prov", PROV)
g.bind("ifc", IFC)
g.bind("rdfs", RDFS)

# ---------- Helper Function ----------
def create_asset_triples(row):
    """Create triples for IFC entities (Asset or Equipment)."""
    guid = row["GlobalId"]
    name = row["Name"]
    ifc_class = row["IfcClass"]
    pset = row["PsetName"]
    prop = row["Property"]
    val = row["Value"]

    asset_uri = SDT[guid]

    # classify type
    if "Sensor" in ifc_class:
        g.add((asset_uri, RDF.type, SOSA.Sensor))
    elif any(x in ifc_class for x in ["Equipment", "Fan", "Light"]):
        g.add((asset_uri, RDF.type, SDT.Asset))
    else:
        g.add((asset_uri, RDF.type, SDT.Asset))

    g.add((asset_uri, RDFS.label, Literal(name)))
    g.add((asset_uri, SDT.ifcGUID, Literal(guid)))

    # operational carbon result
    if "EnergyUse" in pset or "Power" in prop:
        result_uri = SDT[f"{guid}_operationalResult"]
        g.add((result_uri, RDF.type, SDT.OperationalCarbonResult))
        g.add((result_uri, SDT.aboutAsset, asset_uri))
        g.add((result_uri, SDT.hasModule, SDT.B6))
        if val:
            try:
                g.add((result_uri, SDT.value, Literal(float(val), datatype=XSD.decimal)))
            except:
                g.add((result_uri, SDT.value, Literal(str(val))))
        g.add((result_uri, SDT.unit, Literal("kWh" if "Power" in prop else "unknown")))
        g.add((result_uri, SDT.timestamp, Literal("2025-10-08T13:00:00Z", datatype=XSD.dateTime)))

    # general annotation
    if val:
        g.add((asset_uri, SDT.source, Literal(f"{pset}:{prop}={val}")))

# ---------- Process CSV ----------
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        create_asset_triples(row)

# ---------- Output RDF ----------
g.serialize(destination=ttl_file, format="turtle")
print(f"✅ TTL dataset generated: {ttl_file.resolve()}")
print(f"🔢 Total triples: {len(g)}")
