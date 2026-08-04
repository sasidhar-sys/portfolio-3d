import sys
import io
from pathlib import Path
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

p = Path(r"C:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js")
text = p.read_text(encoding="utf-8", errors="ignore")

patterns = [
    r"registerSection\(",
    r"class TopScrollManager",
    r"class .*ScrollManager",
    r"registerSection\([^)]*\)\{",
]

for pat in patterns:
    print("\n" + "=" * 100)
    print("PATTERN:", pat)
    for m in re.finditer(pat, text):
        start = max(0, m.start() - 1200)
        end = min(len(text), m.end() + 5000)
        print(text[start:end])
        print("\n" + "-" * 100)
