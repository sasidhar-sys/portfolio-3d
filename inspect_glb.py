from pygltflib import GLTF2

files = [
    r"C:\Projects\Attempt-1\alche-download\common\scene.glb",
    r"C:\Projects\Attempt-1\alche-download\common\scene_original.glb",
]

for path in files:
    print("\n==============================")
    print(path)

    gltf = GLTF2().load(path)

    node = next((n for n in gltf.nodes if n.name in ("geometry_0", "Alche_A")), None)

    if node is None:
        print("Logo node NOT FOUND")
        continue

    print("Node name :", node.name)
    print("Mesh index:", node.mesh)

    mesh = gltf.meshes[node.mesh]
    print("Mesh name :", mesh.name)

    prim = mesh.primitives[0]

    print("POSITION accessor :", prim.attributes.POSITION)
    print("NORMAL accessor   :", prim.attributes.NORMAL)
    print("TEXCOORD_0        :", prim.attributes.TEXCOORD_0)
    print("Indices           :", prim.indices)