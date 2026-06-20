import os

sitemap_path = r"c:\image converter new\sitemap.xml"

# List of all tools
all_tools = [
    "compress-image",
    "compress-image-to-500kb",
    "compress-image-to-200kb",
    "compress-image-to-100kb",
    "compress-image-to-50kb",
    "compress-image-to-30kb",
    "compress-image-to-20kb",
    "compress-image-to-10kb",
    "compress-jpg-to-100kb",
    "compress-png-to-100kb",
    "compress-jpeg-to-100kb",
    "heic-to-jpg",
    "jpeg-to-webp",
    "jpg-to-avif",
    "jpg-to-png",
    "photo-to-black-and-white",
    "png-to-avif",
    "png-to-ico",
    "png-to-jpg",
    "resize-image",
    "svg-to-jpg",
    "svg-to-png",
    "watermark-image",
    "webp-to-jpg",
    "webp-to-png",
    "jpg-to-pdf",
    "jpg-to-tiff",
    "tiff-to-jpg"
]

languages = ["de", "es", "fr", "hi", "zh"]
base_url = "https://www.imglabconverter.com"

with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap_content = f.read()

new_urls_xml = ""

# Add any missing English tools
for tool in all_tools:
    url = f"{base_url}/{tool}/"
    if f"<loc>{url}</loc>" not in sitemap_content:
        new_urls_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-04-26</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

# Add any missing Localized tools
for lang in languages:
    for tool in all_tools:
        url = f"{base_url}/{lang}/{tool}/"
        if f"<loc>{url}</loc>" not in sitemap_content:
            new_urls_xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-04-26</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

if new_urls_xml:
    sitemap_content = sitemap_content.replace('</urlset>', new_urls_xml + '</urlset>')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Sitemap updated successfully.")
else:
    print("No new URLs to add.")
