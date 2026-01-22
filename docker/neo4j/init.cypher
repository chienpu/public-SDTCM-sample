// ============================================================================
// SDT Reproducibility Testbed (Lifecycle Carbon Management) - init.cypher
// Neo4j 5.x compatible
//
// Purpose:
//  (1) Bootstrap constraints & indexes
//  (2) Provide a minimal SDT semantic backbone projection (TBox-like scaffolding)
//  (3) Seed a tiny demo ABox instance set for immediate reproducible queries
//  (4) Enable reasoning/provenance-ready patterns (PROV-style nodes/edges)
//
// Notes:
//  - This is a research reproducibility bootstrap (not production).
//  - "Ontology" here is realized as a minimal executable graph schema + constraints.
// ============================================================================


// ----------------------------------------------------------------------------
// 0) CONSTRAINTS (id-based uniqueness)
// ----------------------------------------------------------------------------
CREATE CONSTRAINT buildingElement_id IF NOT EXISTS
FOR (n:BuildingElement) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT asset_id IF NOT EXISTS
FOR (n:Asset) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT observation_id IF NOT EXISTS
FOR (n:Observation) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT carbonItem_id IF NOT EXISTS
FOR (n:CarbonItem) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT lifecycleStage_code IF NOT EXISTS
FOR (n:LifecycleStage) REQUIRE n.code IS UNIQUE;

CREATE CONSTRAINT emissionFactor_id IF NOT EXISTS
FOR (n:EmissionFactor) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT workflowTask_id IF NOT EXISTS
FOR (n:WorkflowTask) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT provActivity_id IF NOT EXISTS
FOR (n:ProvenanceActivity) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT provAgent_id IF NOT EXISTS
FOR (n:ProvenanceAgent) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT provEntity_id IF NOT EXISTS
FOR (n:ProvenanceEntity) REQUIRE n.id IS UNIQUE;


// ----------------------------------------------------------------------------
// 1) INDEXES (query performance for common SDT patterns)
// ----------------------------------------------------------------------------
CREATE INDEX carbonItem_stage IF NOT EXISTS
FOR (n:CarbonItem) ON (n.stage);

CREATE INDEX observation_time IF NOT EXISTS
FOR (n:Observation) ON (n.observedAt);

CREATE INDEX workflowTask_status IF NOT EXISTS
FOR (n:WorkflowTask) ON (n.status);

CREATE INDEX asset_type IF NOT EXISTS
FOR (n:Asset) ON (n.assetType);


// ----------------------------------------------------------------------------
// 2) MINIMAL "TBox" SCAFFOLDING (optional, for readability / documentation)
//    This is NOT a full OWL export; it is a lightweight in-graph schema guide.
// ----------------------------------------------------------------------------
MERGE (t:SDT_TBox {name: "SDT_LifecycleCarbon_TBox"})
SET t.alignedStandards = ["BS EN 15978", "IFC (ISO 16739-1)", "SOSA/SSN"],
    t.scope = "Lifecycle carbon management with graph-native reasoning and auditable provenance",
    t.version = "0.1";

UNWIND [
  "BuildingElement",
  "Asset",
  "Observation",
  "CarbonItem",
  "LifecycleStage",
  "EmissionFactor",
  "WorkflowTask",
  "ProvenanceActivity",
  "ProvenanceAgent",
  "ProvenanceEntity"
] AS cls
MERGE (c:Class {name: cls})
MERGE (t)-[:DECLARES_CLASS]->(c);

