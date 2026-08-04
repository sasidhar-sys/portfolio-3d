import bpy
import math
import mathutils
import os

# ----------------------------------------------------
# 1. CLEAR SCENE
# ----------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove unused data blocks
for block in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, bpy.data.images]:
    for item in block:
        block.remove(item)

# ----------------------------------------------------
# 2. CREATE ARCHITECTURAL ANGULAR "S" 2D CURVE / MESH
# ----------------------------------------------------
# Define 2D vertices for a sharp, precision architectural S ribbon
# Symmetrical, angular 45-degree transitions

outer_verts_2d = [
    # Top bar & upper right turn
    (-0.35, 1.0),
    ( 0.45, 1.0),
    ( 0.85, 0.60),
    ( 0.85, 0.25),
    ( 0.50, 0.25),
    ( 0.50, 0.45),
    ( 0.35, 0.60),
    (-0.15, 0.60),
    (-0.45, 0.30),
    (-0.45, 0.05),
    
    # Diagonal waist & lower left turn
    ( 0.35, -0.60),
    ( 0.35, -0.85),
    ( 0.15, -1.0),
    (-0.65, -1.0),
    (-0.85, -0.80),
    (-0.85, -0.35),
    (-0.50, -0.35),
    (-0.50, -0.60),
    (-0.35, -0.70),
    ( 0.15, -0.70),
    ( 0.35, -0.40),
    ( 0.35, -0.15),
    
    # Waist inner return
    (-0.45, 0.50),
    (-0.45, 0.75),
    (-0.25, 0.95),
]

# Create 2D Mesh & Polygon
verts_3d = [(v[0], v[1], 0.0) for v in outer_verts_2d]
faces = [list(range(len(verts_3d)))]

# Build curve/mesh using Bmesh or Blender Mesh
mesh_2d = bpy.data.meshes.new("S_2D")
mesh_2d.from_pydata(verts_3d, [], [])
mesh_2d.update()

obj = bpy.data.objects.new("Crystal_S", mesh_2d)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# ----------------------------------------------------
# 3. EXTRUDE & BEVEL TO CREATE FACETED OPTICAL GLASS
# ----------------------------------------------------
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Fill 2D face
bpy.ops.mesh.edge_face_add()

# Extrude Z height
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value": (0, 0, 0.45)}
)
bpy.ops.object.mode_set(mode='OBJECT')

# Recenter geometry around origin (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
obj.location = (0, 0, 0)

# Add Solidify / Hollow interior if needed, or Bevel modifier
# Bevel Modifier for thick optical facets & chamfers
bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
bevel_mod.width = 0.06
bevel_mod.segments = 3
bevel_mod.limit_method = 'ANGLE'
bevel_mod.angle_limit = math.radians(30)
bevel_mod.miter_outer = 'MITER_ARC'

# Apply Bevel modifier
bpy.ops.object.modifier_apply(modifier="Bevel")

# Smooth shading & Weighted Normals for CAD-quality shading
bpy.ops.object.shade_smooth()
try:
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(45))
except Exception:
    pass


wn_mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
wn_mod.keep_sharp = True
bpy.ops.object.modifier_apply(modifier="WeightedNormal")

# Apply rotation & scale
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# ----------------------------------------------------
# 4. OPTICAL CRYSTAL GLASS PBR MATERIAL
# ----------------------------------------------------
mat = bpy.data.materials.new(name="OpticalCrystalGlass")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Create Principled BSDF & Output
node_output = nodes.new(type='ShaderNodeOutputMaterial')
node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')

# Configure Optical Glass Properties
node_bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
node_bsdf.inputs['Metallic'].default_value = 0.0
node_bsdf.inputs['Roughness'].default_value = 0.015
node_bsdf.inputs['IOR'].default_value = 1.52

# Handles for Transmission, Specular, Clearcoat across Blender versions
for input_name, val in [
    ('Transmission Weight', 1.0), ('Transmission', 1.0),
    ('Specular IOR Level', 0.5), ('Specular', 0.5),
    ('Coat Weight', 0.25), ('Clearcoat', 0.25),
    ('Coat Roughness', 0.01), ('Clearcoat Roughness', 0.01)
]:
    if input_name in node_bsdf.inputs:
        node_bsdf.inputs[input_name].default_value = val

links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

# Assign material to object
obj.data.materials.append(mat)

# ----------------------------------------------------
# 5. EXPORT GLB
# ----------------------------------------------------
target_paths = [
    r"c:\Projects\Attempt-1\crystal_s.glb",
    r"c:\Projects\Attempt-1\alche-download\models\crystal_s.glb"
]

for out_path in target_paths:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format='GLB',
        export_apply=True,
        export_materials='EXPORT',
        export_yup=True
    )
    print(f"Exported: {out_path}")

# Print Polycount details
tri_count = sum(len(p.vertices) - 2 for p in obj.data.polygons)
print(f"Mesh polycount: {tri_count} triangles, {len(obj.data.vertices)} vertices.")

