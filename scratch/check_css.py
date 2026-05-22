with open(r'c:\image converter new\assets\css\style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'header' in line or 'logo-link' in line or 'header-right' in line or 'nav' in line:
        print(f"{i+1}: {line.strip()}")
