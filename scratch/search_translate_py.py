with open(r'c:\image converter new\scripts\translate_locales.py', 'r', encoding='utf-8') as f:
    content = f.read()

for line_num, line in enumerate(content.splitlines(), 1):
    if 'theme-toggle' in line.lower() or 'moon-icon' in line.lower() or 'header' in line.lower():
        print(f"{line_num}: {line.strip()[:120]}")
