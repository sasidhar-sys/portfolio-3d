
import os

js_path = r"c:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js"

with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
    c = f.read()

# Replace failing microCMS image URLs with a transparent 1x1 data URI fallback
fallback_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

import re
# Replace microcms-assets.io URLs with transparent fallback
c = re.sub(r"https://images\.microcms-assets\.io/assets/[^\"]+", fallback_url, c)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Replaced failing remote image URLs with local fallbacks!")

