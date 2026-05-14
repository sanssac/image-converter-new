import os
import re
import shutil

template_path = r"c:\image converter new\blog\best-image-formats-explained\index.html"
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Post 1: webp-vs-jpeg-which-is-better
slug1 = "webp-vs-jpeg-which-is-better"
title1 = "WebP vs JPEG: Which Image Format is Better for Your Website?"
desc1 = "A deep dive into WebP vs JPEG. Learn the technical differences, compression benefits, and why WebP is the superior format for SEO and page speed."
article1 = """      <article class="seo-article glass-panel" style="max-width:800px; margin:0 auto; padding:40px;">
        <h1 style="font-size:32px; margin-bottom:20px; color:var(--text-main, #e2e8f0);">WebP vs JPEG: Which Image Format is Better for SEO?</h1>
        <p>For decades, JPEG has been the undisputed king of web images. But as the internet has evolved, the demand for faster, lighter, and richer experiences has outgrown the capabilities of a format created in 1992. Enter <strong>WebP</strong>.</p>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">What is WebP?</h2>
        <p>WebP is a modern image format developed by Google specifically tailored for the web. It provides superior lossless and lossy compression, meaning it can dramatically reduce image file sizes without noticeable degradation in quality.</p>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">Key Differences: WebP vs JPEG</h2>
        <ul>
          <li><strong>File Size:</strong> WebP lossy images are on average <strong>25% to 34% smaller</strong> than comparable JPEG images at equivalent SSIM quality indexes.</li>
          <li><strong>Transparency:</strong> Unlike JPEG, which strictly supports opaque backgrounds, WebP supports a lossless alpha channel (transparency) just like PNG, but at a fraction of the file size.</li>
          <li><strong>Animation:</strong> WebP supports animation, making it a viable, lightweight alternative to bulky GIFs.</li>
        </ul>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">The SEO Impact of Using WebP</h2>
        <p>Google has explicitly stated that page speed is a ranking factor, specifically measured through Core Web Vitals. The <strong>Largest Contentful Paint (LCP)</strong> metric often hinges entirely on how fast your main hero image loads. By migrating from JPEG to WebP, you directly decrease the payload of your web pages, which directly improves LCP, lowers bounce rates, and boosts your organic search rankings.</p>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">Conclusion</h2>
        <p>In 2024, there is almost no technical reason to continue using JPEG for web delivery. All modern browsers fully support WebP. If you have a massive library of legacy JPEGs, use our free <a href="/jpeg-to-webp">JPEG to WebP converter</a> to bulk convert your assets instantly.</p>
      </article>"""

# Post 2: why-image-compression-improves-seo
slug2 = "why-image-compression-improves-seo"
title2 = "Why Image Compression is Critical for SEO and Core Web Vitals"
desc2 = "Learn how aggressive image compression impacts your Largest Contentful Paint (LCP), boosts Google rankings, and saves bandwidth."
article2 = """      <article class="seo-article glass-panel" style="max-width:800px; margin:0 auto; padding:40px;">
        <h1 style="font-size:32px; margin-bottom:20px; color:var(--text-main, #e2e8f0);">Why Image Compression is Critical for SEO</h1>
        <p>If your website is slow, you are losing money. It's a proven fact that higher load times correlate directly with higher bounce rates. One of the primary culprits behind sluggish websites is unoptimized, bloated imagery. Here is why image compression is a mandatory step in your SEO strategy.</p>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">The Core Web Vitals Connection</h2>
        <p>Google evaluates user experience using a set of metrics called Core Web Vitals. The most heavily weighted metric is <strong>Largest Contentful Paint (LCP)</strong>, which measures how long it takes for the largest element on the screen (usually a hero image or banner) to render.</p>
        <p>If you upload a raw 5MB photograph directly from your camera, it might take 4 seconds to download on a 4G connection. You instantly fail the LCP check. By compressing that same image down to 100KB, it loads in milliseconds, passing the test with flying colors.</p>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">Lossy vs Lossless Compression</h2>
        <p>There are two types of compression:</p>
        <ul>
          <li><strong>Lossless:</strong> Reduces file size by restructuring data without deleting any visual information. Safe, but yields minimal file size reduction.</li>
          <li><strong>Lossy:</strong> Intelligently discards data (like minute color variations) that the human eye cannot perceive. This can reduce file sizes by up to 80% with virtually identical visual results.</li>
        </ul>
        
        <h2 style="font-size:24px; margin-top:30px; color:var(--text-main, #e2e8f0);">How to Start Optimizing</h2>
        <p>You don't need expensive software to optimize your web assets. You can use our free, browser-based <a href="/compress-image">Image Compressor</a> to bulk process your images locally on your device before uploading them to your CMS.</p>
      </article>"""

def create_post(slug, title, desc, article):
    os.makedirs(os.path.join(r"c:\image converter new\blog", slug), exist_ok=True)
    
    # regex replaces
    content = template
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
    content = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{desc}" />', content)
    
    content = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{title}" />', content)
    content = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{desc}" />', content)
    content = re.sub(r'<meta property="og:url" content=".*?" />', f'<meta property="og:url" content="https://www.imglabconverter.com/blog/{slug}/" />', content)
    
    content = re.sub(r'<meta name="twitter:title" content=".*?" />', f'<meta name="twitter:title" content="{title}" />', content)
    content = re.sub(r'<meta name="twitter:description" content=".*?" />', f'<meta name="twitter:description" content="{desc}" />', content)
    
    # replace hreflangs
    content = re.sub(r'href="https://www.imglabconverter.com/.*?blog/best-image-formats-explained/"', lambda m: m.group(0).replace('best-image-formats-explained', slug), content)
    
    # replace article
    old_article_pattern = r'<article class="seo-article glass-panel".*?</article>'
    content = re.sub(old_article_pattern, article, content, flags=re.DOTALL)
    
    out_path = os.path.join(r"c:\image converter new\blog", slug, "index.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {out_path}")

create_post(slug1, title1, desc1, article1)
create_post(slug2, title2, desc2, article2)
