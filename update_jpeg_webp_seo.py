import re
import os
import glob

# ---------------------------------------------------------
# UPDATE JPEG-TO-WEBP
# ---------------------------------------------------------
def update_jpeg_to_webp():
    files = glob.glob('**/jpeg-to-webp/index.html', recursive=True)
    for f in files:
        if 'node_modules' in f: continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Update Titles
        content = re.sub(
            r'<title>.*?</title>',
            r'<title>Bulk Convert JPEG to WebP Online Free | No Size Limits</title>',
            content
        )
        content = re.sub(
            r'<meta property="og:title" content=".*?" />',
            r'<meta property="og:title" content="Bulk Convert JPEG to WebP Online Free | No Size Limits" />',
            content
        )
        content = re.sub(
            r'<meta name="twitter:title" content=".*?" />',
            r'<meta name="twitter:title" content="Bulk Convert JPEG to WebP Online Free | No Size Limits" />',
            content
        )
        
        # English specific updates
        if f == 'jpeg-to-webp/index.html' or f == 'jpeg-to-webp\\index.html':
            # Update H1
            content = re.sub(
                r'<h1.*?>Convert JPEG to WebP Online Free</h1>',
                r'<h1 style="text-align:center; font-size: 28px; margin: 10px 0 20px; background: linear-gradient(135deg, #818cf8, #d8b4fe); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">Batch Convert JPEG to WebP for Core Web Vitals</h1>',
                content
            )
            
            # Update Schema
            old_schema = r'''  <script type="application/ld\+json">
  \{
    "@context": "https://schema\.org",
    "@type": "FAQPage",
    "mainEntity": \[
      \{
        "@type": "Question",
        "name": "Will WebP images work on all browsers\?",
        "acceptedAnswer": \{
          "@type": "Answer",
          "text": "Yes, all modern browsers \(Chrome, Firefox, Edge, Safari\) now fully support the WebP format\. For very old browser versions, it is standard practice to use a fallback, but the vast majority of web traffic today is WebP-compatible\."
        \}
      \},
      \{
        "@type": "Question",
        "name": "Can I convert multiple JPEGs at once\?",
        "acceptedAnswer": \{
          "@type": "Answer",
          "text": "Absolutely\. Drag and drop any number of JPEG files, and our converter will process them in parallel\. You can download the optimized WebP files individually or as a bulk ZIP archive\."
        \}
      \},
      \{
        "@type": "Question",
        "name": "Does converting to WebP lose image quality\?",
        "acceptedAnswer": \{
          "@type": "Answer",
          "text": "Our converter uses optimized settings to ensure the highest possible quality-to-size ratio\. While it is technically a lossy conversion from JPEG, the visual difference is almost never detectable by the human eye\."
        \}
      \}
    \]
  \}
  </script>'''
            
            new_schema = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Will WebP images work on all browsers?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, all modern browsers (Chrome, Firefox, Edge, Safari) now fully support the WebP format. For very old browser versions, it is standard practice to use a fallback, but the vast majority of web traffic today is WebP-compatible."
        }
      },
      {
        "@type": "Question",
        "name": "Can I convert multiple JPEGs at once?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Absolutely. Drag and drop any number of JPEG files, and our converter will process them in parallel. You can download the optimized WebP files individually or as a bulk ZIP archive."
        }
      },
      {
        "@type": "Question",
        "name": "Does converting to WebP lose image quality?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Our converter uses optimized settings to ensure the highest possible quality-to-size ratio. While it is technically a lossy conversion from JPEG, the visual difference is almost never detectable by the human eye."
        }
      },
      {
        "@type": "Question",
        "name": "Does WebP support transparency like PNG?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, unlike JPEG, WebP fully supports a lossless alpha channel for transparency. This makes it a perfect, smaller replacement for both JPG and PNG files on your website."
        }
      },
      {
        "@type": "Question",
        "name": "How to bulk convert images to WebP on Mac or Windows?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "You don't need to install any software. Simply open this browser-based tool on Mac or Windows, drag and drop all your image files at once, and they will be batch converted locally on your machine for maximum privacy."
        }
      }
    ]
  }
  </script>'''
            content = re.sub(old_schema, new_schema, content, flags=re.MULTILINE)
            
            # Update Article
            old_article = r'''      <article class="seo-article glass-panel">
        <h2>How to Convert JPEG to WebP Online Securely</h2>
        <p>WebP is a modern image format that provides superior lossless and lossy compression for images on the web\. Using WebP, webmasters and developers can create smaller, richer images that make the web faster\. Converting your heavy JPEGs to WebP is one of the most effective ways to improve your website's PageSpeed score and Core Web Vitals\.</p>
        <h3>Why convert JPEG to WebP\?</h3>
        <p>Compared to JPEG, WebP images are typically 25-35% smaller in file size while maintaining comparable quality\. This reduction in size results in faster page loads and less bandwidth consumption for your users\. Furthermore, WebP supports transparency \(alpha channel\) which JPEG does not, making it a more versatile format for modern web design\.</p>
        <h3>Is this tool safe to use\?</h3>
        <p>Yes\. This tool runs <strong>100% inside your browser</strong>\. We never upload your images to our servers\. Your device handles the entire conversion process locally, meaning your private data stays on your machine\. This is the fastest and most secure way to optimize your images for the modern web\.</p>
        <p>If you need to further reduce the size of your WebP files without changing the format, try our <a href="/compress-image">Compress Image</a> tool for advanced optimization\.</p>
        <div class="faq-section">
          <h3>Frequently Asked Questions</h3>
          <div class="faq-item">
            <div class="faq-question">Will WebP images work on all browsers\?</div>
            <div class="faq-answer">Yes, all modern browsers \(Chrome, Firefox, Edge, Safari\) now fully support the WebP format\. For very old browser versions, it is standard practice to use a fallback, but the vast majority of web traffic today is WebP-compatible\.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Can I convert multiple JPEGs at once\?</div>
            <div class="faq-answer">Absolutely\. Drag and drop any number of JPEG files, and our converter will process them in parallel\. You can download the optimized WebP files individually or as a bulk ZIP archive\.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Does converting to WebP lose image quality\?</div>
            <div class="faq-answer">Our converter uses optimized settings to ensure the highest possible quality-to-size ratio\. While it is technically a lossy conversion from JPEG, the visual difference is almost never detectable by the human eye\.</div>
          </div>
        </div>
      </article>'''

            new_article = '''      <article class="seo-article glass-panel">
        <h2>How to Batch Convert JPEG to WebP Online Securely</h2>
        <p>WebP is a next-gen image format created by Google that provides superior lossless and lossy compression for images on the web. Using WebP, webmasters and developers can create smaller, richer images that make the web faster. Converting your heavy JPEGs to WebP is one of the most effective, highest-ROI ways to improve your website's Google PageSpeed Insights score and pass Core Web Vitals.</p>
        
        <h3>Why WebP is Essential for SEO</h3>
        <p>Search engines like Google prioritize fast-loading websites. Images often account for the majority of a webpage's downloaded bytes. By migrating from legacy formats like JPEG and PNG to next-gen formats like WebP or AVIF, you directly decrease load times, lower your Largest Contentful Paint (LCP) metric, and provide a snappier user experience. Better performance correlates strongly with higher organic search rankings.</p>
        
        <h3>WebP vs JPEG: The Technical Benefits</h3>
        <p>Compared to legacy JPEG files, WebP images are typically <strong>25% to 35% smaller</strong> in file size while maintaining mathematically comparable SSIM index quality. This massive reduction results in faster page loads, less bandwidth consumption, and lower server CDN costs. Furthermore, WebP natively supports alpha channel transparency (which JPEG lacks) and animation (which standard PNG lacks), making it the ultimate versatile format for modern web design.</p>
        
        <h3>100% Client-Side Privacy: Is this tool safe?</h3>
        <p>Yes. Unlike server-based converters that force you to upload your sensitive files to a remote cloud, our application utilizes modern WebAssembly and HTML5 File APIs to run <strong>100% inside your local browser</strong>. We never upload your images to our servers. Your CPU handles the entire conversion process locally, meaning your private photos, proprietary business assets, and client documents never leave your machine.</p>
        
        <p>If you need to further reduce the size of your WebP files strictly for storage or email, try our <a href="/compress-image">Compress Image</a> tool for aggressive targeted optimization.</p>
        
        <div class="faq-section">
          <h3>Frequently Asked Questions</h3>
          <div class="faq-item">
            <div class="faq-question">Will WebP images work on all browsers?</div>
            <div class="faq-answer">Yes, all modern browsers (Chrome, Firefox, Edge, Safari, Opera) now natively support the WebP format. The vast majority of global web traffic today runs on WebP-compatible software.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Can I convert multiple JPEGs at once?</div>
            <div class="faq-answer">Absolutely. Drag and drop any number of JPEG files, and our bulk converter will process them in parallel using multithreading. You can download the optimized WebP files individually or as a single bulk ZIP archive.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Does converting to WebP lose image quality?</div>
            <div class="faq-answer">Our converter uses optimized perceptual settings to ensure the highest possible quality-to-size ratio. While converting from JPEG to WebP is technically a lossy process, the visual difference is almost never detectable by the human eye at our default 80% quality threshold.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Does WebP support transparency like PNG?</div>
            <div class="faq-answer">Yes, unlike JPEG, WebP fully supports a lossless alpha channel for transparency. This makes it a perfect, significantly smaller replacement for heavy transparent PNG files on your website or app interface.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">How to bulk convert images to WebP on Mac or Windows?</div>
            <div class="faq-answer">You don't need to install any native software or command-line tools. Simply open this browser-based tool on macOS, Windows, or Linux, drag and drop all your image files at once, and they will be batch converted locally.</div>
          </div>
        </div>
      </article>'''
            content = re.sub(old_article, new_article, content, flags=re.MULTILINE)

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Updated {f}")

update_jpeg_to_webp()
