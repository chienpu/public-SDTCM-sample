# make_ntu_campus_ifc.py
# Generates a lightweight IFC4_ADD2 sample: NTU_Campus_Sample.ifc
# Requires: pip install ifcopenshell

import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.api

# ---------- Create a brand new IFC4 file ----------
model = ifcopenshell.api.run("project.create_file")

# ---------- Project & Units ----------
project = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject", name="NTU Campus Sample Project")
ifcopenshell.api.run(
    "unit.assign_unit",
    model,
    length={"is_metric": True, "raw": "METRE"},
    area={"is_metric": True, "raw": "SQUARE_METRE"},
    volume={"is_metric": True, "raw": "CUBIC_METRE"}
)
 # fixed for new API

# ---------- Context (3D) ----------
context = ifcopenshell.api.run(
    "context.add_context",
    model,
    context_type="Model",
    context_identifier=None,
    target_view="MODEL_VIEW",
)

# ---------- Site / Building / Storeys ----------
site = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSite", name="NTU Campus Site")
building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding", name="NTU Campus Sample Building")
storey1 = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Level 1")
storey2 = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Level 2")

# 手動設定 Elevation 屬性
storey1.Elevation = 0.0
storey2.Elevation = 4.5


# Aggregate
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=project, products=[site])
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=site, products=[building])
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=building, products=[storey1, storey2])


# ---------- Spaces ----------
space1 = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSpace", name="Classroom_101")
space2 = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSpace", name="Lobby")
space3 = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSpace", name="Lab_201")

# 將 Spaces 放入樓層層級（Storey）中
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=storey1, products=[space1, space2])
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=storey2, products=[space3])

# ---------- Building Elements ----------
roof = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcRoof", name="Roof_A")
wall = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcWall", name="Wall_A")
slab = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSlab", name="Floor_A")

for elem in (roof, wall, slab):
    ifcopenshell.api.run("spatial.assign_container", model, products=[elem], relating_structure=storey1)

# ---------- Equipment ----------
ahu = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcUnitaryEquipment", name="AHU_1")
fan = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcFan", name="ExhaustFan_2")
light = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcLightFixture", name="LEDPanel_3")

for elem in (ahu, fan, light):
    ifcopenshell.api.run("spatial.assign_container", model, products=[elem], relating_structure=storey2)

# ---------- Sensors ----------
temp_sensor = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSensor", name="TempSensor_AHU")
co2_sensor = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSensor", name="CO2Sensor_Lab")
lux_sensor = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSensor", name="LightSensor_Lobby")

ifcopenshell.api.run("spatial.assign_container", model, products=[temp_sensor], relating_structure=storey2)
ifcopenshell.api.run("spatial.assign_container", model, products=[co2_sensor], relating_structure=storey2)
ifcopenshell.api.run("spatial.assign_container", model, products=[lux_sensor], relating_structure=storey1)



# ---------- Property sets (simulated attributes) ----------
def pset(model, product, name, props):
    pset = ifcopenshell.api.run("pset.add_pset", model, product=product, name=name)
    for k, v in props.items():
        if isinstance(v, (int, float)):
            ifcopenshell.api.run("pset.edit_pset", model, pset=pset, properties={k: float(v)})
        else:
            ifcopenshell.api.run("pset.edit_pset", model, pset=pset, properties={k: str(v)})

# Areas / Volumes
pset(model, space1, "Pset_Area", {"GrossArea_m2": 85, "Volume_m3": 230})
pset(model, space2, "Pset_Area", {"GrossArea_m2": 60, "Volume_m3": 160})
pset(model, space3, "Pset_Area", {"GrossArea_m2": 70, "Volume_m3": 200})

# Materials & EnergyUse on elements
pset(model, roof, "Pset_Material", {"Material": "Concrete", "Thickness_mm": 200})
pset(model, wall, "Pset_Material", {"Material": "Brick", "Thickness_mm": 150})
pset(model, slab, "Pset_Material", {"Material": "Concrete", "Thickness_mm": 250})
pset(model, roof, "Pset_EnergyUse", {"EnergyUse_kWh": 125})
pset(model, ahu, "Pset_Equipment", {"PowerRating_kW": 3.5, "FlowRate_m3h": 1200})

# --- Additional PropertySet for AHU_1 (Energy Performance) ---
pset(model, ahu, "Pset_AHU_Performance", {
    "FlowRate_m3h": 1200,
    "Power_kW": 3.5,
    "Efficiency": 0.88
})

# Sensors’ type/info
pset(model, temp_sensor, "Pset_Sensor", {"SensorType": "TEMPERATURE"})
pset(model, co2_sensor, "Pset_Sensor", {"SensorType": "CO2"})
pset(model, lux_sensor, "Pset_Sensor", {"SensorType": "ILLUMINANCE"})

# ---------- Save ----------
model.write("NTU_Campus_Sample.ifc")
print("✅ NTU_Campus_Sample.ifc generated.")
