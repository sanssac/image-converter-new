import os
import re

base_dir = r"c:\image converter new"

# Helper to create folder if not exist
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 1. GENERATE TARGET SIZE AND FORMAT SPECIFIC PAGES
# We will use compress-image-to-100kb/index.html as a layout template
base_template_path = os.path.join(base_dir, "compress-image-to-100kb", "index.html")

with open(base_template_path, 'r', encoding='utf-8') as f:
    base_html = f.read()

# Strip schema script tags, canonical tag, hreflang tags, related tools, seo article, title, description, and h1
# We will rebuild these dynamically per page
def clean_base_page(html):
    # Strip ld+json schemas
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)
    # Strip alternate hreflangs
    html = re.sub(r'<link rel="alternate" hreflang="[^"]+"\s+href="[^"]+"\s*/?>\n?', '', html, flags=re.IGNORECASE)
    # Strip canonical
    html = re.sub(r'<link rel="canonical" href="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    # Strip title
    html = re.sub(r'<title>.*?</title>', '', html, flags=re.IGNORECASE)
    # Strip description meta
    html = re.sub(r'<meta\s+name="description"\s+content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    # Strip og/twitter headers to prevent duplicates
    html = re.sub(r'<meta property="og:title" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta property="og:description" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta name="twitter:title" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta name="twitter:description" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta property="og:url" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    # Strip H1
    html = re.sub(r'<h1 class="page-title">.*?</h1>', '<!-- PAGE_TITLE_PLACEHOLDER -->', html, flags=re.IGNORECASE)
    # Strip body data-target-size and dataset
    html = re.sub(r'<body data-target-mime="[^"]*" data-mode="compress" data-target-size="[^"]*">', '<!-- BODY_TAG_PLACEHOLDER -->', html, flags=re.IGNORECASE)
    # Strip related tools
    html = re.sub(r'<section class="related-tools glass-panel">.*?</section>', '<!-- RELATED_TOOLS_PLACEHOLDER -->', html, flags=re.DOTALL)
    # Strip seo article
    html = re.sub(r'<article class="seo-article glass-panel">.*?</article>', '<!-- SEO_ARTICLE_PLACEHOLDER -->', html, flags=re.DOTALL)
    return html

clean_html = clean_base_page(base_html)

# Define target tools
tools_info = [
    # (tool_name, size_kb, format_locked, format_display)
    ("compress-image-to-10kb", 10, None, "Image"),
    ("compress-image-to-20kb", 20, None, "Image"),
    ("compress-image-to-30kb", 30, None, "Image"),
    ("compress-image-to-50kb", 50, None, "Image"),
    ("compress-image-to-100kb", 100, None, "Image"),
    ("compress-image-to-200kb", 200, None, "Image"),
    ("compress-image-to-500kb", 500, None, "Image"),
    ("compress-jpg-to-100kb", 100, "image/jpeg", "JPG"),
    ("compress-png-to-100kb", 100, "image/png", "PNG"),
    ("compress-jpeg-to-100kb", 100, "image/jpeg", "JPEG")
]

for tool_name, size_kb, fmt_mime, fmt_disp in tools_info:
    dest_dir = os.path.join(base_dir, tool_name)
    ensure_dir(dest_dir)
    
    # Titles and descriptions optimized for CTR ("No Upload Required", "Free & Online")
    title = f"Compress {fmt_disp} to {size_kb}KB Online Free | No Upload Required"
    desc = f"Instantly compress and reduce {fmt_disp.lower()} size to under {size_kb}KB. Perfect for signatures, forms, and passport photos. 100% private and offline."
    
    # Build schema FAQ
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"How do I compress a {fmt_disp.lower()} to {size_kb}KB?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Upload your file into our local {fmt_disp} compressor. The client-side engine will automatically optimize resolution and quality parameters to fit within the {size_kb}KB limit."
                }
            },
            {
                "@type": "Question",
                "name": f"Can I compress PNG to {size_kb}KB without losing quality?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Compressing to exactly {size_kb}KB requires lossy optimization. While our kb reducer uses smart local canvas serialization to minimize quality loss, PNGs will be optimized to meet the target threshold."
                }
            },
            {
                "@type": "Question",
                "name": "Are my images uploaded to a server?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Absolutely not. Our compressor runs 100% locally in your web browser. Your images never leave your device, ensuring maximum privacy and security."
                }
            },
            {
                "@type": "Question",
                "name": "Can I compress images offline?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes! Since all processing is done client-side, this tool functions entirely offline without any internet connection once the page is loaded."
                }
            },
            {
                "@type": "Question",
                "name": "Does this work on mobile phones?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, it works seamlessly on all Android devices, iPhones (including HEIC formats), and tablets directly through your mobile web browser."
                }
            },
            {
                "@type": "Question",
                "name": "Can I compress multiple images at once?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, our tool supports bulk image compression. Drag and drop multiple files to optimize them in a single batch."
                }
            },
            {
                "@type": "Question",
                "name": "What image formats are supported?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "We support JPG, JPEG, PNG, WEBP, HEIC, and TIFF formats. Uploaded HEIC or TIFF files are automatically processed and converted."
                }
            }
        ]
    }
    
    # Build schema HowTo
    page_url = f"https://www.imglabconverter.com/{tool_name}/"
    howto_schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to compress {fmt_disp.lower()} to {size_kb}KB online",
        "step": [
            {
                "@type": "HowToStep",
                "name": "Upload Images",
                "text": "Drag and drop your files into the upload area or click select to browse from your device.",
                "url": page_url
            },
            {
                "@type": "HowToStep",
                "name": "Select Target Size",
                "text": f"Our tool automatically locks optimization parameter parameters for {size_kb}KB compression. No configuration needed.",
                "url": page_url
            },
            {
                "@type": "HowToStep",
                "name": "Download Output",
                "text": "Click the compress button and download your optimized files instantly.",
                "url": page_url
            }
        ]
    }
    
    import json
    faq_schema_str = json.dumps(faq_schema, ensure_ascii=False, indent=2)
    howto_schema_str = json.dumps(howto_schema, ensure_ascii=False, indent=2)
    
    schemas_block = f"""  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{page_url}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <script type="application/ld+json">
{faq_schema_str}
  </script>
  <script type="application/ld+json">
{howto_schema_str}
  </script>"""

    # H1 title
    h1_title = f"Compress {fmt_disp} to {size_kb}KB Online"
    h1_html = f'<h1 class="page-title">{h1_title}</h1>'
    
    # Body tag configuration
    if fmt_mime:
        body_tag = f'<body data-target-mime="{fmt_mime}" data-mode="compress" data-target-size="{size_kb}">'
    else:
        body_tag = f'<body data-target-mime="image/jpeg" data-mode="compress" data-target-size="{size_kb}">'
        
    # Related Tools Link Block
    related_tools_html = f"""<section class="related-tools glass-panel">
        <h3>Related Free Tools</h3>
        <a href="/">Convert Multiple Formats</a>
        <a href="/compress-image">Compress Image (Custom Size)</a>
        <a href="/compress-image-to-10kb/">Compress Image to 10KB</a>
        <a href="/compress-image-to-20kb/">Compress Image to 20KB</a>
        <a href="/compress-image-to-30kb/">Compress Image to 30KB</a>
        <a href="/compress-image-to-50kb/">Compress Image to 50KB</a>
        <a href="/compress-image-to-100kb/">Compress Image to 100KB</a>
        <a href="/compress-image-to-200kb/">Compress Image to 200KB</a>
        <a href="/compress-image-to-500kb/">Compress Image to 500KB</a>
        <a href="/compress-jpg-to-100kb/">Compress JPG to 100KB</a>
        <a href="/compress-png-to-100kb/">Compress PNG to 100KB</a>
        <a href="/compress-jpeg-to-100kb/">Compress JPEG to 100KB</a>
      </section>"""
      
    # SEO article with H2 cluster structures, comparison metrics, and government application keywords
    seo_article_html = f"""<article class="seo-article glass-panel">
        <h2>Reduce {fmt_disp} Image Size to {size_kb}KB Online Securely</h2>
        <p>Whether you are submitting an online job application, applying for government examinations, uploading details for passport registration, or filing digital signatures, strict file size limits are always a hurdle. Most portals require you to upload a photo under {size_kb}KB. Our dedicated client-side <strong>image kb reducer</strong> is the perfect utility to compress your photos instantly to meet these exact thresholds without losing noticeable quality.</p>
        
        <h2>Compress JPG to {size_kb}KB</h2>
        <p>If you are optimizing standard photographic images or passport photos, they are usually in JPG/JPEG format. Since JPEGs hold camera tags and metadata, they can easily exceed {size_kb}KB. This page acts as a targeted <strong>jpg size reducer</strong> that intelligently downscales image dimensions and quality parameters to ensure the final payload is under {size_kb}KB. No registration or software downloads required.</p>
        
        <h2>Compress PNG to {size_kb}KB</h2>
        <p>PNG formats are lossless and carry large weight, making it incredibly difficult to shrink them under {size_kb}KB. Our advanced canvas optimization converts and compresses PNG images down to {size_kb}KB by quantizing color layouts. This makes it perfect for digital signature crop files and transparent logo files that must fit strict government portals.</p>
        
        <h2>Reduce Image Size for Government Forms and Applications</h2>
        <p>Filling out forms like the India UPSC registration, SSC application portals, passport upload documents, or college admission forms requires photo resizing to exact parameters like {size_kb}KB. Our tool is optimized to process passport photos, signatures, and ID cards locally to help you upload them without error messages.</p>
        
        <section class="comparison-section" style="margin: 20px 0; padding: 15px; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px;">
          <h3>Why use ImgLabConverter instead of upload-based compressors?</h3>
          <ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 8px; margin: 15px 0 0;">
            <li><strong>✓ No Uploads Required:</strong> Your files never touch our servers. All compression happens locally.</li>
            <li><strong>✓ Works Offline:</strong> You can compress images even without an active internet connection.</li>
            <li><strong>✓ Faster Processing:</strong> No waiting for uploads or downloads. Instant client-side optimization.</li>
            <li><strong>✓ Unlimited Usage:</strong> Compress as many images as you want for free without caps.</li>
            <li><strong>✓ Privacy Friendly:</strong> Perfect for confidential documents, IDs, and signatures.</li>
          </ul>
        </section>

        <div class="faq-section">
          <h3>Frequently Asked Questions</h3>
          <div class="faq-item">
            <div class="faq-question">How do I compress a {fmt_disp.lower()} to {size_kb}KB?</div>
            <div class="faq-answer">Upload your file into our local {fmt_disp} compressor. The client-side engine will automatically optimize resolution and quality parameters to fit within the {size_kb}KB limit.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Can I compress PNG to {size_kb}KB without losing quality?</div>
            <div class="faq-answer">Compressing to exactly {size_kb}KB requires lossy optimization. While our kb reducer uses smart local canvas serialization to minimize quality loss, PNGs will be optimized to meet the target threshold.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Are my images uploaded to a server?</div>
            <div class="faq-answer">Absolutely not. Our compressor runs 100% locally in your web browser. Your images never leave your device, ensuring maximum privacy and security.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Can I compress images offline?</div>
            <div class="faq-answer">Yes! Since all processing is done client-side, this tool functions entirely offline without any internet connection once the page is loaded.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Does this work on mobile phones?</div>
            <div class="faq-answer">Yes, it works seamlessly on all Android devices, iPhones (including HEIC formats), and tablets directly through your mobile web browser.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Can I compress multiple images at once?</div>
            <div class="faq-answer">Yes, our tool supports bulk image compression. Drag and drop multiple files to optimize them in a single batch.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">What image formats are supported?</div>
            <div class="faq-answer">We support JPG, JPEG, PNG, WEBP, HEIC, and TIFF formats. Uploaded HEIC or TIFF files are automatically processed and converted.</div>
          </div>
        </div>
      </article>"""

    # Assemble HTML
    temp_html = clean_html
    temp_html = temp_html.replace('</head>', f'{schemas_block}\n</head>')
    temp_html = temp_html.replace('<!-- PAGE_TITLE_PLACEHOLDER -->', h1_html)
    temp_html = temp_html.replace('<!-- BODY_TAG_PLACEHOLDER -->', body_tag)
    temp_html = temp_html.replace('<!-- RELATED_TOOLS_PLACEHOLDER -->', related_tools_html)
    temp_html = temp_html.replace('<!-- SEO_ARTICLE_PLACEHOLDER -->', seo_article_html)
    
    # Save index.html
    dest_path = os.path.join(dest_dir, "index.html")
    with open(dest_path, 'w', encoding='utf-8') as f_out:
        f_out.write(temp_html)
        
    print(f"Generated root English page: {tool_name}/index.html")


