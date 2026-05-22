import glob
import os

base_dir = r"c:\image converter new"
files = glob.glob(os.path.join(base_dir, '**', '*.*'), recursive=True)

for filepath in files:
    if '.git' in filepath or 'node_modules' in filepath or '__pycache__' in filepath:
        continue
    if os.path.isdir(filepath):
        continue
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue
        
    if 'unexpected' in content.lower() or 'error' in content.lower():
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            if 'unexpected' in line.lower() or 'error' in line.lower():
                safe_line = line.strip()[:100].encode('ascii', errors='ignore').decode('ascii')
                print(f"{os.path.relpath(filepath, base_dir)}:{idx}: {safe_line}")
