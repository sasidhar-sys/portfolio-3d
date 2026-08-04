import bpy
import math
import mathutils
import os

# ----------------------------------------------------
# 1. CLEAR SCENE
# ----------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for block in [bpy.data.meshes, bpy.data.materials, bpy.data.textures, bpy.data.images]:
    for item in block:
        block.remove(item)

# ----------------------------------------------------
# 2. CREATE ARCHITECTURAL ANGULAR "S" GEOMETRY
# ----------------------------------------------------
# Outer boundary of precision 45-degree geometric S
# Symmetrical around origin (0, 0, 0), straight segments only
outer_verts = [
    # Top horizontal cap & top-right slope
    (-0.25,  1.10),
    ( 0.40,  1.10),
    ( 0.85,  0.65),
    ( 0.85,  0.25),
    ( 0.45,  0.25),
    ( 0.45,  0.50),
    ( 0.25,  0.70),
    (-0.15,  0.70),
    (-0.45,  0.40),
    (-0.45,  0.10),
    
    # Diagonal waist transition down to bottom-left
    ( 0.25, -0.60),
    ( 0.45, -0.40),
    ( 0.45, -0.10),
    
    # Bottom loop & bottom-left slope
    ( 0.25, -1.10),
    (-0.40, -1.10),
    (-0.85, -0.65),
    (-0.85, -0.25),
    (-0.45, -0.25),
    (-0.45, -0.50),
    (-0.25, -0.70),
    ( 0.15, -0.70),
    ( 0.45, -0.40),
    ( 0.45, -0.10),
    
    # Waist return upper
    (-0.25,  0.60),
    (-0.45,  0.40),
    (-0.45,  0.10)
]

# Clean up & deduplicate polygon vertices to build a valid manifold 2D profile
def build_precision_s_mesh():
    # 2D polygonal vertices for the blueprint geometric S
    # Defined cleanly with 45-degree angles
    pts = [
        # Top roof peak
        (0.0, 1.25),
        (0.65, 0.80),
        (0.85, 0.40),
        (0.85, 0.15),
        (0.50, 0.15),
        (0.50, 0.40),
        (0.30, 0.60),
        (-0.10, 0.60),
        (-0.35, 0.35),
        (0.35, -0.35), # Diagonal waist
        (0.35, -0.60),
        (0.10, -0.60),
        (-0.30, -0.60),
        (-0.50, -0.40),
        (-0.50, -0.15),
        (-0.85, -0.15),
        (-0.85, -0.40),
        (-0.65, -0.80),
        (0.0, -1.25),
        (0.55, -0.80),
        (0.55, -0.55),
        (-0.15, 0.15), # Inner waist return
        (-0.55, 0.55),
        (-0.55, 0.80)
    ]
    return pts

profile_pts = build_precision_s_mesh()

# Construct 3D Mesh
verts_3d = [(p[0], p[1], -0.22) for p in profile_pts]
num_pts = len(verts_3d)

# Single manifold face or polygon
faces = [list(range(num_pts))]

mesh_2d = bpy.data.meshes.new("S_Architectural_Mesh")
mesh_2d.from_pydata(verts_3d, [], faces)
mesh_2d.update()

obj = bpy.data.objects.new("Crystal_S", mesh_2d)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# ----------------------------------------------------
# 3. EXTRUDE 3D VOLUME & BEVEL OPTICAL CHAMFERS
# ----------------------------------------------------
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Extrude Z height
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value": (0, 0, 0.44)}
)
bpy.ops.object.mode_set(mode='OBJECT')

# Recenter geometry around origin (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
obj.location = (0, 0, 0)

# Multi-segment Bevel modifier for architectural 45° optical facets
bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
bevel_mod.width = 0.045
bevel_mod.segments = 3
bevel_mod.limit_method = 'ANGLE'
bevel_mod.angle_limit = math.radians(30)
bevel_mod.miter_outer = 'MITER_ARC'
bpy.ops.object.modifier_apply(modifier="Bevel")

# CAD Smooth Shading & Weighted Normals
bpy.ops.object.shade_smooth()
try:
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
except Exception:
    pass

wn_mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
wn_mod.keep_sharp = True
bpy.ops.object.modifier_apply(modifier="WeightedNormal")

# Apply all transforms (Rotation, Scale, Location)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# ----------------------------------------------------
# 4. PBR OPTICAL CRYSTAL GLASS MATERIAL (With subtle cyan/purple glass tint)
# ----------------------------------------------------
mat = bpy.data.materials.new(name="OpticalCrystalGlass")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

node_output = nodes.new(type='ShaderNodeOutputMaterial')
node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')

# Optical Glass with subtle premium blue/purple edge tint
node_bsdf.inputs['Base Color'].default_value = (0.94, 0.96, 1.0, 1.0)
node_bsdf.inputs['Metallic'].default_value = 0.0
node_bsdf.inputs['Roughness'].default_value = 0.015
node_bsdf.inputs['IOR'].default_value = 1.52

for input_name, val in [
    ('Transmission Weight', 1.0), ('Transmission', 1.0),
    ('Specular IOR Level', 0.5), ('Specular', 0.5),
    ('Coat Weight', 0.25), ('Clearcoat', 0.25),
    ('Coat Roughness', 0.01), ('Clearcoat Roughness', 0.01)
]:
    if input_name in node_bsdf.inputs:
        node_bsdf.inputs[input_name].default_value = val

links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
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

tri_count = sum(len(p.vertices) - 2 for p in obj.data.polygons)
print(f"Mesh polycount: {tri_count} triangles, {len(obj.data.vertices)} vertices.")
