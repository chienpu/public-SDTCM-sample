
# TH1–TH6 SHACL Test & Validation Guide (NTU Campus Edition, MERGE-safe)
**Ontology:** `ontology_tbox_v4.ttl` (SDT namespace `sdt:`)  
**SHACL:** `ontology_tbox_v4_shacl.ttl`  
**Context:** NTU campus placeholders; **all Cypher uses MERGE** for idempotent re-runs.

> Run these after importing ontology & shapes:
> ```cypher
> CALL n10s.graphconfig.init({ handleVocabUris:"SHORTEN", handleRDFTypes:"LABELS", handleMultival:"ARRAY" });
> CALL n10s.rdf.import.fetch("file:///ontology_tbox_v4.ttl","Turtle");
> CALL n10s.validation.shacl.import.fetch("file:///ontology_tbox_v4_shacl.ttl","Turtle");
> ```

---

## TH1 — Standards‑Aligned Ontology (A1–D linkage)

### 🎯 Goal
Each `sdt:CarbonResult` must be aligned to a valid `sdt:LifecycleModule` and record provenance.

### 🧱 MERGE ABox (NTU)
```cypher
MERGE (res:sdt__EmbodiedCarbonResult { id:"NTU_A1_CR_001" })
  SET res.sdt__value = 125.5, res.sdt__unit = "kgCO2e"
MERGE (mod:sdt__A1 { id:"A1_Class" })
MERGE (act:sdt__EmbodiedActivity { id:"NTU_EmbodiedAct_001" })
MERGE (res)-[:sdt__alignedWith]->(mod)
MERGE (res)-[:prov__wasGeneratedBy]->(act);
```

### ✅ Validate & Interpret
```cypher
CALL n10s.validation.shacl.validate();
```
- Expect **Valid** under **`sdt:CarbonResultShape`** and **`sdt:EmbodiedResultShape`**.  
- If `prov:wasGeneratedBy` missing → violation from `sdt:CarbonResultShape`.

---

## TH2 — Semantic Integration (IFC × SDT)

### 🎯 Goal
IFC hierarchy connected to SDT: IfcProject → Site → Building → Storey → Space → BuildingElement.

### 🧱 MERGE ABox (NTU)
```cypher
MERGE (proj:ifc__IfcProject { id:"NTU_Project_01" })
MERGE (site:ifc__IfcSite { id:"NTU_Site_01" })-[:sdt__belongsToProject]->(proj)
MERGE (bldg:ifc__IfcBuilding { id:"NTU_Building_A" })-[:sdt__locatedIn]->(site)
MERGE (story:ifc__IfcBuildingStorey { id:"NTU_BldgA_L2" })-[:sdt__locatedIn]->(bldg)
MERGE (space:ifc__IfcSpace { id:"NTU_BldgA_L2_201" })-[:sdt__locatedIn]->(story)

MERGE (elem:ifc__IfcBuildingElement { id:"NTU_Column_C201" })
  SET elem.sdt__ifcGUID = "3uK1$Xa9P9FQ8pV2"
MERGE (elem)-[:sdt__locatedIn]->(space)

MERGE (mat:sdt__Material { id:"NTU_Material_Concrete" })
MERGE (elem)-[:sdt__hasMaterial]->(mat);
```

### ✅ Validate & Traverse
```cypher
CALL n10s.validation.shacl.validate();

MATCH (e:ifc__IfcBuildingElement {id:"NTU_Column_C201"})-[:sdt__locatedIn*1..5]->(b:ifc__IfcBuilding)
RETURN e,b;
```

- Shape checked: **`sdt:IfcBuildingElementMaterialShape`**.

---

## TH3 — Reasoning‑to‑Action (Embodied & Operational)

### 🎯 Goal
Embodied uses `ActivityQuantity` + `EmissionFactor`; Operational uses `Observation` + `EmissionFactor`.

### 🧱 MERGE ABox (NTU)
```cypher
// Embodied
MERGE (q:sdt__ActivityQuantity { id:"NTU_Q_Concrete_1" }) SET q.sdt__unit="m3"
MERGE (f:sdt__EmissionFactor { id:"EF_Concrete" }) SET f.sdt__unit="kgCO2e/m3"
MERGE (aE:sdt__EmbodiedActivity { id:"NTU_EmbodiedAct_002" })
MERGE (aE)-[:prov__used]->(q)
MERGE (aE)-[:prov__used]->(f)
MERGE (rE:sdt__EmbodiedCarbonResult { id:"NTU_CR_Emb_002" })
  SET rE.sdt__value=950.0, rE.sdt__unit="kgCO2e"
MERGE (rE)-[:prov__wasGeneratedBy]->(aE)
MERGE (rE)-[:sdt__alignedWith]->(:sdt__A3)

// Operational
MERGE (meter:sdt__ElectricityMeter { id:"NTU_Sensor_Elec_MainHall" })
MERGE (obs:sosa__Observation { id:"NTU_Obs_2024_07" })
  SET obs.sdt__value=12000.0, obs.sdt__unit="kWh"
MERGE (meter)-[:sosa__madeObservation]->(obs)
MERGE (aO:sdt__OperationalActivity { id:"NTU_OperationalAct_001" })
MERGE (efO:sdt__EmissionFactor { id:"EF_Grid_2024" }) SET efO.sdt__unit="kgCO2e/kWh"
MERGE (aO)-[:prov__used]->(obs)
MERGE (aO)-[:prov__used]->(efO)
MERGE (rO:sdt__OperationalCarbonResult { id:"NTU_CR_Op_001" })
  SET rO.sdt__value=5400.0, rO.sdt__unit="kgCO2e"
MERGE (rO)-[:prov__wasGeneratedBy]->(aO)
MERGE (rO)-[:sdt__alignedWith]->(:sdt__B6);
```

