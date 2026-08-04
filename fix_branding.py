
import os

html_path = r"c:\Projects\Attempt-1\alche-download\index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    
    html = html.replace("ALCHE", "SASIDHAR").replace("Alche", "Sasidhar")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("SUCCESS: Updated index.html branding!")

