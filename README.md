# Semantic Digital Thread – NTU Prototype
*A standards-aligned, ontology-driven framework for lifecycle carbon management*  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](deployment/docker/docker-compose.yml)  

---

## 📖 Overview  
This repository hosts the **prototype implementation** of the **Semantic Digital Thread (SDT)** validated through the NTU campus case study.  
The SDT enables:  

- Standards-aligned **ontology backbone** (BS EN 15978 × IFC × SOSA × PROV-O).  
- Semantic **data integration** of BIM, IoT, and LCA sources.  
- Graph-native **reasoning** and anomaly detection.  
- Workflow automation with **n8n** for facility management actions.  
- PROV-enabled **traceability** for audit-ready carbon reporting.  
- **AI-assisted ingestion** to reduce manual ontology/data modeling effort.  
- Fully **Dockerized deployment** for reproducibility.  

👉 For full methodology, see:  
Huang, C.-P. & Hsieh, S.-H. (2025). *Semantic Digital Thread for Lifecycle Carbon Management: An Ontology-Driven Framework for Data Integration, Reasoning, and Traceability*.  

---

## 🚀 Quickstart  

```bash
# 1. Clone repo
git clone https://github.com/YourOrg/SemanticDigitalThread-NTU.git
cd SemanticDigitalThread-NTU

# 2. (Optional) configure environment
cp deployment/docker/.env.example .env
# edit passwords, API keys as needed

# 3. One-click deployment
docker compose up -d

# 4. Access services
Neo4j Browser → http://localhost:7474 (user: neo4j / pass: your_pwd)  
n8n Workflow UI → http://localhost:5678 (user: user / pass: your_pwd)  
```

---

## 📂 Repository Structure (High-Level)

```
/ontologyschema/       # TH1 – Standards-aligned ontology (TBox, schema exports)
/integration/etl/       # TH2 – ETL pipelines & sample datasets (IFC, IoT, LCA)
/reasoning/workflows/   # TH3 – Cypher rules & n8n workflows for reasoning-to-action
/provenance/queries/    # TH4 – PROV-O based provenance queries & graph snapshots
/ai_ingestion/          # TH5 – AI-assisted ingestion (scripts, samples, outputs)
/deployment/docker/     # TH6 – Docker Compose setup for reproducibility
```

Additional files:  
- `README.md` → Overview + instructions  
- `LICENSE` → Open-source license (MIT/Apache-2.0)  
- `CONTRIBUTING.md` → Collaboration guidelines  
- `requirements.txt` → Python dependencies  
- `repo_structure.md` → Detailed file-level description of each folder  

👉 For detailed file-level contents of each folder (e.g., sample IFC, Cypher scripts, Dockerfiles), see [repo_structure.md](repo_structure.md).  

---

## 🧩 Mapping to Research Contributions  

| Technical Highlight | Folder | What’s Inside |
|---------------------|--------|----------------|
| **TH1. Standards-Aligned Ontology** | `/ontologyschema/` | Cypher schema, SHACL constraints, Neo4j exports |
| **TH2. Semantic Data Integration** | `/integration/etl/` | Python ETL scripts, raw/processed sample data |
| **TH3. Reasoning-to-Action** | `/reasoning/workflows/` | Cypher anomaly rules, n8n JSON workflows |
| **TH4. Provenance & Traceability** | `/provenance/queries/` | PROV queries, provenance graph exports |
| **TH5. AI-Assisted Ingestion** | `/ai_ingestion/` | AI parsing scripts, sample spreadsheets, RDF triples |
| **TH6. Reproducibility** | `/deployment/docker/` | Docker Compose, Dockerfiles, version logs |

---

## ✅ Validation Checklist (Quick Tests)  

After deployment:  

1. **Ontology schema loaded**  
```cypher
CALL db.schema.visualization()
```  

2. **ETL ingestion success**  
```cypher
MATCH (b:BuildingComponent)-[:HAS_CARBON_TOTAL]->(ct:CarbonTotal) RETURN b, ct LIMIT 5;
```  

3. **Anomaly detection**  
```cypher
MATCH (a:Anomaly) RETURN a LIMIT 5;
```  

4. **Provenance trace**  
```cypher
MATCH path = (ct:CarbonTotal {id:"BuildingX_B6"})-[*1..5]-(n) RETURN path;
```  

5. **n8n workflow trigger**  
Check n8n UI → run “Anomaly Alert” workflow → verify task creation/email.  

---

## 🔍 Citation  

If you use this repository, please cite:  

> Huang, C.-P., & Hsieh, S.-H. (2025). *Semantic Digital Thread for Lifecycle Carbon Management: An Ontology-Driven Framework for Data Integration, Reasoning, and Traceability*.  

---

## 📜 License  
Released under the [MIT License](LICENSE).  