# 2. GENERATE 4 PROGRAMMATIC BLOG PAGES
# We will use blog/reduce-image-size/index.html as a layout template
blog_template_path = os.path.join(base_dir, "blog", "reduce-image-size", "index.html")

with open(blog_template_path, 'r', encoding='utf-8') as f:
    blog_base = f.read()

def clean_blog_page(html):
    html = re.sub(r'<title>.*?</title>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta\s+name="description"\s+content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta property="og:title" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta property="og:description" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta name="twitter:title" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta name="twitter:description" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta property="og:url" content="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/?>\n?', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<link rel="canonical" href="[^"]+"\s*/?>', '', html, flags=re.IGNORECASE)
    # Strip structural content
    html = re.sub(r'<article class="seo-article glass-panel">.*?</article>', '<!-- BLOG_CONTENT_PLACEHOLDER -->', html, flags=re.DOTALL)
    return html

blog_clean = clean_blog_page(blog_base)

blog_posts = [
    {
        "slug": "how-to-compress-jpg-to-100kb",
        "title": "How to Compress JPG to 100KB Online Free | No Upload Required",
        "desc": "A step-by-step tutorial on reducing JPEG images to exactly under 100KB locally in your web browser. Safely compress passport photos and online applications.",
        "article": """<article class="seo-article glass-panel">
        <h1>How to Compress JPG to 100KB Online Free</h1>
        <p>Many online submission portals limit your image uploads to strictly under 100KB. This is typical for passport applications, government examinations, and corporate job forms. While there are dozens of compression websites online, most force you to upload your sensitive photos to their cloud servers.</p>
        
        <p>Here is a simple, secure tutorial on how to compress your JPG photos under 100KB offline, right on your machine, using our 100% private <strong>jpg size reducer</strong>.</p>
        
        <h2>Step 1: Navigate to the 100KB Compressor</h2>
        <p>Go to our specialized <a href="/compress-image-to-100kb/">Compress Image to 100KB</a> tool or our <a href="/compress-jpg-to-100kb/">Compress JPG to 100KB</a> locking page. This pre-configures the compression algorithms to automatically stay under the 100KB limit.</p>
        
        <h2>Step 2: Drag and Drop Your Photos</h2>
        <p>Drag your bloated JPG/JPEG photos into the drag-and-drop box, or click the select button to select files from your mobile phone camera roll or computer hard drive.</p>
        
        <h2>Step 3: Execute Local Processing</h2>
        <p>Click the <strong>Compress Images</strong> button. Under the hood, HTML5 canvas scaling and binary optimization algorithms will calculate the highest quality ratio that fits within 100KB. This requires zero cloud uploads and works instantly.</p>
        
        <h2>Step 4: Download Your File</h2>
        <p>Click <strong>Download Compressed</strong> to save your lightweight JPG directly to your download directory, ready to be uploaded to your registration form!</p>
      </article>"""
    },
    {
        "slug": "how-to-compress-png-to-50kb",
        "title": "How to Compress PNG to 50KB Without Losing Quality Online",
        "desc": "Learn how to compress PNG images to under 50KB using client-side canvas quantization. Perfect for digital signatures and transparent logos.",
        "article": """<article class="seo-article glass-panel">
        <h1>How to Compress PNG to 50KB Without Losing Quality</h1>
        <p>PNG format files are lossless, meaning they contain high details and transparency metadata. The trade-off is their size: a simple digital signature crop can easily weigh 500KB, making it fail strict 50KB submission limits. To compress a PNG under 50KB without making it look pixelated or losing transparency, specialized color quantization is required.</p>
        
        <h2>The HTML5 Local Quantization Solution</h2>
        <p>Instead of converting your PNG to a blurry JPG, you can use canvas quantization. Our tool handles this directly on the client side:</p>
        
        <h2>Step 1: Open the 50KB Compressor</h2>
        <p>Navigate to our specialized <a href="/compress-image-to-50kb/">Compress Image to 50KB</a> page. The page comes pre-configured with a 50KB threshold limitation.</p>
        
        <h2>Step 2: Add Your PNG Signature or Image</h2>
        <p>Select your signature file. If your browser supports it, it will render a high-quality local thumb review instantly.</p>
        
        <h2>Step 3: Auto-Scale Optimization</h2>
        <p>Our client-side code will look at the PNG file dimensions. To hit 50KB, it will scale dimensions down iteratively while preserving transparency values. Click compress, and within milliseconds, a optimized PNG will be generated.</p>
        
        <h2>Step 4: Download Your Upload-Ready File</h2>
        <p>Save the transparent, lightweight PNG to your phone or desktop, fully compliant with SSC, bank portal, or application specifications.</p>
      </article>"""
    },
    {
        "slug": "how-to-resize-passport-photo-online",
        "title": "How to Resize Passport Photo to 20KB/50KB/100KB Online Free",
        "desc": "A complete guide on preparing, cropping, and resizing passport photos to strict size guidelines (20KB, 50KB, 100KB) for online applications.",
        "article": """<article class="seo-article glass-panel">
        <h1>How to Resize Passport Photo to Specific KB Limits Online</h1>
        <p>Preparing a passport photo for digital upload is one of the most frustrating aspects of online registrations. Different websites have vastly different size requirements—some demand under 20KB, others require under 50KB or 100KB, and others demand specific aspect ratios.</p>
        
        <h2>1. Crop to the Standard Aspect Ratio</h2>
        <p>Before compressing, ensure your photo is cropped to a standard passport ratio (usually 3.5cm x 4.5cm or a 1:1 square ratio depending on the guidelines). You can use our <a href="/resize-image">Resize Image</a> tool to crop and set explicit width and height dimensions.</p>
        
        <h2>2. Target the Required Size Limit</h2>
        <p>Once cropped, navigate to the specific size-limited compressor. We provide dedicated pages that guarantee your image fits exactly within limits:</p>
        <ul>
          <li>For extremely small files: <a href="/compress-image-to-10kb/">Compress Image to 10KB</a> or <a href="/compress-image-to-20kb/">Compress Image to 20KB</a></li>
          <li>For typical passport photos: <a href="/compress-image-to-30kb/">Compress Image to 30KB</a> or <a href="/compress-image-to-50kb/">Compress Image to 50KB</a></li>
          <li>For passport/resume documents: <a href="/compress-image-to-100kb/">Compress Image to 100KB</a></li>
        </ul>
        
        <h2>3. Compress Privately and Locally</h2>
        <p>Select your cropped photo and hit compress. The canvas engine will output a perfectly sized JPG file that is compliant with standard government systems. Because it works locally, your personal passport photo is completely secure.</p>
      </article>"""
    },
    {
        "slug": "how-to-reduce-image-size-for-government-forms",
        "title": "How to Reduce Image Size for Government Forms (UPSC, SSC, Passport)",
        "desc": "Prepare your photo and signature uploads for strict government application portals (UPSC, SSC, and others) by compressing files to under 20KB and 50KB locally.",
        "article": """<article class="seo-article glass-panel">
        <h1>How to Reduce Image Size for Government Forms (UPSC, SSC, Passport)</h1>
        <p>Online government application portals in India (such as UPSC, SSC, IBPS, and state-level registration forms) have notoriously strict requirements for uploaded attachments. Typically, candidate photos must be between 20KB and 50KB, while candidate signatures must be between 10KB and 20KB. Uploading larger files throws an immediate upload error.</p>
        
        <h2>UPSC & SSC Photo and Signature Guidelines</h2>
        <p>Follow this checklist to format your files perfectly in under 2 minutes:</p>
        
        <h2>Candidate Signature (10KB - 20KB)</h2>
        <p>Sign on plain white paper with a black ink pen, take a clear photo, crop out excess background space, and use our <a href="/compress-image-to-20kb/">Compress Image to 20KB</a> or <a href="/compress-image-to-10kb/">Compress Image to 10KB</a> tools. This ensures the signature file remains legible and falls safely within the limit.</p>
        
        <h2>Candidate Photo (20KB - 50KB)</h2>
        <p>Stand against a light/white background, take a passport-style headshot, and use our <a href="/compress-image-to-50kb/">Compress Image to 50KB</a> tool. The tool will automatically downscale the file to sit right between 20KB and 50KB, which is the exact acceptance window.</p>
        
        <h2>Absolute Privacy for Personal Documents</h2>
        <p>Never upload your official signatures or passport photos to unverified third-party cloud engines. Our client-side local optimizer executes all conversions entirely in your browser memory, meaning your document files never travel over the network. Save your time and protect your identity.</p>
      </article>"""
    }
]

