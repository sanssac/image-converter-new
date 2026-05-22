with open(r'c:\image converter new\assets\css\style.css', 'r', encoding='utf-8') as f:
    content = f.read()

for line_num, line in enumerate(content.splitlines(), 1):
    if '::before' in line or '::after' in line or 'background' in line or 'content:' in line:
        if any(cls in line for cls in ['mega', 'lang', 'theme', 'btn', 'switcher', 'chev']):
            print(f"{line_num}: {line.strip()}")
