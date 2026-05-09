import os
import glob
import re

workspace = "c:\\image converter new"

html_files = glob.glob(os.path.join(workspace, "**", "*.html"), recursive=True)
pattern = re.compile(r'<script src="/assets/js/app\.js(\?v=[^"]*)?"></script>')

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, num_subs = pattern.subn(r'<script type="module" src="/assets/js/main.js?v=20260506"></script>', content)
    
    if num_subs > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} HTML files to use ES modules (main.js).")
