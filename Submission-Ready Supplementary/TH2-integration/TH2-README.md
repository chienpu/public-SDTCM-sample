# TH2 — Semantic Data Integration (ETL & SHACL Validation)

## 🎯 Validation Objective
To confirm that BIM entities can be enriched with **embodied (LCA)** and **operational (IoT)** carbon data through a unified ETL pipeline, minimizing manual reconciliation.

---

## 🧠 Method Overview
- Python ETL container processes BIM (IFC), IoT, and LCA data.
- Schema mapping based on TH1 ontology classes.
- SHACL rules used to validate instance consistency and units.
- Automated ID reconciliation between `IfcGUID`, `SensorID`, and lifecycle modules.

---

## 📊 Key Results
| Metric | Result | Description |
|---------|---------|-------------|
| SHACL Validation Pass Rate | 98 % | All instantiated triples meet ontology constraints |
| Integration Effort Reduction | 70 % ↓ | Compared with Excel-based manual merging |
| Instance Correctness | High | Confirmed via Neo4j validation |

---

## 🗂️ Artifacts
- `etl_main.py` — Core Python ETL script  
- `data_sample/` — Input datasets (IFC, IoT, LCA)  
- `neo4j_import.csv` — Output for Neo4j import  
- `validation_report.ttl` — SHACL report  
- `etl_workflow_diagram.png` — ETL pipeline visualization  

---

## 🔗 Relation to Other Layers
- **Feeds:** `/TH3-reasoning/` (reasoning inputs)  
- **Uses:** `/TH1-ontology/` (schema constraints)

---

## 🧩 Validation Outcome
✅ 98 % SHACL conformance achieved with substantial reduction in integration effort.  
⚡ Demonstrates practical feasibility of ontology-based data ingestion.
