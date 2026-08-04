import sys
import io
from pathlib import Path
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

p = Path(r"C:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js")
text = p.read_text(encoding="utf-8", errors="ignore")

keywords = [
    "works_intro",
    "works_outro",
    "works_progress",
    "topScrollManager",
    "getTrigger(",
    "addTrigger",
    "createTrigger",
    "ScrollTrigger",
]

for kw in keywords:
    print("\n" + "=" * 80)
    print("KEYWORD:", kw)

    for m in re.finditer(re.escape(kw), text):
        start = max(0, m.start() - 600)
        end = min(len(text), m.end() + 1200)

        print("\nPOSITION:", m.start())
        print(text[start:end])
        print("\n" + "-" * 80)
