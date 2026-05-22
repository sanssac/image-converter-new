import glob
import os

base_dir = r"c:\image converter new"
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

required_ids = [
    'dropZone',
    'fileInput',
    'fileGallery',
    'convertBtn',
    'convertBtnText',
    'resultCard',
    'downloadBtn',
    'copyBtn',
    'downloadText',
    'canvas',
    'progressContainer',
    'progressFill'
]

for filepath in html_files:
    if '.git' in filepath or 'node_modules' in filepath or '__pycache__' in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'id="dropZone"' in content or "id='dropZone'" in content:
        # This is a converter page. Check for other elements
        missing = []
        for rid in required_ids:
            if f'id="{rid}"' not in content and f"id='{rid}'" not in content:
                missing.append(rid)
        if missing:
            print(f"{os.path.relpath(filepath, base_dir)}: missing IDs: {missing}")
