with open(r'c:\image converter new\assets\js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

for line_num, line in enumerate(content.splitlines(), 1):
    if 'theme-toggle' in line or 'moon-icon' in line or 'clone' in line or 'header' in line or 'document.createElement' in line:
        print(f"{line_num}: {line.strip()}")
