from pygltflib import GLTF2

gltf = GLTF2().load("common/scene.glb")

print("=== NODES ===")
for i, node in enumerate(gltf.nodes):
    print(i, node.name)