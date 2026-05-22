import os
import glob
import re

base_dir = r"c:\image converter new"
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

scripts_seen = set()

for filepath in html_files:
    if '.git' in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    rel_path = os.path.relpath(filepath, base_dir)
    
    found = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content)
    for s in found:
        scripts_seen.add(s)

print("All script src tags in HTML files:")
for s in sorted(scripts_seen):
    print(s)
