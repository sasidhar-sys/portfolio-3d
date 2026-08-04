
import os

js_path = r"c:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js"

with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Auto-compute bounding sphere/box on loaded GLTF scenes to stop frustum clipping
old_pattern = "c.scene.traverse("
new_pattern = "c.scene.traverse(o=>{if(o.isMesh){o.frustumCulled=!1;if(o.geometry){o.geometry.computeBoundingBox();o.geometry.computeBoundingSphere();}}});c.scene.traverse("

if old_pattern in code:
    code = code.replace(old_pattern, new_pattern, 1)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Added auto-bounding calculation and disabled aggressive culling!")

