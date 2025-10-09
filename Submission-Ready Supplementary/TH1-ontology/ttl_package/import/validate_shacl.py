#################################################################
# Semantic Digital Thread – SHACL Validation Script (Enhanced)
# File: validate_shacl.py
# Description:
#   Validates RDF data (e.g., SDT ontology instances) against SHACL
#   shapes and computes instance correctness (% of valid instances).
#################################################################

import sys
import os
import csv
from rdflib import Graph
from pyshacl import validate

# ---------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------
DATA_FILE = "import/dataset/ntu_campus_sample.ttl"
SHACL_FILE = "import/sdt_tbox_s1.ttl"
OUTPUT_CSV = "validation_report.csv"

# ---------------------------------------------------------------
# MAIN VALIDATION FUNCTION
# ---------------------------------------------------------------

def run_shacl_validation(data_file=DATA_FILE, shacl_file=SHACL_FILE, output_csv=OUTPUT_CSV):
    print("🔍 Loading RDF data...")
    data_graph = Graph().parse(data_file, format="turtle")

    print("🧩 Loading SHACL shapes...")
    shacl_graph = Graph().parse(shacl_file, format="turtle")

    print("⚙️  Running SHACL validation (this may take a moment)...")
    conforms, report_graph, report_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        debug=False
    )

    print("\n✅ Conforms:" if conforms else "\n❌ Violations detected!")
    print("Validation Report")
    print(report_text)

    # -----------------------------------------------------------
    # Extract SHACL validation results into CSV
    # -----------------------------------------------------------
    print("\n🧾 Exporting CSV report...")

    qres = report_graph.query(
        """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        SELECT ?focusNode ?resultPath ?resultMessage ?sourceShape
        WHERE {
            ?vr a sh:ValidationResult ;
                sh:focusNode ?focusNode ;
                sh:resultMessage ?resultMessage ;
                sh:sourceShape ?sourceShape .
            OPTIONAL { ?vr sh:resultPath ?resultPath . }
        }
        """
    )

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["focusNode", "resultPath", "resultMessage", "sourceShape"])
        for row in qres:
            writer.writerow([str(x) if x else "" for x in row])

    print(f"📂 Validation results exported to: {output_csv}")

    # -----------------------------------------------------------
    # Compute instance correctness (simple ratio)
    # -----------------------------------------------------------
    total_instances = len(set(data_graph.subjects()))  # count all RDF subjects
    violation_count = sum(1 for _ in open(output_csv, encoding="utf-8")) - 1  # minus header
    valid_instances = max(total_instances - violation_count, 0)
    correctness_rate = (valid_instances / total_instances) * 100 if total_instances > 0 else 0

    print(f"\n📊 Instance correctness: {correctness_rate:.2f}%")
    print(f"🧩 Total instances: {total_instances}, Violations: {violation_count}")
    print("Done ✅")

# ---------------------------------------------------------------
# COMMAND-LINE ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    data_arg = sys.argv[1] if len(sys.argv) > 1 else DATA_FILE
    shacl_arg = sys.argv[2] if len(sys.argv) > 2 else SHACL_FILE
    output_arg = sys.argv[3] if len(sys.argv) > 3 else OUTPUT_CSV
    run_shacl_validation(data_arg, shacl_arg, output_arg)
