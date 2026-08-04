
import os

js_path = r"c:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js"

with open(js_path, "r", encoding="utf-8", errors="ignore") as f:
    c = f.read()

# Restore encoded URL paths that break remote CDN image fetches
c = c.replace("Sasidhar%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE", "ALCHE%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE")
c = c.replace("Sasidhar%20Studio", "ALCHE%20Studio")     
c = c.replace("Sasidhar", "ALCHE")

# Re-apply UI-only text replacements so your name stays visible in DOM/Canvas
c = c.replace("\"ALCHE\"", "\"SASIDHAR\"")
c = c.replace(">ALCHE<", ">SASIDHAR<")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed remote asset URLs and preserved UI branding!")

