# SDT Reproducibility Testbed (Lifecycle Carbon Management)

This directory provides a minimal, containerized testbed to reproduce the
Semantic Digital Thread (SDT) for lifecycle carbon management as described in the paper.

The testbed focuses on:
- Graph-native semantic backbone (Neo4j)
- Standards-aligned ontology (TBox) and instantiated data (ABox)
- Reproducible reasoning and provenance annotation
- Lightweight, script-driven ETL for data ingestion

> Note: Workflow orchestration (e.g., n8n) is optional and disabled by default
> to keep the academic testbed minimal and reproducible.

---

## Services Overview

- **Neo4j**  
  Hosts the SDT semantic backbone, including ontology schema (TBox),
  instantiated BIM/IoT/LCA data (ABox), and Cypher/APOC-based reasoning with provenance annotations.

- **Python ETL (optional runner)**  
  Preprocesses and ingests ontology-driven BIM, IoT, and LCA datasets into Neo4j.

- **n8n (optional)**  
  Demonstrates workflow orchestration and agent-based automation.
  Disabled by default to avoid over-engineering in academic reproducibility packages.

---

## How to Run (Reviewer-Friendly)

### Run the core SDT testbed (Neo4j + ETL)
```bash
docker compose up
```

This will:
1.Start the Neo4j container.
2.Bootstrap the semantic schema and demo setup via neo4j/init.cypher.
3.Execute the Python ETL pipeline to ingest sample lifecycle carbon data.

Neo4j Browser: http://localhost:7474

(Default credentials: neo4j / testpassword)

(Optional) Enable workflow orchestration
docker compose --profile orchestration up


This additionally starts the n8n container for demonstrating
agent-based ingestion, orchestration, and reasoning workflows.

Directory Structure
```bash
deployment/docker/
├── docker-compose.yml
├── data/              # BIM / IoT / LCA input datasets (CSV/JSON)
├── etl/
│   └── run_etl.py     # Python ETL entry point
├── outputs/           # Exported results (optional)
├── neo4j/
│   ├── init.cypher    # Constraints, ontology loading, demo queries
│   ├── data/
│   ├── import/
│   └── logs/
└── n8n/               # Optional orchestration workflows
```
Scope and Limitations

This testbed is designed for research reproducibility, not for production deployment. Security hardening, scalability optimization, and full workflow automation are intentionally out of scope and will be addressed in future journal extensions.

---