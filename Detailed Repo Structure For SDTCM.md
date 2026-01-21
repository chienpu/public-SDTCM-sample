# Detailed Repo Structure For SDTCM

```bash

public-SDTCM-sample/
│
├── TH1-ontology/
│   ├── ontology_schema.png      # Fig. X in paper
│   ├── ontology_core.ttl        # Minimal TBox only
│   └── README.md                # Design rationale & standards alignment
│
├── TH2-integration/
│   ├── integration_workflow.png # ETL / integration diagram (from paper)
│   └── README.md                # Mapping explanation (no code)
│
├── TH3-reasoning/
│   ├── example_rule.cypher      # 1–2 representative rules
│   ├── reasoning_chain.png      # Sensor → Anomaly → Task
│   └── README.md                # Traversal-based reasoning explanation
│
├── TH4-provenance/
│   ├── provenance_pattern.ttl   # Minimal PROV-O pattern
│   ├── lineage_query.cypher     # Example query
│   ├── provenance_example.png
│   └── README.md
│
├── TH6-deployment/
│   ├── deployment_overview.png  # Architecture diagram
│   └── README.md                # Executed by authors; environment-dependent
│
├── SUMMARY.md                   # Table 6 counterpart
├── README.md                    # Reviewer-facing overview
└── LICENSE

```
