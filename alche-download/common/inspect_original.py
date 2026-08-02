from pygltflib import GLTF2

gltf = GLTF2().load("scene_original1.glb")

print("=" * 80)
print("NODES")
print("=" * 80)

for i, node in enumerate(gltf.nodes):
    print(
        f"{i:3d} | {node.name!r:35} mesh={node.mesh} children={node.children}"
    )

print("\n" + "=" * 80)
print("MESHES")
print("=" * 80)

for i, mesh in enumerate(gltf.meshes):
    print(i, mesh.name)