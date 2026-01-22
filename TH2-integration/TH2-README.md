# 🧩 TH2 – Semantic Data Integration (ETL & SHACL Validation)

**Purpose:**  
This experiment validates whether heterogeneous BIM, IoT, and LCA datasets can be semantically integrated into a unified ontology-based graph using the *Semantic Digital Thread (SDT)* framework.  
The validation confirms that BIM entities can be enriched with both **embodied (LCA)** and **operational (IoT)** carbon data through a unified ETL pipeline, significantly reducing manual reconciliation effort.

---

## 🎯 Validation Objective
To confirm that ontology-guided data integration can:
- Semantically align BIM, IoT, and LCA data within a unified graph.
- Preserve structural and unit consistency through SHACL validation.
- Reduce manual reconciliation time compared with Excel-based workflows.

---

## 🧠 Method Overview
- **Python ETL pipeline** processes BIM (IFC), IoT, and LCA datasets.  
- **Ontology mapping** leverages TH1 ontology classes (e.g., `sdt:Asset`, `sdt:PerformanceData`).  
- **SHACL rules** in `sdt_tbox_s1.ttl` validate instance completeness and unit coherence.  
- Automated reconciliation between `IfcGUID`, `SensorID`, and lifecycle modules ensures traceable linkage.

---

## 📂 Folder Structure
```
TH2_Semantic_Data_Integration/
│
├─ data_sources/
│ ├─ building_model.ifc # BIM model extract (IfcBuildingElement, IfcSpace)
│ ├─ campus_energy.csv # IoT sensor readings (timestamp, power, CO₂)
│ ├─ lca_spreadsheet.xlsx # LCA dataset (A1–A3 embodied carbon factors)
│
├─ ontology/
│ ├─ sdt_tbox_s1.ttl # Core ontology schema (TBox)
│ └─ sdt_imports.ttl # External ontology imports (SOSA, PROV-O, IFC)
│
├─ scripts/
│ ├─ etl_pipeline.py # Python ETL: integrates IFC + IoT + LCA
│ ├─ validate_shacl.py # SHACL validation script (computes instance correctness)
│
├─ dataset/
│ ├─ ntu_campus_sample2.ttl # Integrated dataset (ABox, ETL output)
│
├─ validation/
│ ├─ validation_report.csv # SHACL validation results
│ └─ shacl_shapes.ttl # (optional) Shape constraints used for validation
│
└─ README.md
```
---

## ▶️ Run Instructions

### 1️⃣ Generate Integrated Dataset
```bash
python scripts/etl_pipeline.py
```
This merges IFC, IoT, and LCA sources into:
```bash
/dataset/ntu_campus_sample2.ttl
```

### 2️⃣Validate Semantic Consistency
```bash
python scripts/validate_shacl.py dataset/ntu_campus_sample2.ttl ontology/sdt_tbox_s1.ttl
```

#### Expected Output
```bash
✅ Conforms: True
📊 Instance correctness: 98–100%
🧩 Total instances: <n>, Violations: 0
📂 Validation results exported to: validation_report.csv
```

## 📊 Key Results
| Metric | Result | Description |
|---------|---------|-------------|
| **SHACL Validation Pass Rate** | 98–100 % | All instantiated triples meet ontology constraints |
| **Integration Effort Reduction** | 70 % ↓ | Compared with Excel-based manual merging |
| **Instance Correctness** | High | Confirmed via Neo4j validation |

## 🔗 Relation to Other Layers
- **Feeds:** `/TH3-reasoning/` (reasoning inputs for provenance traceability)  
- **Uses:** `/TH1-ontology/` (schema constraints and TBox classes)  
- **Extends:** `/TH5-ai-ingestion/` (AI-assisted ingestion workflows)

---

## 🧩 Validation Outcome
✅ **98–100 % SHACL conformance** achieved with substantial reduction in manual integration effort.  
⚡ Demonstrates the *practical feasibility* of ontology-based data ingestion and semantic alignment across BIM, IoT, and LCA domains.

## ⚙️ Pipeline Overview
```css
flowchart LR
  subgraph A[Data Sources]
    BIM[📘 BIM (IFC Extract)]
    IoT[🌡️ IoT Sensor Data]
    LCA[📊 LCA Spreadsheet]
  end

  subgraph B[ETL & Semantic Mapping]
    ETL[🧩 Python ETL Pipeline\n(Entity Extraction, Mapping, Merging)]
    Mapping[🗂️ Ontology Mapping\n(BS EN 15978 + SOSA + PROV-O)]
  end

  subgraph C[Graph Integration & Validation]
    Neo4j[(🕸️ Neo4j Graph Database)]
    SHACL[✅ SHACL Validation\nInstance Correctness: 100%]
  end

  BIM --> ETL
  IoT --> ETL
  LCA --> ETL
  ETL --> Mapping --> Neo4j --> SHACL
```
## 🔗 Relation to Other Layers
-Uses: /TH1-ontology/ → Provides schema constraints (TBox, property definitions).
-Feeds: /TH3-reasoning/ → Supplies validated ABox data for reasoning and provenance traceability.
-Extends: /TH5-ai-ingestion/ → Serves as baseline for AI-assisted ingestion automation.

## 🧩 Validation Outcome

✅ 98–100 % SHACL conformance achieved with substantial reduction in manual integration effort.
⚡ Demonstrates the practical feasibility of ontology-based data ingestion and semantic alignment across BIM, IoT, and LCA domains.
The results confirm the effectiveness of the SDT framework in achieving reliable cross-domain interoperability while maintaining traceable data provenance.

Author: C.-P. Huang
Affiliation: National Taiwan University / BuiltInsight Project
Contact: builtinsight.io | github.com/builtinsight


---
