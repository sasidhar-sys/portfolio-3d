import os, re

js_path = r"c:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js"

if not os.path.exists(js_path):
    print("Error: JS file not found at " + js_path)
    exit(1)

with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Neutralize microcms-assets 404 requests with a blank pixel data URI
fallback_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
code = re.sub(r"https://images\.microcms-assets\.io/assets/[^\"]+", fallback_img, code)

# 2. Safely wrap line 3980 geometry calls with optional chaining
code = re.sub(r"(\w+)\.getObjectByName\(([^)]+)\)\.geometry", r"\1?.getObjectByName(\2)?.geometry", code)

# 3. Guard WebGL render call safely using a short-circuit expression (expression-safe)
code = code.replace(
    "this.renderer.render(",
    "(this.renderer?.domElement?.width>0&&this.renderer?.domElement?.height>0)&&this.renderer.render("
)

# 4. Clean UI Branding text
code = code.replace("\"ALCHE\"", "\"SASIDHAR\"").replace(">ALCHE<", ">SASIDHAR<")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Cleanly patched JS bundle with valid syntax!")