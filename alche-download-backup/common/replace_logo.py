from pygltflib import GLTF2
import copy

ORIGINAL = "scene1.glb"
REPLACEMENT = "crystal_s.glb"
OUTPUT = "scene_fixed.glb"

orig = GLTF2().load(ORIGINAL)
rep = GLTF2().load(REPLACEMENT)

# -------------------------------------------------
# Find nodes by name
# -------------------------------------------------
def find_node(gltf, name):
    for i, n in enumerate(gltf.nodes):
        if n.name == name:
            return i
    return None

orig_node = find_node(orig, "Alche_A")
rep_node = find_node(rep, "Alche_A")

if orig_node is None:
    raise RuntimeError("Original Alche_A node not found.")

if rep_node is None:
    raise RuntimeError("Replacement Alche_A node not found.")

orig_mesh = orig.nodes[orig_node].mesh
rep_mesh = rep.nodes[rep_node].mesh

if rep_mesh is None:
    raise RuntimeError("Replacement mesh missing.")

# -------------------------------------------------
# Copy replacement mesh into original
# -------------------------------------------------

mesh = copy.deepcopy(rep.meshes[rep_mesh])
orig.meshes[orig_mesh] = mesh

# -------------------------------------------------
# Save
# -------------------------------------------------

orig.save(OUTPUT)

print("Done.")
print("Created:", OUTPUT)