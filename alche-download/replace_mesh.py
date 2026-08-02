from pygltflib import GLTF2
import copy

# Load files
scene = GLTF2().load("scene.glb")
crystal = GLTF2().load("common/crystal_s.glb")

# Replace the Alche_A mesh
scene.meshes[0] = copy.deepcopy(crystal.meshes[0])

# Save
scene.save("scene_replaced.glb")

print("Done! Created scene_replaced.glb")