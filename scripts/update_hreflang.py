import os
import glob
import re

base_dir = r"c:\image converter new"
base_url = "https://image-converter-rho-six.vercel.app"
languages = ["de", "es", "fr", "hi", "zh"]

# Get all HTML files
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

def strip_hreflang_tags(html):
    # Remove all existing hreflang link tags
    return re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/?>\n?', '', html, flags=re.IGNORECASE)

for filepath in html_files:
    if '.git' in filepath:
        continue
    
    # Calculate the canonical path relative to the root, ignoring the language prefix
    rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
    
    # E.g., 'es/compress-image/index.html' or 'compress-image/index.html' or 'index.html'
    
    parts = rel_path.split('/')
    
    if parts[-1] == 'index.html':
        parts.pop()
        
    # Check if the first part is a language code
    if len(parts) > 0 and parts[0] in languages:
        parts.pop(0)
        
    route = "/".join(parts)
    if route:
        route = route + "/"
        
    hreflang_block = f"""
  <link rel="alternate" hreflang="x-default" href="{base_url}/{route}" />
  <link rel="alternate" hreflang="en" href="{base_url}/{route}" />
"""
    for lang in languages:
        hreflang_block += f'  <link rel="alternate" hreflang="{lang}" href="{base_url}/{lang}/{route}" />\n'
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Clean up existing ones
    html = strip_hreflang_tags(html)
    
    # Insert new ones right before </head>
    html = html.replace('</head>', hreflang_block + '</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Successfully updated hreflang tags for all pages!")
