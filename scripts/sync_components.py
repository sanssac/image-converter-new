import glob
import re

# Edit this header HTML, run python sync_components.py, and it updates all 15 sites instantly!
GLOBAL_NAV = '''    <nav>
      <a href="/jpg-to-png">JPG to PNG</a>
      <a href="/png-to-jpg">PNG to JPG</a>
      <a href="/compress-image">Compress Image</a>
      <a href="/blog">Blog</a>
    </nav>'''

for filepath in glob.glob('**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_nx = content.find('<nav>')
    end_nx = content.find('</nav>') + 6
    if start_nx != -1 and end_nx != -1:
        content = content[:start_nx] + GLOBAL_NAV + content[end_nx:]
        
    # Remove JSZip to support lazy-loading
    content = re.sub(r'<script[^>]*jszip\.min\.js[^>]*></script>\s*', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print("Globally synchronized the navigation component and cleaned up scripts!")
