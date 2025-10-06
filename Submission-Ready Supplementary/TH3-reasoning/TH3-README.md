# TH3 — Reasoning-to-Action Automation

## 🎯 Validation Objective
To evaluate whether semantic reasoning in Neo4j can autonomously trigger workflow actions for predictive maintenance or anomaly detection.

---

## 🧠 Method Overview
- Cypher/APOC rules define threshold-based energy anomaly detection (Module B6).
- Reasoning results passed to **n8n** via HTTP trigger.
- n8n workflow creates corresponding maintenance tasks with provenance logging.

---

## 📊 Key Results
| Metric | Result |
|---------|---------|
| Precision | 95 % |
| Recall | 90 % |
| Avg. Reasoning Latency | 0.8 s/query |
| Workflow Execution Success | 100 % |

---

## 🗂️ Artifacts
- `reasoning_rules.cypher` — Cypher logic for anomaly detection  
- `maintenance_trigger.cypher` — Action trigger queries  
- `n8n_workflow_template.json` — Workflow definition  
- `workflow_execution_log.png` — Screenshot of triggered tasks  

---

## 🔗 Relation to Other Layers
- **Uses:** `/TH2-integration/` outputs  
- **Logged by:** `/TH4-provenance/`

---

## 🧩 Validation Outcome
✅ Confirmed reliable mapping from semantic inference → automated action.  
Bridges reasoning and FM workflow within the SDT architecture.
