# TH6 — Reproducibility via Docker Deployment

## 🎯 Validation Objective
To verify that the SDT testbed can be redeployed across environments with one-click reproducibility.

---

## 🧠 Method Overview
- Three core containers:
  - **Neo4j** — Ontology management  
  - **Python ETL** — Data ingestion  
  - **n8n** — Workflow automation  
- All services orchestrated via Docker Compose.  
- Version-controlled workflow templates ensure consistency.

---

## 📊 Key Results
| Metric | Result | Description |
|---------|---------|-------------|
| Deployment Success Rate | 100 % | Across local and server environments |
| Redeployment Time | < 3 min | One-click initialization |
| Workflow Consistency | 100 % | Confirmed via version hash check |

---

## 🗂️ Artifacts
- `docker-compose.yml` — Container orchestration file  
- `Dockerfile.neo4j`, `Dockerfile.etl`, `Dockerfile.n8n` — Image definitions  
- `init.sh` — Initialization script  
- `deployment_overview.png` — System architecture diagram  

---

## 🔗 Relation to Other Layers
- **Hosts:** `/TH1–TH5/` processes within containerized services  
- **Ensures:** End-to-end reproducibility for validation evidence  

---

## 🧩 Validation Outcome
✅ All validation steps (TH1–TH5) successfully reproduced under containerized deployment.  
Confirms the SDT as a portable research-to-practice testbed.
