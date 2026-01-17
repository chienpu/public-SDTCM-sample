# Semantic Digital Thread (SDT) – NTU Prototype  
*A standards-aligned, ontology-driven framework for lifecycle carbon management*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](deployment/docker/docker-compose.yml)

---

## 📖 Overview  

This repository provides **reproducibility and transparency artifacts** for the research study:

> **Huang, C.-P. & Hsieh, S.-H. (2025).**  
> *Semantic Digital Thread for Lifecycle Carbon Management:  
> An Ontology-Driven Framework for Data Integration, Reasoning, and Traceability.*

It hosts a **research prototype implementation** of the **Semantic Digital Thread (SDT)** framework, validated through an NTU campus case study.

The SDT is positioned as a **general, ontology-driven digital twin methodology**, demonstrated here using **lifecycle carbon management** as a representative validation scenario.

Specifically, the prototype supports:

- A **standards-aligned ontology backbone** integrating  
  **BS EN 15978 × IFC × SOSA/SSN × PROV-O**
- Semantic **data integration pipelines** across BIM, IoT, and LCA datasets  
- Graph-native **reasoning and anomaly detection** using Cypher  
- **Workflow-oriented automation** via *n8n* for facility management actions  
- PROV-enabled **end-to-end traceability** for audit-ready carbon reporting  
- **AI-assisted ingestion** to reduce manual ontology and data modeling effort  
- Fully **Dockerized deployment** to support methodological reproducibility  

> ⚠️ **Scope note**  
> This repository is intended for **methodological validation and reproducibility** only.  
> It is **not** a production-ready facility management system.

---

## 🚀 Quickstart (Reproducibility Setup)

```bash
# 1. Clone repository
git clone https://github.com/chienpu/public-SDTCM-sample.git
cd public-SDTCM-sample

# 2. (Optional) configure environment
cp deployment/docker/.env.example .env
# Edit passwords or ports if needed

# 3. One-click deployment
docker compose up -d

# 4. Access services
Neo4j Browser → http://localhost:7474  
n8n Workflow UI → http://localhost:5678
```

---

## 📂 Repository Structure (High-Level)

```
/ontologyschema/        # TH1 – Standards-aligned ontology (TBox, schema exports)
/integration/etl/       # TH2 – ETL pipelines & sample datasets (IFC, IoT, LCA)
/reasoning/workflows/   # TH3 – Cypher rules & n8n workflows (reasoning-to-action)
/provenance/queries/    # TH4 – PROV-O based provenance queries & lineage examples
/ai_ingestion/          # TH5 – AI-assisted ingestion (scripts, samples, outputs)
/deployment/docker/     # TH6 – Docker Compose setup for reproducibility
```

---

## 🧩 Mapping to Research Contributions (TH1–TH6)

| Research Contribution | Folder | Description |
|----------------------|--------|-------------|
| **TH1. Standards-Aligned Ontology** | `/ontologyschema/` | Core SDT ontology (TBox), schema diagrams, constraint definitions |
| **TH2. Semantic Data Integration** | `/integration/etl/` | Python ETL scripts, sample BIM/IoT/LCA datasets |
| **TH3. Reasoning-to-Action** | `/reasoning/workflows/` | Cypher reasoning rules and n8n workflow templates |
| **TH4. Provenance & Traceability** | `/provenance/queries/` | PROV-O lineage queries and graph snapshots |
| **TH5. AI-Assisted Ingestion** | `/ai_ingestion/` | AI parsing notebooks, generated RDF triples, refinement examples |
| **TH6. Reproducibility** | `/deployment/docker/` | Docker Compose files and container specifications |

---

## 📜 License  

Released under the [MIT License](LICENSE).

