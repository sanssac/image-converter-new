import glob

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
        updated = content[:start_nx] + GLOBAL_NAV + content[end_nx:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
print("Globally synchronized the navigation component!")
