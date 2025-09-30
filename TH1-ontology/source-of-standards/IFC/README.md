# IFC4x3 Schema Extractor
This project provides a Python script (extract_ifc43_schema.py) that automatically extracts the structure, attributes, and definitions of all IfcXXX entities from the official **IFC4x3 documentation** on the buildingSMART website. The script then exports this data into a CSV format, making it easy to import into Neo4j or other knowledge graph platforms.

---

## 🔧 Setup

### 1. Create a Virtual Environment
First, create and activate a virtual environment within the project folder:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows PowerShell
source .venv/bin/activate   # Linux / macOS
```

### 2. Install Dependencies
Next, install the required packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```bash
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

---

## ▶️ How to Run

To run the script, use the following command:

```bash
python extract_ifc43_schema.py
```

The script's process is as follows:
1. It automatically parses `toc.html` to find all sub-schema `content.html` pages.
2. It scrapes the list of `IfcXXX` entities from each sub-schema.
3. It navigates to each entity's page to extract its **definition** and **attributes**.
4. It exports the data to a file named `IFC4x3_full_schema.csv`.

Example of the output file:

| Entity   | Definition              | Attr_Name   | Attr_Type               | Attr_Desc                  |
|----------|-------------------------|-------------|-------------------------|----------------------------|
| IfcWall  | A wall is a vertical... | GlobalId    | IfcGloballyUniqueId     | Assignment of GUID         |
| IfcWall  | ...                     | OwnerHistory| IfcOwnerHistory         | Information about creation |

---

## 📥 Import into Neo4j

To import the `IFC4x3_full_schema.csv` file into Neo4j, use the following Cypher query:

```cypher
LOAD CSV WITH HEADERS FROM 'file:///IFC4x3_full_schema.csv' AS row
MERGE (e:IFCEntity {name: row.Entity})
  ON CREATE SET e.definition = row.Definition
MERGE (a:IFCAttribute {name: row.Attr_Name, datatype: row.Attr_Type})
  ON CREATE SET a.description = row.Attr_Desc
MERGE (e)-[:HAS_ATTRIBUTE]->(a);
```

This query will create the following in your Neo4j database:
- A node for each `(:IFCEntity {name, definition})`
- A node for each `(:IFCAttribute {name, datatype, description})`
- A `[:HAS_ATTRIBUTE]` relationship connecting each entity to its attributes. `(:IFCEntity)-[:HAS_ATTRIBUTE]->(:IFCAttribute)`

---

## 🚀 Use Cases

- Serves as a foundational ontology for a **Semantic Digital Thread**.
- Supports information modeling for **Lifecycle Carbon Management**.
- Enables the integration of IoT data by linking with the **SOSA/SSN Observation Event** ontology.

---

## ⚠️ Important Notes
- The official server can occasionally return 500/404 errors; the script is designed to automatically skip these pages.
- To extract all entities, you can set `LIMIT = 0` in the script.
