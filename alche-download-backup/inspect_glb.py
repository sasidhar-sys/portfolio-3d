from pygltflib import GLTF2

gltf = GLTF2().load("scene.glb")

print("=" * 80)
print("NODES")
print("=" * 80)

for i, node in enumerate(gltf.nodes):
    print(
        f"{i:3d} | "
        f"name={node.name!r:35} "
        f"mesh={node.mesh} "
        f"children={node.children}"
    )

print("\n" + "=" * 80)
print("MESHES")
print("=" * 80)

for i, mesh in enumerate(gltf.meshes):
    print(i, mesh.name)