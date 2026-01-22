# TH4 — Provenance & Traceability

## 🎯 Validation Objective
To verify that the system can reconstruct full decision lineage (IoT → BIM → LCA → maintenance) using PROV-O relations for auditability.

---

## 🧠 Method Overview
- All data and computation steps represented as PROV-O Entities, Activities, Agents.  
- Neo4j queries reconstruct lineage across containers.  
- Provenance results visualized in Neo4j Bloom.

---

## 📊 Key Results
| Metric | Result | Description |
|---------|---------|-------------|
| Traceability Completeness | 100 % | Full lineage reconstruction across all datasets |
| Lineage Depth | Avg. 5 relations | per decision chain |

---

## 🗂️ Artifacts
- `provenance_query.cypher` — Lineage reconstruction query  
- `bloom_lineage.png` — Visualization of decision chain  
- `provenance_chain.ttl` — Exported PROV graph  

---

## 🔗 Relation to Other Layers
- **Logs:** Activities from `/TH3-reasoning/`  
- **Supports:** Reproducibility in `/TH6-deployment/`

---

## 🧩 Validation Outcome
✅ Complete and queryable audit trail achieved.  
Ensures accountability and data trustworthiness across the SDT framework.