for post in blog_posts:
    slug = post["slug"]
    title = post["title"]
    desc = post["desc"]
    art_html = post["article"]
    
    dest_dir = os.path.join(base_dir, "blog", slug)
    ensure_dir(dest_dir)
    
    page_url = f"https://www.imglabconverter.com/blog/{slug}/"
    
    headers_block = f"""  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{page_url}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <link rel="alternate" hreflang="x-default" href="{page_url}" />
  <link rel="alternate" hreflang="en" href="{page_url}" />"""

    temp_html = blog_clean
    temp_html = temp_html.replace('</head>', f'{headers_block}\n</head>')
    temp_html = temp_html.replace('<!-- BLOG_CONTENT_PLACEHOLDER -->', art_html)
    
    dest_path = os.path.join(dest_dir, "index.html")
    with open(dest_path, 'w', encoding='utf-8') as f_out:
        f_out.write(temp_html)
        
    print(f"Generated programmatic blog post: blog/{slug}/index.html")


# 3. UPDATE blog/index.html TO LINK TO THE NEW ARTICLES
blog_index_path = os.path.join(base_dir, "blog", "index.html")
with open(blog_index_path, 'r', encoding='utf-8') as f:
    blog_idx_html = f.read()

# Define new blog cards
new_blog_cards_html = """           <a href="/blog/how-to-compress-jpg-to-100kb/" class="blog-card glass-panel">
              <span>Tutorial</span>
              <h2>How to Compress JPG to 100KB Online Free</h2>
              <p>A step-by-step guide to compressing JPEG files under 100KB locally for secure applications.</p>
           </a>
           <a href="/blog/how-to-compress-png-to-50kb/" class="blog-card glass-panel">
              <span>Optimization</span>
              <h2>How to Compress PNG to 50KB Without Losing Quality</h2>
              <p>Learn how to resize and compress transparent PNG files under 50KB for signature uploads.</p>
           </a>
           <a href="/blog/how-to-resize-passport-photo-online/" class="blog-card glass-panel">
              <span>Tutorial</span>
              <h2>How to Resize Passport Photo to 20KB/50KB/100KB</h2>
              <p>Prepare crops and compress passport photos to strict size guidelines safely.</p>
           </a>
           <a href="/blog/how-to-reduce-image-size-for-government-forms/" class="blog-card glass-panel">
              <span>Applications</span>
              <h2>How to Reduce Image Size for Government Forms</h2>
              <p>Format photo and signature attachments for SSC, UPSC and passport portals offline.</p>
           </a>
"""

# Let's insert the new blog cards right after the class="blog-grid" opening
if '<div class="blog-grid">' in blog_idx_html:
    blog_idx_html = blog_idx_html.replace('<div class="blog-grid">', '<div class="blog-grid">\n' + new_blog_cards_html)
    with open(blog_index_path, 'w', encoding='utf-8') as f:
        f.write(blog_idx_html)
    print("Updated blog/index.html successfully!")
else:
    print("Warning: blog-grid div not found in blog/index.html")
