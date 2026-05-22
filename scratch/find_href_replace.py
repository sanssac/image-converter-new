import re

file_path = r"c:\image converter new\scripts\translate_locales.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for occurrences of href in translate_page
lines = content.split('\n')
for idx, line in enumerate(lines):
    if 'href' in line or 'route' in line:
        if idx > 1300: # translate_page is near the end
            print(f"Line {idx+1}: {line}")
