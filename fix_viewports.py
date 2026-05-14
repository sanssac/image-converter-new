import os

files = [
    'blog/index.html', 
    'blog/best-image-formats-explained/index.html', 
    'blog/how-to-convert-jpg-to-png/index.html', 
    'blog/reduce-image-size/index.html', 
    'privacy-policy/index.html', 
    'terms/index.html', 
    'about/index.html', 
    'contact/index.html'
]

for f in files:
    if os.path.exists(f):
        content = open(f, encoding='utf-8').read()
        if '<meta name="viewport"' not in content:
            # Handle both formats
            content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
            content = content.replace('<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
            
            # Clean up duplicates if any
            content = content.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <meta name="viewport"', '<meta name="viewport"')
            
            open(f, 'w', encoding='utf-8').write(content)
            print(f'Fixed {f}')
