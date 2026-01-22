# extract_ifc_properties.py
# Purpose: Extract property sets from NTU_Campus_Sample.ifc into CSV for TH2 ETL

import ifcopenshell
import csv
from pathlib import Path

# ---------- Configuration ----------
input_ifc = Path("NTU_Campus_Sample.ifc")
output_csv = Path("NTU_Campus_Properties.csv")

# ---------- Load IFC ----------
print(f"📂 Loading IFC file: {input_ifc}")
model = ifcopenshell.open(input_ifc)

# ---------- Prepare output ----------
rows = []
header = ["GlobalId", "Name", "IfcClass", "PsetName", "Property", "Value"]

# ---------- Iterate through all objects ----------
for element in model.by_type("IfcObjectDefinition"):
    if hasattr(element, "IsDefinedBy"):
        for rel in element.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_def = rel.RelatingPropertyDefinition
                if prop_def.is_a("IfcPropertySet"):
                    pset_name = prop_def.Name
                    for prop in getattr(prop_def, "HasProperties", []):
                        pname = prop.Name
                        pval = None
                        if hasattr(prop, "NominalValue") and prop.NominalValue:
                            pval = prop.NominalValue.wrappedValue
                        rows.append([
                            element.GlobalId,
                            getattr(element, "Name", ""),
                            element.is_a(),
                            pset_name,
                            pname,
                            pval
                        ])

# ---------- Write CSV ----------
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ Extraction complete. {len(rows)} properties exported.")
print(f"📄 Output file: {output_csv.resolve()}")
