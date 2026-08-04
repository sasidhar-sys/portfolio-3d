from pathlib import Path

html = Path(r"C:\Projects\Attempt-1\alche-download\index.html").read_text(encoding="utf-8")

start = html.find('data-top_section="works"')
end = html.find('data-top_section="works_outro"')

print(html[start:end])
