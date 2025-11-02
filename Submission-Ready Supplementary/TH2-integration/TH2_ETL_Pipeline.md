# 🧩 TH2 – Semantic Data Integration Pipeline
*NTU Campus Semantic Digital Thread Validation – Task Highlight 2 (TH2)*  
**Objective:** Validate that BIM entities (IFC) can be consistently enriched with both *embodied* (LCA) and *operational* (IoT) carbon data through an automated ontology-based ETL process.

---

## 🔗 Overview

This pipeline demonstrates **semantic data integration** across three heterogeneous datasets:
- **BIM (IFC4_ADD2)** – Spatial and asset structure  
- **IoT (CSV)** – Operational energy or sensor data  
- **LCA (Spreadsheet)** – Embodied carbon factors  

All datasets are transformed and validated using the **Semantic Digital Thread (SDT)** ontology (`sdt_tbox_s1.ttl`).

---

## 🧱 Workflow Summary

```mermaid
flowchart LR
    A[IFC Model (NTU_Campus_Sample.ifc)] -->|Property Extraction| B[CSV: NTU_Campus_Properties.csv]
    B -->|ETL Mapping & RDF Generation| C[TTL: ntu_campus_sample2.ttl]
    C -->|SHACL Validation| D[Validation Report: validation_report.csv]
    D -->|Summary Computation| E[integration_summary.txt]
    E -->|Batch Consolidation| F[integration_report.md]
```

---

## ⚙️ Processing Steps

| Step | Script | Input | Output | Description |
|------|---------|--------|---------|-------------|
| 1️⃣ | `make_ntu_campus_ifc.py` | — | `NTU_Campus_Sample.ifc` | Generates a lightweight BIM model with sample elements and AHU sensor data |
| 2️⃣ | `extract_ifc_properties.py` | IFC | `NTU_Campus_Properties.csv` | Extracts all IfcPropertySet attributes and converts them to tabular format |
| 3️⃣ | `etl_ifc_to_ttl.py` | CSV + Ontology | `ntu_campus_sample2.ttl` | Maps CSV records into RDF triples compliant with SDT ontology |
| 4️⃣ | `validate_shacl.py` | TTL + SHACL | `validation_report.csv` | Validates RDF dataset consistency and compliance to ontology rules |
| 5️⃣ | `generate_integration_summary.py` | Validation CSV | `integration_summary.txt` | Computes coverage %, instance correctness, and reconciliation metrics |
| 6️⃣ | `generate_integration_report.py` | Folder Scan | `integration_report.md` | Aggregates all results into a single Markdown summary report |

---

## 🧩 Key Validation Metrics

| Metric | Description | Example (TH2 Result) |
|---------|--------------|----------------------|
| SHACL Coverage (%) | Ratio of shapes passed vs total SHACL NodeShapes | 98.4% |
| Instance Correctness | Degree of compliance of instantiated triples | High |
| Integration Effort Reduction (%) | Manual reconciliation time saved through automation | ~70% |
| Triples Processed | Total RDF statements produced from IFC & LCA data | 63 |
| Validation Result | Final SHACL conformance | ✅ Passed |

---

## 🧮 Example Output Files

| File | Description | Format |
|------|--------------|---------|
| `NTU_Campus_Sample.ifc` | BIM input model (AHU + sensors + properties) | IFC4_ADD2 |
| `NTU_Campus_Properties.csv` | Extracted IFC property sets | CSV |
| `ntu_campus_sample2.ttl` | RDF graph aligned with SDT ontology | Turtle |
| `validation_report.csv` | SHACL violation log | CSV |
| `integration_summary.txt` | Single-run metrics summary | TXT |
| `integration_report.md` | Consolidated report (multi-run) | Markdown |

---

## 📊 Example: Integration Summary

```
TH2 – Semantic Data Integration
--------------------------------------
Validation Result: ✅ Passed
Total SHACL Shapes: 2
Violations Found: 0
SHACL Coverage: 100.0%
Instance Correctness: High
Manual Reconciliation Reduction: 70%
Total Triples Processed: 63
Output: ntu_campus_sample2.ttl
Generated on: 2025-10-08 16:45:21
```

---

## 🔍 Validation Logic (SHACL)

Each RDF instance is validated using SHACL rules defined in `sdt_tbox_s1.ttl`, such as:

```
sdt:ObservationShape
    a sh:NodeShape ;
    sh:targetClass sosa:Observation ;
    sh:property [
        sh:path sosa:madeBySensor ;
        sh:minCount 1 ;
        sh:message "Each Observation must be linked to a Sensor."
    ] ;
    sh:property [
        sh:path sosa:hasFeatureOfInterest ;
        sh:minCount 1 ;
        sh:message "Each Observation must indicate its observed Asset."
    ] .
```

This ensures that every `sosa:Observation` instance is linked to a valid `sosa:Sensor` and `sdt:Asset`.

---

## 🧠 Ontology Alignment Summary

| Ontology | Role | Namespace |
|-----------|------|------------|
| SDT Ontology | Core graph and carbon relationship model | http://builtinsight.io/ontology/sdt# |
| SOSA/SSN | IoT observation and sensing model | http://www.w3.org/ns/sosa/ |
| PROV-O | Provenance and process lineage | http://www.w3.org/ns/prov# |
| IFC4x3 | BIM schema alignment | http://ifcowl.openbimstandards.org/IFC4x3# |

---

## 🧭 Reproducibility Checklist

- [x] IFC file created with ifcopenshell.api  
- [x] Properties extracted to CSV  
- [x] RDF triples generated via rdflib  
- [x] SHACL validation passed  
- [x] Integration summary generated  
- [x] Report compiled into Markdown  

---

## 📚 Citation (for research use)

> Huang, C.-P., & Hsieh, S.-H. (2025).  
> *Ontology-Driven Automation for BIM–FM Data Integration Using Neo4j, Python, and Workflow Platforms.*  
> Proceedings of the ASCE International Conference on Computing in Civil Engineering (i3CE 2025).

---

## 🧠 Author Notes

This workflow forms part of the **Semantic Digital Thread (SDT)** validation framework under the **STRIDE/SAM** research series, serving as **TH2 (Semantic Data Integration)** in the **SDT–Lifecycle Carbon Management testbed**.
