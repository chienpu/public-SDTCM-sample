# TH5 — AI-Assisted Ontology & Data Ingestion

## 🎯 Validation Objective
To evaluate the effectiveness of AI-assisted parsing in converting spreadsheet-based LCA data into ontology-compliant triples.

---

## 🧠 Method Overview
- LLM-based parser trained to identify quantity, unit, and factor patterns.  
- Parsed outputs automatically matched to ontology classes.  
- Expert review ensures semantic accuracy.

---

## 📊 Key Results
| Metric | Result | Description |
|---------|---------|-------------|
| Parsing Accuracy | 85 % | vs expert benchmark |
| Revision Effort Reduction | 60 % | Expert time saved vs manual RDF conversion |

---

## 🗂️ Artifacts
- `ai_parser.ipynb` — Notebook for AI parsing logic  
- `lca_input_sample.xlsx` — Input spreadsheet  
- `generated_triples.ttl` — Parsed ontology output  
- `refinement_example.png` — Visualization of post-processing  

---

## 🔗 Relation to Other Layers
- **Feeds:** `/TH2-integration/` (pre-processed triples)  
- **Enhances:** Future ontology population efficiency

---

## 🧩 Validation Outcome
✅ AI-assisted parsing substantially reduces manual effort while maintaining semantic integrity.  
Promotes scalable adoption of ontology-based carbon management.
