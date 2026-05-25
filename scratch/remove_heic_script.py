import glob
import re
import os

base_dir = r"c:\image converter new"
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

pattern = re.compile(r'\s*<script\s+src="https://cdn\.jsdelivr\.net/npm/heic2any@[^"]*/heic2any\.min\.js"[^>]*>\s*</script>\s*', re.IGNORECASE)

count = 0
for filepath in html_files:
    if '.git' in filepath or 'scratch' in filepath:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    new_html, sub_count = pattern.subn('\n', html)
    if sub_count > 0:
        # Also clean up double newlines if left behind
        new_html = re.sub(r'\n\s*\n\s*\n', '\n\n', new_html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        count += 1

print(f"Successfully removed eager heic2any script from {count} HTML pages.")
