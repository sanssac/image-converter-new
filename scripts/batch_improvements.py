"""
Batch script to apply 3 improvements across all HTML files:
1. Add og:image meta tag (where missing)
2. Add defer to JSZip and heic2any CDN scripts
3. Add hreflang alternate tags to the 3 language pages + main index
"""
import glob, re

DOMAIN = 'https://image-converter-rho-six.vercel.app'
OG_IMAGE = f'{DOMAIN}/assets/images/og-banner.png'

# hreflang config: which pages have language alternates
HREFLANG_MAP = {
    'index.html': [
        ('x-default', f'{DOMAIN}/'),
        ('en', f'{DOMAIN}/'),
        ('es', f'{DOMAIN}/es/'),
        ('fr', f'{DOMAIN}/fr/'),
        ('de', f'{DOMAIN}/de/'),
    ],
    'es\\index.html': [
        ('x-default', f'{DOMAIN}/'),
        ('en', f'{DOMAIN}/'),
        ('es', f'{DOMAIN}/es/'),
        ('fr', f'{DOMAIN}/fr/'),
        ('de', f'{DOMAIN}/de/'),
    ],
    'fr\\index.html': [
        ('x-default', f'{DOMAIN}/'),
        ('en', f'{DOMAIN}/'),
        ('es', f'{DOMAIN}/es/'),
        ('fr', f'{DOMAIN}/fr/'),
        ('de', f'{DOMAIN}/de/'),
    ],
    'de\\index.html': [
        ('x-default', f'{DOMAIN}/'),
        ('en', f'{DOMAIN}/'),
        ('es', f'{DOMAIN}/es/'),
        ('fr', f'{DOMAIN}/fr/'),
        ('de', f'{DOMAIN}/de/'),
    ],
}

stats = {'og': 0, 'defer': 0, 'hreflang': 0}

for filepath in glob.glob('**/*.html', recursive=True):
    if '.git' in filepath:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False

    # 1. Add og:image if missing
    if 'og:image' not in html and '</head>' in html:
        og_tag = f'  <meta property="og:image" content="{OG_IMAGE}" />\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n  <meta name="twitter:image" content="{OG_IMAGE}" />\n'
        html = html.replace('</head>', og_tag + '</head>', 1)
        stats['og'] += 1
        changed = True

    # 2. Add defer to CDN scripts (jszip and heic2any)
    for cdn in ['jszip.min.js', 'heic2any.min.js']:
        pattern = rf'(<script src="[^"]*{re.escape(cdn)}[^"]*")(?! defer)(?![^>]*defer)>'
        replacement = r'\1 defer>'
        new_html = re.sub(pattern, replacement, html)
        if new_html != html:
            html = new_html
            stats['defer'] += 1
            changed = True

    # 3. Add hreflang tags for language pages
    norm = filepath.replace('/', '\\')
    if norm in HREFLANG_MAP and 'hreflang' not in html:
        links = '\n'.join(
            f'  <link rel="alternate" hreflang="{lang}" href="{url}" />'
            for lang, url in HREFLANG_MAP[norm]
        )
        html = html.replace('</head>', links + '\n</head>', 1)
        stats['hreflang'] += 1
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

print(f"og:image added to {stats['og']} files")
print(f"defer added to {stats['defer']} CDN script tags")
print(f"hreflang added to {stats['hreflang']} pages")
