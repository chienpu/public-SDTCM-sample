# SDT Lifecycle Carbon Ontology — v4 (Academic Complete, TH1–TH6)
**Namespace:** `sdt:` → http://builtinsight.io/ontology/sdt#  
**IFC Core:** Hierarchical (IfcRoot → … → IfcBuildingElement; Project/Site/Building/Storey/Space)

## Import in Neo4j
```cypher
CALL n10s.graphconfig.init({ handleVocabUris:"SHORTEN", handleRDFTypes:"LABELS", handleMultival:"ARRAY" });
CALL n10s.rdf.import.fetch("file:///ontology_tbox_v4.ttl","Turtle");
```

## Import SHACL Shapes (Neo4j n10s) & Validate
```cypher
CALL n10s.validation.shacl.import.fetch("file:///ontology_tbox_v4_shacl.ttl","Turtle");
CALL n10s.validation.shacl.validate();
```

## Quick schema checks
```cypher
MATCH (n) RETURN DISTINCT labels(n) AS labels, COUNT(*) AS cnt ORDER BY cnt DESC;
MATCH (p:owl__ObjectProperty)-[:rdfs__domain]->(d),(p)-[:rdfs__range]->(r)
RETURN p.rdfs__label AS property, d.rdfs__label AS domain, r.rdfs__label AS range
ORDER BY property;
```

## IFC hierarchy traversal
```cypher
// Products located in a given building via recursive spatial chain
MATCH (prod:ifc__IfcProduct)-[:sdt__locatedIn*1..5]->(b:ifc__IfcBuilding)
RETURN prod, b LIMIT 25;

// Building elements and their materials
MATCH (e:ifc__IfcBuildingElement)-[:sdt__hasMaterial]->(m:sdt__Material)
RETURN e, m LIMIT 25;
```

## Embodied (A1–A5) provenance chain
```cypher
MATCH (res:sdt__EmbodiedCarbonResult)-[:prov__wasGeneratedBy]->(act:sdt__EmbodiedActivity),
      (res)-[:sdt__alignedWith]->(mod:sdt__LifecycleModule)
RETURN res, act, mod LIMIT 25;
```

## Operational (B6/B7) observation chain
```cypher
MATCH (asset:ifc__IfcAsset)-[:sdt__hasElectricityConsumption]->(meter:sdt__ElectricityMeter)-[:sosa__madeObservation]->(obs:sosa__Observation),
      (res:sdt__OperationalCarbonResult)-[:prov__wasGeneratedBy]->(act:sdt__OperationalActivity),
      (res)-[:sdt__alignedWith]->(mod:sdt__LifecycleModule)
RETURN asset, meter, obs, res, act, mod LIMIT 25;
```

## Aggregation per lifecycle module
```cypher
MATCH (mod:sdt__LifecycleModule)-[:sdt__aggregates]->(res:sdt__CarbonResult)
RETURN mod.rdfs__label AS module, COUNT(res) AS results ORDER BY results DESC;
```

## Protégé & pySHACL
- Load `ontology_tbox_v4.ttl` and `ontology_tbox_v4_shacl.ttl` as active ontology + shapes graph.
- Run SHACL validation to ensure data (ABox) conforms to SDT rules (A1–A5 vs B6/B7 alignment, provenance, etc.).

## Notes
- Keep ABox in ETL; v4 is TBox + optional module individuals for rules.
- `sdt:ifcGUID` anchors external IFC IDs for joins.
- `sdt:derivedFrom` and `sdt:relatedTo` support integration lineage beyond PROV-O.
