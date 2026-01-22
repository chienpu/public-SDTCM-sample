
# TH1 Validation Cypher Snippets
Developer Guide for Neo4j + Neosemantics Validation of ontology_tbox_v3.ttl

---

## 1️⃣ Basic Graph Statistics

```cypher
// Check number of nodes per label
MATCH (n) 
RETURN DISTINCT labels(n) AS NodeLabel, COUNT(*) AS Count 
ORDER BY Count DESC;

// List all relationships by type
MATCH ()-[r]->() 
RETURN type(r) AS Relationship, COUNT(*) AS Count 
ORDER BY Count DESC;
```

---

## 2️⃣ Class Taxonomy Check

```cypher
// Verify CarbonResult subclass structure
MATCH (n)-[:rdfs__subClassOf]->(m) 
WHERE m.rdfs__label CONTAINS "Carbon Result" 
RETURN n.rdfs__label AS SubClass, m.rdfs__label AS SuperClass;

// Confirm BS EN 15978 lifecycle module hierarchy
MATCH (m:bs__LifecycleModule) 
RETURN m.rdfs__label AS ModuleName 
ORDER BY ModuleName;
```

---

## 3️⃣ Property Integrity and Alignment

```cypher
// Show all object properties with domain and range
MATCH (p:owl__ObjectProperty)-[:rdfs__domain]->(d),
      (p)-[:rdfs__range]->(r)
RETURN p.rdfs__label AS Property, d.rdfs__label AS Domain, r.rdfs__label AS Range;

// Count datatype properties
MATCH (p:owl__DatatypeProperty) RETURN COUNT(p) AS DatatypePropertyCount;
```

---

## 4️⃣ Embodied Carbon Path Validation (A1–A5)

```cypher
// Verify material linkage and emission factor alignment
MATCH (b:ifc__IfcBuildingElement)-[:bs__hasMaterial]->(m:bs__Material),
      (m)<-[:bs__hasEmissionFactor]-(q:bs__ActivityQuantity)
RETURN b.rdfs__label AS BuildingElement, m.rdfs__label AS Material, q.rdfs__label AS Quantity;

// Verify CarbonResult → wasGeneratedBy → Activity
MATCH (c:bs__EmbodiedCarbonResult)-[:prov__wasGeneratedBy]->(a:prov__Activity)
RETURN c.rdfs__label AS CarbonResult, a.rdfs__label AS Activity;
```

---

## 5️⃣ Operational Carbon Path Validation (B6–B7)

```cypher
// Check Asset → Observation → LifecycleModule alignment
MATCH (asset:ifc__IfcAsset)-[:bs__hasObservation]->(obs:sosa__Observation),
      (obs)-[:prov__wasGeneratedBy]->(act:prov__Activity)
RETURN asset.rdfs__label AS Asset, obs.rdfs__label AS Observation, act.rdfs__label AS Activity;

// Verify OperationalCarbonResult → alignedWith → LifecycleModule (B6/B7)
MATCH (c:bs__OperationalCarbonResult)-[:bs__alignedWith]->(l:bs__LifecycleModule)
RETURN c.rdfs__label AS CarbonResult, l.rdfs__label AS Module;
```

---

## 6️⃣ Provenance Path Verification

```cypher
// Trace full provenance chain
MATCH (r:bs__CarbonResult)-[:prov__wasGeneratedBy]->(a:prov__Activity)-[:prov__used]->(s:rdfs__Resource)
RETURN r.rdfs__label AS Result, a.rdfs__label AS Activity, s.rdfs__label AS Source;

// Verify attribution (agent involvement)
MATCH (r:bs__CarbonResult)-[:prov__wasAttributedTo]->(ag:prov__Agent)
RETURN r.rdfs__label AS Result, ag.rdfs__label AS Agent;
```

---

## 7️⃣ Visualization & Bloom Setup

```cypher
// Suggest Bloom perspective grouping
// Group 1: LifecycleModule, CarbonResult, Activity
// Group 2: IfcBuildingElement, Material, EmissionFactor
// Group 3: IfcAsset, Observation, Sensor, Agent
MATCH (n) RETURN DISTINCT labels(n) AS Labels LIMIT 50;
```

---

✅ **Usage Notes**
1. Ensure `ontology_tbox_v3.ttl` is imported using:
```cypher
CALL n10s.graphconfig.init({ handleVocabUris:"SHORTEN", handleRDFTypes:"LABELS", handleMultival:"ARRAY" });
CALL n10s.rdf.import.fetch("file:///ontology_tbox_v3.ttl","Turtle");
```
2. Use this validation script in Neo4j Browser or Neo4j Bloom to confirm graph coherence and visualize the ontology-level relationships.
3. Ideal for TH1 interoperability demonstration.

---
© 2025 BuiltInsight | SDT Framework Ontology Validation Script