### ✅ Validate & Interpret
```cypher
CALL n10s.validation.shacl.validate();
```
- Shapes checked: **`sdt:EmbodiedActivityShape`**, **`sdt:OperationalActivityShape`**, **`sdt:OperationalResultShape`**.

---

## TH4 — Provenance Traceability

### 🎯 Goal
Entity → Activity → Result → Module chain remains queryable and validated.

### 🧱 MERGE ABox (NTU)
```cypher
MERGE (agent:prov__Agent { id:"NTU_EnergyTeam" })
MATCH (aO:sdt__OperationalActivity { id:"NTU_OperationalAct_001" }),
      (rO:sdt__OperationalCarbonResult { id:"NTU_CR_Op_001" })
MERGE (aO)-[:prov__wasAssociatedWith]->(agent)
MERGE (rO)-[:prov__wasGeneratedBy]->(aO);
```

### ✅ Validate & Trace
```cypher
CALL n10s.validation.shacl.validate();

MATCH (res:sdt__CarbonResult)-[:prov__wasGeneratedBy]->(act:prov__Activity)-[:prov__used]->(src)
RETURN res.id AS result, labels(act) AS activityType, src.id AS input LIMIT 20;
```

- Shape checked: **`sdt:CarbonResultShape`** (prov:wasGeneratedBy).

---

## TH5 — Aggregation / Roll‑Up

### 🎯 Goal
Lifecycle modules aggregate multiple results for roll-up.

### 🧱 MERGE ABox (NTU)
```cypher
MERGE (mB6:sdt__B6 { id:"Module_B6" })
MATCH (r1:sdt__OperationalCarbonResult { id:"NTU_CR_Op_001" })
MERGE (r2:sdt__OperationalCarbonResult { id:"NTU_CR_Op_002" })
  SET r2.sdt__value = 2750.0, r2.sdt__unit = "kgCO2e"
MERGE (mB6)-[:sdt__aggregates]->(r1)
MERGE (mB6)-[:sdt__aggregates]->(r2);
```

### ✅ Validate & Sum
```cypher
CALL n10s.validation.shacl.validate();

MATCH (mod:sdt__LifecycleModule {id:"Module_B6"})-[:sdt__aggregates]->(res:sdt__CarbonResult)
RETURN mod.id, COUNT(res) AS results, SUM(res.sdt__value) AS total_kgCO2e;
```

- Shape checked: **`sdt:LifecycleAggregatesShape`**.

---

## TH6 — System Integration (IFC × SOSA)

### 🎯 Goal
Asset → Meter → Observation → FOI chain exists and validates.

### 🧱 MERGE ABox (NTU)
```cypher
MERGE (asset:ifc__IfcAsset { id:"NTU_Building_A_Asset" })
MERGE (meter:sdt__ElectricityMeter { id:"NTU_Sensor_Elec_MainHall" })
MERGE (obs:sosa__Observation { id:"NTU_Obs_2024_07" })
MERGE (asset)-[:sdt__hasElectricityConsumption]->(meter)
MERGE (meter)-[:sosa__madeObservation]->(obs)
MERGE (foi:sosa__FeatureOfInterest { id:"NTU_Building_A_FOI" })
MERGE (obs)-[:sosa__hasFeatureOfInterest]->(foi);
```

### ✅ Validate & Inspect
```cypher
CALL n10s.validation.shacl.validate();

MATCH (asset:ifc__IfcAsset {id:"NTU_Building_A_Asset"})-[:sdt__hasElectricityConsumption]->(m:sdt__ElectricityMeter)
MATCH (m)-[:sosa__madeObservation]->(o:sosa__Observation)-[:sosa__hasFeatureOfInterest]->(f:sosa__FeatureOfInterest)
RETURN asset, m, o, f;
```
- Shapes checked: **`sdt:AssetB6Shape`**, **`sdt:ElectricityMeterShape`**, **`sdt:ObservationFOIShape`**.

---

## Cleanup Helper (optional, MERGE-safe environment)
```cypher
MATCH (n) WHERE n.id STARTS WITH "NTU_" OR n.id STARTS WITH "Module_"
DETACH DELETE n;
CALL db.clearQueryCaches();
```

> Tip: If a validation fails, the output includes the **NodeShape IRI** (e.g., `sdt:OperationalResultShape`) and the human‑readable message you can cite in your appendix.
