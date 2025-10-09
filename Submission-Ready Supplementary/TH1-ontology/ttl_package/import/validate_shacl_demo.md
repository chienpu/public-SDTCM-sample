# Semantic Digital Thread (SDT) SHACL Validation Demo

This repository provides a working example for validating **SDT ontology data** using **SHACL rules** with `pySHACL`.

---

## 📦 Included Files

```
/import/
   ├─ sdt_tbox_s1.ttl              ← ontology + SHACL shapes
   ├─ sdt_imports_local.ttl        ← offline ontology import manifest
   ├─ dataset/
   │    └─ ntu_campus_sample.ttl   ← demo dataset (valid + invalid data)
   ├─ validate_shacl.py            ← validation script
   └─ validation_report.csv        ← output after running validation
```

---

## 🧭 How to Use

### 1️⃣ Install Dependencies

```bash
pip install rdflib pyshacl
```

---

### 2️⃣ Run Validation

#### Option A – Validate ontology (embedded SHACL)

```bash
python validate_shacl.py import/sdt_tbox_s1.ttl import/sdt_tbox_s1.ttl
```

#### Option B – Validate a dataset against SHACL rules

```bash
python validate_shacl.py import/dataset/ntu_campus_sample.ttl import/sdt_tbox_s1.ttl
```

---

### 3️⃣ Review Results

After execution, a `validation_report.csv` file will be generated with details like:

| focusNode                 | resultPath                | resultMessage                                          | sourceShape                |
| ------------------------- | ------------------------- | ------------------------------------------------------ | -------------------------- |
| sdt:Obs001                | sosa:hasFeatureOfInterest | "Each Observation must indicate its observed Asset."   | sdt:ObservationShape       |
| sdt:OperationalCarbon_001 | sdt:hasModule             | "Operational carbon results must belong to module B6." | sdt:OperationalResultShape |

---

## 🧠 How It Works

* **rdflib** loads RDF/OWL data and SHACL constraints.
* **pySHACL** performs SHACL 1.1 validation with RDFS inference.
* The results graph is exported into a structured `.csv` file.

---

## 🧩 Sample Dataset – `ntu_campus_sample.ttl`

This dataset demonstrates both a valid and an invalid observation.

```ttl
@prefix sdt: <http://builtinsight.io/ontology/sdt#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# ✅ Valid Observation
sdt:Obs001 a sosa:Observation ;
    sosa:hasFeatureOfInterest sdt:Asset001 ;
    sosa:observedProperty sdt:ElectricityUsage ;
    sosa:resultTime "2024-05-01T08:00:00Z"^^xsd:dateTime ;
    sosa:hasResult sdt:PerformanceData001 .

sdt:Asset001 a sdt:Asset ;
    sdt:hasModule sdt:ModuleB6 ;
    sdt:assetName "NTU Civil Engineering Building" .

# ⚠️ Invalid Observation (missing hasFeatureOfInterest)
sdt:Obs002 a sosa:Observation ;
    sosa:observedProperty sdt:ElectricityUsage ;
    sosa:resultTime "2024-05-01T09:00:00Z"^^xsd:dateTime ;
    sosa:hasResult sdt:PerformanceData002 .

sdt:PerformanceData001 a sdt:PerformanceData ;
    sdt:hasQuantity "125.6"^^xsd:decimal .

sdt:PerformanceData002 a sdt:PerformanceData ;
    sdt:hasQuantity "131.4"^^xsd:decimal .
```

When validated, `sdt:Obs002` will trigger a SHACL violation message indicating that it lacks `sosa:hasFeatureOfInterest`.