UNWIND [
  {name:"HAS_LOCATION", from:"BuildingElement", to:"Location"},
  {name:"PART_OF_SYSTEM", from:"BuildingElement", to:"System"},
  {name:"MONITORED_BY", from:"Asset", to:"Sensor"},
  {name:"MADE_BY_SENSOR", from:"Observation", to:"Sensor"},
  {name:"HAS_RESULT", from:"Observation", to:"Result"},
  {name:"PART_OF_STAGE", from:"CarbonItem", to:"LifecycleStage"},
  {name:"LINKED_TO_FACTOR", from:"CarbonItem", to:"EmissionFactor"},
  {name:"TRIGGERED_BY", from:"WorkflowTask", to:"Observation"},
  {name:"ASSOCIATED_WITH_ASSET", from:"WorkflowTask", to:"Asset"},
  {name:"PROV_USED", from:"ProvenanceActivity", to:"ProvenanceEntity"},
  {name:"PROV_GENERATED", from:"ProvenanceActivity", to:"ProvenanceEntity"},
  {name:"PROV_ASSOCIATED_WITH", from:"ProvenanceActivity", to:"ProvenanceAgent"}
] AS r
MERGE (rel:Relation {name: r.name})
SET rel.domain = r.from, rel.range = r.to
MERGE (t)-[:DECLARES_RELATION]->(rel);


// ----------------------------------------------------------------------------
// 3) SEED LIFECYCLE STAGES (BS EN 15978 oriented)
// ----------------------------------------------------------------------------
UNWIND [
  {code:"B2", name:"Maintenance"},
  {code:"B4", name:"Replacement"},
  {code:"B6", name:"Operational energy use"}
] AS s
MERGE (st:LifecycleStage {code: s.code})
SET st.name = s.name,
    st.standard = "BS EN 15978";


// ----------------------------------------------------------------------------
// 4) SEED EMISSION FACTORS (illustrative; replace with your dataset if needed)
// ----------------------------------------------------------------------------
UNWIND [
  {id:"EF_ELEC_GRID", name:"Electricity (grid)", unit:"kgCO2e/kWh", value:0.5},
  {id:"EF_FILTER",    name:"HVAC filter",       unit:"kgCO2e/unit", value:12.3}
] AS ef
MERGE (f:EmissionFactor {id: ef.id})
SET f.name = ef.name,
    f.unit = ef.unit,
    f.value = ef.value,
    f.source = "demo";


// ----------------------------------------------------------------------------
// 5) SEED A TINY DEMO ABox (BIM/Asset + Observation + CarbonItem + Task)
// ----------------------------------------------------------------------------

// 5.1 Building element & asset (IFC-aligned anchor)
MERGE (be:BuildingElement {id:"BE_AHU_ROOM_01"})
SET be.ifcType = "IfcSpace",
    be.name = "AHU Room 01",
    be.stageHint = "B6";

MERGE (a:Asset {id:"ASSET_AHU_01"})
SET a.name = "Air Handling Unit 01",
    a.assetType = "HVAC_AHU",
    a.locationRef = "BE_AHU_ROOM_01";

MERGE (a)-[:LOCATED_IN]->(be);

// 5.2 Observation (SOSA-style)
MERGE (o:Observation {id:"OBS_0001"})
SET o.metric = "Power",
    o.value = 35.0,
    o.unit = "kW",
    o.observedAt = datetime("2026-01-22T12:00:00Z"),
    o.source = "demo_sensor_stream";

MERGE (a)-[:HAS_OBSERVATION]->(o);

// 5.3 Carbon items (EN 15978 accounting units)
MERGE (ci1:CarbonItem {id:"CI_B6_ELEC_0001"})
SET ci1.quantity = 1000.0,
    ci1.unit = "kWh",
    ci1.stage = "B6",
    ci1.description = "Operational electricity consumption";

MERGE (ci2:CarbonItem {id:"CI_B4_FILTER_0001"})
SET ci2.quantity = 1.0,
    ci2.unit = "unit",
    ci2.stage = "B4",
    ci2.description = "Filter replacement";

