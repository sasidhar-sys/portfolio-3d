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
# 2. CREATE ARCHITECTURAL HOLLOW ANGULAR "S" PROFILE
# ----------------------------------------------------
# Outer boundary of precision geometric S
outer_pts = [
    # Top horizontal bar
    (-0.30, 0.95), (0.45, 0.95), (0.80, 0.60), (0.80, 0.25),
    (0.40, 0.25), (0.40, 0.45), (0.30, 0.55), (-0.15, 0.55),
    (-0.45, 0.25), (-0.45, -0.05),
    # Lower loop & bottom bar
    (0.35, -0.60), (0.35, -0.85), (0.15, -0.95), (-0.60, -0.95),
    (-0.80, -0.75), (-0.80, -0.35), (-0.40, -0.35), (-0.40, -0.55),
    (-0.30, -0.65), (0.15, -0.65), (0.35, -0.45), (0.35, -0.15),
    # Waist inner transition
    (-0.45, 0.45), (-0.45, 0.75), (-0.25, 0.90)
]

# Inner hollow cutout boundary (scaling inward for CAD hollow interior)
scale_inner = 0.65
inner_pts = [(pt[0] * scale_inner, pt[1] * scale_inner) for pt in reversed(outer_pts)]

# Combine outer and inner 2D vertices
all_verts_2d = outer_pts + inner_pts
num_outer = len(outer_pts)
num_inner = len(inner_pts)

verts_3d = [(v[0], v[1], -0.25) for v in all_verts_2d]

# Build faces connecting outer and inner boundary
faces = []
for i in range(num_outer):
    i_next = (i + 1) % num_outer
    j = num_outer + (num_inner - 1 - i)
    j_next = num_outer + (num_inner - 1 - i_next)
    faces.append([i, i_next, j_next, j])

mesh_2d = bpy.data.meshes.new("S_Precision_2D")
mesh_2d.from_pydata(verts_3d, [], faces)
mesh_2d.update()

obj = bpy.data.objects.new("Crystal_S", mesh_2d)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# ----------------------------------------------------
# 3. EXTRUDE & BEVEL FOR FACETED OPTICAL GLASS
# ----------------------------------------------------
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Extrude Z height for thick 3D volume
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value": (0, 0, 0.50)}
)
bpy.ops.object.mode_set(mode='OBJECT')

# Recenter geometry around origin (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
obj.location = (0, 0, 0)

# Multi-segment Bevel modifier for architectural facets
bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
bevel_mod.width = 0.05
bevel_mod.segments = 4
bevel_mod.limit_method = 'ANGLE'
bevel_mod.angle_limit = math.radians(35)
bevel_mod.miter_outer = 'MITER_ARC'
bpy.ops.object.modifier_apply(modifier="Bevel")

# CAD Smooth Shading & Weighted Normals
bpy.ops.object.shade_smooth()
try:
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(45))
except Exception:
    pass

wn_mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
wn_mod.keep_sharp = True
bpy.ops.object.modifier_apply(modifier="WeightedNormal")

# Apply transforms
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# ----------------------------------------------------
# 4. PBR TRANSPARENT OPTICAL CRYSTAL GLASS MATERIAL
# ----------------------------------------------------
mat = bpy.data.materials.new(name="OpticalCrystalGlass")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

node_output = nodes.new(type='ShaderNodeOutputMaterial')
node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')

node_bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
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
