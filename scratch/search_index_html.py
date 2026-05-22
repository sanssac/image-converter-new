with open(r'c:\image converter new\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for line_num, line in enumerate(content.splitlines(), 1):
    if 'moon' in line.lower() or 'sun' in line.lower() or 'theme-toggle' in line.lower():
        print(f"{line_num}: {line.strip()}")
