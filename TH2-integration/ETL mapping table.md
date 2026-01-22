# 🧩 ETL Mapping Table — Semantic Data Integration (TH2)

**Purpose:**  
Defines the column-to-ontology mapping rules used in the `etl_pipeline.py` to transform BIM, IoT, and LCA source data into ontology-compliant RDF triples (Turtle format).  
Each mapping follows the class and property definitions in `sdt_tbox_s1.ttl`.

---

## 🏗️ 1. BIM Data → `sdt:Asset`

| Source File | Sample Columns | Target Ontology Class | Property Mappings | Example Triple |
|--------------|----------------|------------------------|-------------------|----------------|
| `data_sources/building_model.ifc` (or CSV export) | `GlobalId`, `Name`, `Type`, `ObjectType` | `sdt:Asset` | - `GlobalId` → `sdt:ifcGUID`  <br> - `Name` → `rdfs:label` | `sdt:AHU12 a sdt:Asset ; sdt:ifcGUID "3adG-XYZ-123" ; rdfs:label "Air Handling Unit 12" .` |
| Optional Fields | `Parent`, `System`, `Zone` | `sdt:Asset` relationships | - `System` → `sdt:partOfSystem` *(if defined)* | — |

**Transformation Note:**  
Each IFC entity with `IfcBuildingElement` class type should be converted into an RDF node under `sdt:Asset`.  
The `ifcGUID` ensures traceable alignment across domains.

---

## ⚡ 2. IoT Sensor Data → `sosa:Observation` + `sosa:Sensor`

| Source File | Sample Columns | Target Ontology Class | Property Mappings | Example Triple |
|--------------|----------------|------------------------|-------------------|----------------|
| `data_sources/campus_energy.csv` | `Timestamp`, `SensorID`, `Value`, `Unit`, `AssetID` | `sosa:Observation` | - `SensorID` → `sosa:madeBySensor` <br> - `AssetID` → `sosa:hasFeatureOfInterest` <br> - `Value` → `sdt:value` <br> - `Unit` → `sdt:unit` <br> - `Timestamp` → `sdt:timestamp` | `sdt:Obs002 a sosa:Observation ; sosa:madeBySensor sdt:BLDG_A_Sensor01 ; sosa:hasFeatureOfInterest sdt:BLDG_A_Roof ; sdt:value "124.7"^^xsd:decimal ; sdt:unit "kWh" ; sdt:timestamp "2025-10-08T14:00:00Z"^^xsd:dateTime .` |
| `Sensor Metadata` (if separate CSV) | `SensorID`, `Type`, `Location` | `sosa:Sensor` | - `SensorID` → `rdfs:label` <br> - `Location` → `sdt:monitors` (links to Asset) | `sdt:BLDG_A_Sensor01 a sosa:Sensor ; sdt:monitors sdt:BLDG_A_Roof ; rdfs:label "Roof Energy Sensor 01" .` |

**Transformation Note:**  
IoT readings are converted into `sosa:Observation` nodes linked to `sosa:Sensor` and `sdt:Asset`.  
The timestamp ensures temporal traceability for TH2–TH3 reasoning.

---

## 🌱 3. LCA Data → `sdt:EmbodiedCarbonResult` + `sdt:EmissionFactor`

| Source File | Sample Columns | Target Ontology Class | Property Mappings | Example Triple |
|--------------|----------------|------------------------|-------------------|----------------|
| `data_sources/lca_spreadsheet.xlsx` | `Material`, `LifecycleStage`, `GWP_kgCO2e`, `Unit`, `Source` | `sdt:EmbodiedCarbonResult` | - `GWP_kgCO2e` → `sdt:value` <br> - `Unit` → `sdt:unit` <br> - `LifecycleStage` → `sdt:hasModule` (maps to individuals A1–C4) <br> - `Material` → `rdfs:label` or linked Asset via `sdt:aboutAsset` | `sdt:EmbRes001 a sdt:EmbodiedCarbonResult ; sdt:value "1280.5"^^xsd:decimal ; sdt:unit "kgCO2e" ; sdt:hasModule sdt:A1 ; sdt:aboutAsset sdt:BLDG_A_Roof .` |
|  | `Source`, `Factor`, `Uncertainty` | `sdt:EmissionFactor` | - `Source` → `sdt:source` <br> - `Factor` → `sdt:value` <br> - `Uncertainty` → `sdt:uncertainty` | `sdt:Factor_A1_Steel a sdt:EmissionFactor ; sdt:source "ICE v4.0" ; sdt:value "1.85"^^xsd:decimal ; sdt:unit "kgCO2e/kg" .` |

