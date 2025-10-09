This file does not contain ontology content — only owl:imports declarations.
It’s the semantic equivalent of a “requirements.txt” file in Python.

# 🧭 How to Use This Manifest
## 🪜 Option 1: In Protégé

Open Protégé.

Go to File → Open...

Select sdt_imports.ttl.

Protégé will automatically load all imports listed under owl:imports.

You’ll then see all imported ontologies under
Active Ontology → Ontology imports (SOSA, PROV, IFC, TIME, VOAF).

You can then:

Add your sdt_tbox_s1.ttl as another import (or open it next)

Or merge both (using Refactor → Merge ontologies together)

## 🪜 Option 2: In Neo4j (n10s)

If you’re using Neo4j n10s RDF Import, you can fetch the entire ontology stack in one shot:

```cypher
CALL n10s.graphconfig.init({
  handleVocabUris: "SHORTEN",
  keepLangTag: false,
  handleMultival: "OVERWRITE"
});

CALL n10s.rdf.import.fetch(
  "file:///sdt_imports.ttl", 
  "Turtle"
);
```

Neo4j will read sdt_imports.ttl → detect each owl:imports → and fetch them all automatically (it can follow HTTP URIs).

## 🪜 Option 3: In Dockerized Workflow (Testbed / GitHub Repo)

In your docker-compose.yml stack (for example sam-stride-testbed),
you can mount it inside /import/ and set it as the startup ontology:

```yaml
services:
  neo4j:
    image: neo4j:5
    environment:
      - NEO4JLABS_PLUGINS=["n10s"]
      - NEO4J_apoc_export_file_enabled=true
      - NEO4J_dbms_security_procedures_unrestricted=n10s.*
    volumes:
      - ./ontology:/import
    command: >
      bash -c "
      neo4j-admin dbms set-initial-password test &&
      cypher-shell -u neo4j -p test
        'CALL n10s.graphconfig.init({handleVocabUris:\"SHORTEN\"});
         CALL n10s.rdf.import.fetch(\"file:///import/sdt_imports.ttl\",\"Turtle\");'"

```

# 🧠 Benefits of Using a Manifest
Benefit	Description
Version control	Track which ontology version (e.g., IFC4x3) you used for each experiment
Reproducibility	Anyone cloning your repo can rebuild the ontology graph stack instantly
Portability	Works with Protégé, Neo4j, GraphDB, Fuseki, Stardog — same file
Automation-ready	Ideal for container workflows and CI/CD testing