MATCH (b6:LifecycleStage {code:"B6"})
MATCH (b4:LifecycleStage {code:"B4"})
MATCH (efElec:EmissionFactor {id:"EF_ELEC_GRID"})
MATCH (efFilter:EmissionFactor {id:"EF_FILTER"})
MERGE (ci1)-[:PART_OF_STAGE]->(b6)
MERGE (ci2)-[:PART_OF_STAGE]->(b4)
MERGE (ci1)-[:LINKED_TO_FACTOR]->(efElec)
MERGE (ci2)-[:LINKED_TO_FACTOR]->(efFilter)
MERGE (a)-[:HAS_CARBON_ITEM]->(ci1)
MERGE (a)-[:HAS_CARBON_ITEM]->(ci2);

// 5.4 A minimal "reasoning-to-action" artifact (WorkflowTask)
MERGE (t1:WorkflowTask {id:"TASK_0001"})
SET t1.type = "Inspect_AHU",
    t1.status = "Open",
    t1.createdAt = datetime("2026-01-22T12:05:00Z"),
    t1.triggerRule = "Power > threshold";

MERGE (t1)-[:TRIGGERED_BY]->(o)
MERGE (t1)-[:ASSOCIATED_WITH_ASSET]->(a);


// ----------------------------------------------------------------------------
// 6) PROVENANCE SEED (PROV-style; minimal but auditable)
// ----------------------------------------------------------------------------

// Agent (who)
MERGE (agent:ProvenanceAgent {id:"AGENT_ETL"})
SET agent.name = "Python ETL Runner",
    agent.role = "Ingestion";

// Entities (what)
MERGE (e1:ProvenanceEntity {id:"ENTITY_carbon_items_csv"})
SET e1.name = "carbon_items.csv",
    e1.entityType = "Dataset",
    e1.location = "/deployment/docker/data/carbon_items.csv";

// Activity (how/when)
MERGE (act:ProvenanceActivity {id:"ACT_INGEST_0001"})
SET act.name = "Ingest lifecycle carbon dataset",
    act.executedAt = datetime("2026-01-22T12:02:00Z"),
    act.tool = "run_etl.py";

// Provenance links
MERGE (act)-[:PROV_ASSOCIATED_WITH]->(agent)
MERGE (act)-[:PROV_USED]->(e1)
MERGE (act)-[:PROV_GENERATED]->(ci1)
MERGE (act)-[:PROV_GENERATED]->(ci2);


// ----------------------------------------------------------------------------
// 7) OPTIONAL: CREATE A VIEW-LIKE SUMMARY NODE (for quick demo queries)
// ----------------------------------------------------------------------------
MERGE (s:SDTSummary {id:"SUMMARY_0001"})
SET s.note = "Convenience summary node for reproducible demo queries";

MATCH (a:Asset {id:"ASSET_AHU_01"})
MERGE (s)-[:SUMMARIZES]->(a);


// ----------------------------------------------------------------------------
// 8) DEMO QUERIES (comments only; run in Neo4j Browser)
// ----------------------------------------------------------------------------
//
// (Q1) Compute carbon for B6 electricity item:
// MATCH (c:CarbonItem {id:"CI_B6_ELEC_0001"})-[:LINKED_TO_FACTOR]->(f:EmissionFactor)
// RETURN c.id, c.quantity, c.unit, f.value AS factor, (c.quantity * f.value) AS kgCO2e;
//
// (Q2) List lifecycle carbon items by stage for an asset:
// MATCH (a:Asset {id:"ASSET_AHU_01"})-[:HAS_CARBON_ITEM]->(c:CarbonItem)-[:PART_OF_STAGE]->(s:LifecycleStage)
// RETURN a.id, s.code AS stage, c.id, c.quantity, c.unit, c.description
// ORDER BY stage;
//
// (Q3) Traceability: show task trigger + provenance:
// MATCH (t:WorkflowTask {id:"TASK_0001"})-[:TRIGGERED_BY]->(o:Observation)
// OPTIONAL MATCH (act:ProvenanceActivity)-[:PROV_GENERATED]->(c:CarbonItem)
// RETURN t.id, t.type, o.metric, o.value, o.observedAt, collect(DISTINCT act.id) AS provActivities;
// ============================================================================
