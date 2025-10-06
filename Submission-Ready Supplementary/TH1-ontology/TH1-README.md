# TH1 — Standards-Aligned Ontology (Interoperability)

## 🎯 Validation Objective
To verify whether lifecycle carbon data at the campus scale can align **BS EN 15978 modules**, **IFC building entities**, and **SOSA IoT observations** within a unified ontology backbone.

---

## 🧠 Method Overview
- Ontology backbone (TBox) designed in Neo4j using:
  - **BS EN 15978** modules (A1–D)
  - **IFC 4x3** entities for BuildingComponent, Space, Asset
  - **SOSA** Observation / Sensor hierarchy
  - **PROV-O** for provenance traceability
- Schema formalized as `ontology_tbox.ttl` and visualized via Neo4j Bloom.
- Validation focuses on cross-standard mapping coverage and logical completeness.

---

## 📊 Key Results
| Metric | Result | Description |
|---------|---------|-------------|
| Mapping Coverage | 92 % | Lifecycle modules correctly linked to IFC and SOSA classes |
| Triple-Chain Completeness | 100 % | Full alignment achieved across ontology modules |
| Gaps | IFC Pset attributes (≈ 8 %) | Omitted for scope reasons |

---

## 🗂️ Artifacts
- `ontology_tbox.ttl` — Complete TBox file  
- `ontology_schema.png` — Neo4j schema visualization  
- `schema_description.md` — Class/relation documentation  

---

## 🔗 Relation to Other Layers
- **Feeds:** `/TH2-integration/` (ETL instance creation)  
- **Used by:** `/TH3-reasoning/`, `/TH4-provenance/`

---

## 🧩 Validation Outcome
✅ Ontology successfully aligned across BS EN 15978, IFC, and SOSA standards.  
⚠ Extension of IFC Psets identified as future work for richer semantic detail.
