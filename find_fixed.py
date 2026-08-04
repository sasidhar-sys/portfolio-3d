from pathlib import Path
import re

path = Path(r"C:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js")
text = path.read_text(encoding="utf-8")

terms = [
    "Works__content_inner",
    "Works__content",
    "data-works-container",
    "style.position",
    ".style.position",
    "position:\"fixed\"",
    "position:'fixed'",
    "ScrollTrigger.create(",
    "new ScrollTrigger",
    "pin:",
    "pinSpacing"
]

for term in terms:
    print("\n" + "=" * 70)
    print(term)
    print("=" * 70)

    found = False
    for m in re.finditer(re.escape(term), text):
        found = True
        s = max(0, m.start() - 150)
        e = min(len(text), m.end() + 250)
        print(text[s:e])
        print("\n" + "-" * 80)

    if not found:
        print("NOT FOUND")
