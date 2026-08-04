from pygltflib import GLTF2

gltf = GLTF2().load("scene_original1.glb")

print()

for i, node in enumerate(gltf.nodes):
    print("="*70)
    print(node.name)
    print("mesh :", node.mesh)
    print("translation :", node.translation)
    print("rotation :", node.rotation)
    print("scale :", node.scale)