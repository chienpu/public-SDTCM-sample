"""
SDT ETL Runner
--------------
Ontology-driven ETL for Semantic Digital Thread (SDT)
Lifecycle Carbon Management testbed

This script:
1. Loads ontology-aligned lifecycle carbon data (CSV / JSON)
2. Instantiates ABox entities in Neo4j
3. Attaches basic provenance metadata for auditability

NOTE:
- This is a research-grade, reproducible ETL runner.
- Data schemas are assumed to be ontology-aligned beforehand.
"""

import os
import csv
from neo4j import GraphDatabase
from datetime import datetime

# -------------------------------------------------------------------
# Neo4j connection (provided via docker-compose environment variables)
# -------------------------------------------------------------------

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "testpassword")

driver = GraphDatabase.driver(
    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# -------------------------------------------------------------------
# Paths & configuration
# -------------------------------------------------------------------

DATA_DIR = "./data"
PIPELINE_NAME = os.getenv("SDT_PIPELINE", "demo_lifecycle_carbon")
INGESTION_TIME = datetime.utcnow().isoformat()

# -------------------------------------------------------------------
# Helper: create provenance node
# -------------------------------------------------------------------

def create_provenance(tx, source_file):
    tx.run(
        """
        MERGE (p:ProvenanceActivity {
            name: $pipeline,
            executedAt: datetime($time),
            source: $source
        })
        """,
        pipeline=PIPELINE_NAME,
        time=INGESTION_TIME,
        source=source_file
    )

# -------------------------------------------------------------------
# ETL Step: ingest lifecycle carbon items (example CSV)
# -------------------------------------------------------------------

def ingest_carbon_items(tx, rows):
    for r in rows:
        tx.run(
            """
            MERGE (c:CarbonItem {id: $id})
            SET c.stage = $stage,
                c.quantity = $qty,
                c.unit = $unit
            """,
            id=r["carbon_id"],
            stage=r["lifecycle_stage"],
            qty=float(r["quantity"]),
            unit=r["unit"]
        )

# -------------------------------------------------------------------
# Main ETL pipeline
# -------------------------------------------------------------------

def run():
    print("Starting SDT ETL pipeline...")
    print(f"Pipeline: {PIPELINE_NAME}")

    carbon_file = os.path.join(DATA_DIR, "carbon_items.csv")

    if not os.path.exists(carbon_file):
        raise FileNotFoundError(
            "Expected data file not found: carbon_items.csv"
        )

    with open(carbon_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with driver.session() as session:
        session.execute_write(create_provenance, "carbon_items.csv")
        session.execute_write(ingest_carbon_items, rows)

    print("ETL completed successfully.")
    print(f"Ingested {len(rows)} CarbonItem instances.")

# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    run()
