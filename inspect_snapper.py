import sys
import io
from pathlib import Path
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

text = Path(
    r"C:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js"
).read_text(encoding="utf-8", errors="ignore")

keywords = [
    "data-snapper",
    "snap-ratio",
    "SectionContainer",
    "offsetHeight",
    "scrollHeight",
    "clientHeight",
    "setSectionHeight",
    "style.height",
]

for kw in keywords:
    print("\n" + "=" * 80)
    print("KEYWORD:", kw)

    for m in re.finditer(re.escape(kw), text):
        s = max(0, m.start() - 800)
        e = min(len(text), m.end() + 3000)
        print(text[s:e])
        print("\n" + "-" * 80)
