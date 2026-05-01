import os

sitemap_path = r"c:\image converter new\sitemap.xml"

# List of all 15 tools
all_tools = [
    "compress-image",
    "compress-image-to-100kb",
    "compress-image-to-50kb",
    "heic-to-jpg",
    "jpeg-to-webp",
    "jpg-to-avif",
    "jpg-to-png",
    "photo-to-black-and-white",
    "png-to-avif",
    "png-to-ico",
    "png-to-jpg",
    "svg-to-jpg",
    "svg-to-png",
    "webp-to-jpg",
    "webp-to-png"
]

languages = ["de", "es", "fr", "hi", "zh"]
base_url = "https://imglabconverter.vercel.app"

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
