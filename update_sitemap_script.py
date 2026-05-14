import re

sitemap_path = r"c:\image converter new\sitemap.xml"
with open(sitemap_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_urls = """  <url>
    <loc>https://www.imglabconverter.com/blog/webp-vs-jpeg-which-is-better/</loc>
    <lastmod>2026-05-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.imglabconverter.com/blog/why-image-compression-improves-seo/</loc>
    <lastmod>2026-05-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>"""

content = content.replace("</urlset>", new_urls)

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated sitemap.xml")
