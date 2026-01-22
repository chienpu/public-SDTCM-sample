# Detailed Repo Structure For SDTCM
```bash
PUBLIC-SDTCM-SAMPLE/
│
├── TH1-ontology/               # Standards-Aligned Ontology (Interoperability)
│   ├── ontology_tbox.ttl
│   ├── ontology_schema.png
│   ├── schema_description.md
│   └── README.md
│
├── TH2-integration/            # Semantic Data Integration (ETL & SHACL)
│   ├── etl_main.py
│   ├── input_data/
│   │   ├── NTU_BuildingX.ifc
│   │   ├── B6_Energy_1month.csv
│   │   └── LCA_sample.xlsx
│   ├── output/
│   │   ├── neo4j_import.csv
│   │   └── validation_report.ttl
│   ├── etl_workflow_diagram.png
│   └── README.md
│
├── TH3-reasoning/              # Reasoning-to-Action (Graph-native Rules)
│   ├── rules/
│   │   ├── anomaly_detection.cypher
│   │   └── maintenance_trigger.cypher
│   ├── n8n_workflow_template.json
│   ├── workflow_execution_log.png
│   └── README.md
│
├── TH4-provenance/             # Provenance Traceability (PROV-O)
│   ├── provenance_query.cypher
│   ├── bloom_lineage_example.png
│   ├── provenance_chain.ttl
│   └── README.md
│
├── TH5-ai_ingestion/           # AI-assisted Ontology & Data Ingestion
│   ├── ai_parser.ipynb
│   ├── lca_input_sample.xlsx
│   ├── generated_triples.ttl
│   ├── refinement_example.png
│   └── README.md
│
├── TH6-deployment/             # Reproducibility (Dockerized System)
│   ├── docker-compose.yml
│   ├── Dockerfile.neo4j
│   ├── Dockerfile.etl
│   ├── Dockerfile.n8n
│   ├── init.sh
│   ├── deployment_overview.png
│   └── README.md
│
├── docker/                     # Optional (Zenodo release, post-acceptance)
│   ├── volumes/
│   │   ├── ontology/
│   │   ├── data/
│   │   ├── workflows/
│   │   └── logs/
│   └── init.sh
│
├── SUMMARY.md                  # Summary of Validation Results (Table 6)
├── LICENSE
└── README.md                   # Main project overview (for reviewer)
```