**Transformation Note:**  
Each material row corresponds to an `EmbodiedCarbonResult` linked to its `EmissionFactor`.  
Use lifecycle modules (`A1`–`C4`) from the ontology as controlled vocabulary.

---

## 🔄 4. Cross-Domain Linkage Rules

| Relationship | Domain → Range | Ontology Property | Description |
|---------------|----------------|------------------|--------------|
| Sensor–Asset | `sosa:Sensor` → `sdt:Asset` | `sdt:monitors` | Links IoT sensors to their monitored assets |
| Observation–Sensor | `sosa:Observation` → `sosa:Sensor` | `sosa:madeBySensor` | Connects measurement record to its originating sensor |
| Observation–Asset | `sosa:Observation` → `sdt:Asset` | `sosa:hasFeatureOfInterest` | Binds measurement result to building component |
| Carbon Result–Asset | `sdt:CarbonResult` → `sdt:Asset` | `sdt:aboutAsset` | Ensures traceability between carbon calculation and physical asset |
| Carbon Result–Module | `sdt:CarbonResult` → `sdt:LifecycleModule` | `sdt:hasModule` | Maps emission record to its lifecycle phase |
| Carbon Result–Emission Factor | `sdt:CarbonResult` → `sdt:EmissionFactor` | `sdt:derivedFromFactor` | Captures source of embodied/operational factor |

---

## 🧮 5. Example Integration Output (Target Schema)

| Entity | Class | Linked To | Key Properties |
|---------|--------|-----------|----------------|
| `sdt:BLDG_A_Roof` | `sdt:Asset` | — | `sdt:ifcGUID`, `rdfs:label` |
| `sdt:BLDG_A_Sensor01` | `sosa:Sensor` | `sdt:BLDG_A_Roof` | `sdt:monitors` |
| `sdt:Obs002` | `sosa:Observation` | `sdt:BLDG_A_Sensor01`, `sdt:BLDG_A_Roof` | `sdt:value`, `sdt:unit`, `sdt:timestamp` |
| `sdt:OpCarbon001` | `sdt:OperationalCarbonResult` | `sdt:B6`, `sdt:BLDG_A_Roof` | `sdt:value`, `sdt:timestamp` |
| `sdt:EmbRes001` | `sdt:EmbodiedCarbonResult` | `sdt:A1`, `sdt:Factor_A1_Steel`, `sdt:BLDG_A_Roof` | `sdt:value`, `sdt:unit` |

---

## 📦 6. Validation Alignment (SHACL Rules)

| SHACL Shape | Target Class | Key Constraints | Source Data Affected |
|--------------|---------------|------------------|----------------------|
| `sdt:OperationalResultShape` | `sdt:OperationalCarbonResult` | Must have `sdt:hasModule = sdt:B6`, numeric value, and timestamp | IoT-derived carbon results |
| `sdt:ObservationShape` | `sosa:Observation` | Must include both `sosa:madeBySensor` and `sosa:hasFeatureOfInterest` | All IoT observations |

---

## 🧭 7. Notes for Implementation

- Use `rdflib` to generate RDF triples programmatically.  
- IFC extraction can use [IfcOpenShell](https://ifcopenshell.org/).  
- Use `pandas` to read CSV and Excel files.  
- Ensure all URIs are prefixed with `sdt:` and unique identifiers (e.g., `sdt:Obs001`, `sdt:EmbRes001`).  
- Export integrated graph to:  `/dataset/ntu_campus_sample2.ttl`
- Then run:
```bash
python scripts/validate_shacl.py dataset/ntu_campus_sample2.ttl ontology/sdt_tbox_s1.ttl
```

Expected result:

✅ Conforms: True
📊 Instance correctness: 98–100%

---
Author: C.-P. Huang
Affiliation: National Taiwan University / BuiltInsight Project
Date: 2025-10-08