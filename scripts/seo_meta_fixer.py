import glob
import re
import os

print("Starting SEO meta tag normalization...")

def strip_existing_tags(html):
    # Remove any existing Standard SEO comment blocks
    html = re.sub(r'<!--\s*Standard SEO\s*/\s*Social Meta Tags\s*-->\s*', '', html, flags=re.IGNORECASE)
    
    # List of social and theme tags to remove completely
    tags_to_remove = [
        r'<meta\s+property="og:title"[^>]*>',
        r'<meta\s+property="og:description"[^>]*>',
        r'<meta\s+property="og:type"[^>]*>',
        r'<meta\s+property="og:url"[^>]*>',
        r'<meta\s+property="og:image"[^>]*>',
        r'<meta\s+property="og:image:width"[^>]*>',
        r'<meta\s+property="og:image:height"[^>]*>',
        r'<meta\s+name="twitter:card"[^>]*>',
        r'<meta\s+name="twitter:title"[^>]*>',
        r'<meta\s+name="twitter:description"[^>]*>',
        r'<meta\s+name="twitter:image"[^>]*>',
        r'<meta\s+name="author"[^>]*>',
        r'<meta\s+name="theme-color"[^>]*>'
    ]
    for tag in tags_to_remove:
        html = re.sub(tag, '', html, flags=re.IGNORECASE)
    
    # Clean up double blank lines
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    return html

base_dir = r"c:\image converter new"
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

count = 0
for filepath in html_files:
    if '.git' in filepath or 'scratch' in filepath:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.IGNORECASE)
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.IGNORECASE)
    
    title = title_match.group(1).strip() if title_match else "Free Online Image Converter"
    desc = desc_match.group(1).strip() if desc_match else "Free, secure, client-side browser image conversion tool."
    url = canonical_match.group(1).strip() if canonical_match else "https://www.imglabconverter.com/"
    
    html = strip_existing_tags(html)
    
    seo_block = f"""
  <!-- Standard SEO / Social Meta Tags -->
  <meta name="theme-color" content="#09090b" media="(prefers-color-scheme: dark)" />
  <meta name="theme-color" content="#f8fafc" media="(prefers-color-scheme: light)" />
  <meta name="author" content="Image Converter" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://www.imglabconverter.com/assets/images/og-banner.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://www.imglabconverter.com/assets/images/og-banner.png" />
"""
    
    # insert right before </head>
    html = html.replace('</head>', seo_block + '</head>')
    
    # Final cleanup of double newlines that replacement might cause
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        count += 1

print(f"Processed {count} HTML files with standardized and consolidated SEO/Social meta tags.")
