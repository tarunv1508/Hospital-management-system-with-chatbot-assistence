from pathlib import Path
import re

root = Path('.').resolve()
pattern = re.compile(r'^[ \t]*<li><a href="appointment\.html">Appointment</a></li>[ \t]*\n', re.MULTILINE)
updated = []

for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    new_text, count = pattern.subn('', text)
    if count > 0:
        path.write_text(new_text, encoding='utf-8')
        updated.append(str(path.relative_to(root)))

print(f'updated files: {len(updated)}')
for file in updated:
    print(file)
