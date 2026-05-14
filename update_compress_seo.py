import re
import glob

def update_compress_image():
    files = glob.glob('**/compress-image/index.html', recursive=True)
    for f in files:
        if 'node_modules' in f: continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Update Titles
        content = re.sub(
            r'<title>.*?</title>',
            r'<title>Best Free Image Compressor | Reduce Image File Size to 50KB/100KB</title>',
            content
        )
        content = re.sub(
            r'<meta property="og:title" content=".*?" />',
            r'<meta property="og:title" content="Best Free Image Compressor | Reduce Image File Size to 50KB/100KB" />',
            content
        )
        content = re.sub(
            r'<meta name="twitter:title" content=".*?" />',
            r'<meta name="twitter:title" content="Best Free Image Compressor | Reduce Image File Size to 50KB/100KB" />',
            content
        )
        
        # Update Descriptions
        desc = "Reduce image file sizes instantly without noticeable quality loss. Bulk compress JPG, PNG, and WebP to 50KB, 100KB, or custom sizes using advanced browser compression."
        content = re.sub(
            r'<meta name="description"\s+content=".*?" />',
            f'<meta name="description" content="{desc}" />',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'<meta property="og:description"\s+content=".*?" />',
            f'<meta property="og:description" content="{desc}" />',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'<meta name="twitter:description"\s+content=".*?" />',
            f'<meta name="twitter:description" content="{desc}" />',
            content, flags=re.DOTALL
        )
        
        # English specific updates
        if f == 'compress-image/index.html' or f == 'compress-image\\index.html':
            # Update H1
            content = re.sub(
                r'<h1.*?Free Image Compressor Online</h1>',
                r'<h1 style="text-align:center; font-size: 28px; margin: 10px 0 20px; background: linear-gradient(135deg, #818cf8, #d8b4fe); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">Best Free Bulk Image Compressor Online</h1>',
                content, flags=re.DOTALL
            )
            
            # Update Schema
            old_schema = r'''  <script type="application/ld\+json">
  \{
    "@context": "https://schema\.org",
    "@type": "FAQPage",
    "mainEntity": \[
      \{
        "@type": "Question",
        "name": "Does compressing an image ruin the quality\?",
        "acceptedAnswer": \{
          "@type": "Answer",
          "text": "Our compressor uses smart lossy compression to reduce file sizes by up to 70% while keeping visual differences nearly imperceptible to the human eye\."
        \}
      \},
      \{
        "@type": "Question",
        "name": "Are my compressed images uploaded to a server\?",
        "acceptedAnswer": \{
          "@type": "Answer",
          "text": "No\. All compression happens directly on your device inside your web browser\. No files are uploaded or stored online, ensuring maximum privacy\."
        \}
      \},
      \{
        "@type": "Question",
        "name": "Is there a limit to how many images I can compress\?",
        "acceptedAnswer": \{
          "@type": "Answer",
          "text": "Because the processing is done locally on your machine, our tool has no artificial usage limits\. Compress as many images as you need for free\."
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
        "name": "Does compressing an image ruin the quality?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Our compressor uses smart lossy compression algorithms to aggressively reduce file sizes by up to 80% while keeping visual differences nearly imperceptible to the human eye. This is achieved by stripping invisible metadata and intelligently reducing color depth."
        }
      },
      {
        "@type": "Question",
        "name": "Are my compressed images uploaded to a server?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "No. All compression happens directly on your device inside your web browser. No files are ever uploaded or stored on an external cloud server, ensuring absolute privacy for your personal or business files."
        }
      },
      {
        "@type": "Question",
        "name": "Is there a limit to how many images I can compress?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Because the processing is done entirely locally using your own hardware, our bulk image compressor has absolutely no artificial usage limits, no daily caps, and no paywalls. Compress as many images as you need for free."
        }
      },
      {
        "@type": "Question",
        "name": "How do I compress an image to exactly 50KB or 100KB?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Our tool features a Target File Size setting. Simply select 'Under 50KB' or 'Under 100KB' before dragging your files into the drop zone. The compressor will iteratively adjust dimensions and quality to strictly meet your target threshold."
        }
      },
      {
        "@type": "Question",
        "name": "Does this tool strip EXIF data?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, to maximize compression, our tool dynamically strips unnecessary and bloated EXIF metadata such as camera GPS location, lens settings, and creation timestamps. This further protects your privacy when sharing images online."
        }
      }
    ]
  }
  </script>'''
            content = re.sub(old_schema, new_schema, content, flags=re.MULTILINE)
            
            # Update Article
            old_article = r'''      <article class="seo-article glass-panel">
        <h2>Reduce Image File Size Online Securely</h2>
        <p>Bloated, large image files drastically slow down website loading times, which results in poor SEO rankings
          and lost visitors\. Furthermore, unoptimized files quickly consume excessive storage on mobile devices and make
          emailing photos frustrating\. Our free image compressor provides an instant, easy way to resize and shrink your
          JPG, PNG, WEBP, and HEIC files to manageable sizes\.</p>
        <h3>How does the compression work\?</h3>
        <p>This tool utilizes aggressive browser-level serialization, dynamically stripping invisible EXIF metadata
          \(such as camera location data, device type, and exposure settings\), and reducing embedded color profiles\. It
          then applies an intelligent ~70% lossy compression ratio which creates massively smaller files with virtually
          zero human-detectable difference in visual quality\. The result is a web-ready image that looks identical but
          weighs a fraction of the original size\.</p>
        <h3>Fast, Private, and Client-Side</h3>
        <p>We believe in absolute privacy\. Unlike traditional cloud compressors that require you to upload your personal
          or proprietary business images, our app uses advanced HTML5 technology to compress files locally on your own
          hardware\. Your data never touches our servers\. This ensures a 100% secure environment that operates instantly,
          without waiting for uploads or downloads to complete\.</p>
        <div class="faq-section">
          <h3>Frequently Asked Questions</h3>
          <div class="faq-item">
            <div class="faq-question">Does compressing an image ruin the quality\?</div>
            <div class="faq-answer">Our compressor uses smart lossy compression to reduce file sizes by up to 70% while
              keeping visual differences nearly imperceptible to the human eye\.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Are my compressed images uploaded to a server\?</div>
            <div class="faq-answer">No\. All compression happens directly on your device inside your web browser\. No
              files are uploaded or stored online, ensuring maximum privacy\.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Is there a limit to how many images I can compress\?</div>
            <div class="faq-answer">Because the processing is done locally on your machine, our tool has no artificial
              usage limits\. Compress as many images as you need for free\.</div>
          </div>
        </div>
      </article>'''

            new_article = '''      <article class="seo-article glass-panel">
        <h2>Reduce Image File Size Online Securely & Instantly</h2>
        <p>Bloated, multi-megabyte image files drastically slow down website loading times, which directly results in poor SEO rankings, failed Core Web Vitals, and lost visitors. Furthermore, unoptimized files quickly consume excessive local storage on smartphones and make emailing or uploading photos to restrictive government/educational portals frustrating. Our free bulk image compressor provides an instant, easy way to aggressively resize and shrink your JPG, PNG, WEBP, and HEIC files to strict target sizes like 50KB or 100KB.</p>
        
        <h3>Lossy vs Lossless: How does the compression work?</h3>
        <p>This tool utilizes advanced browser-level canvas serialization and smart lossy algorithms. First, it dynamically strips out invisible and bloated EXIF metadata (such as GPS coordinates, camera models, and timestamp data), protecting your privacy. Second, it applies an intelligent compression ratio—often reducing file sizes by up to 80%—while making iterative dimension adjustments if you select a strict KB target. The visual difference is practically imperceptible to the human eye, yielding a web-ready image that looks identical but weighs a fraction of its original size.</p>
        
        <h3>Compress Images to Specific Sizes (50KB, 100KB, 500KB)</h3>
        <p>Many online forms, application portals, and social platforms strictly limit image uploads to very small sizes. Our application features an intelligent targeted compressor. Simply click on a preset (like "Under 50KB" or "Under 100KB") or enter a custom value in MB or KB, and our engine will recursively optimize your image until it successfully fits within the required threshold.</p>
        
        <h3>Fast, 100% Private, and Client-Side</h3>
        <p>We believe in absolute data privacy. Unlike traditional cloud compressors that force you to upload your sensitive personal photos or proprietary business assets to a remote server, our application leverages powerful WebAssembly and HTML5 APIs to compress files entirely locally on your own hardware. Your data never touches the internet. This ensures a 100% secure workflow that operates instantly, completely eliminating network latency and upload wait times.</p>
        
        <div class="faq-section">
          <h3>Frequently Asked Questions</h3>
          <div class="faq-item">
            <div class="faq-question">Does compressing an image ruin the quality?</div>
            <div class="faq-answer">Our compressor uses smart lossy compression algorithms to aggressively reduce file sizes by up to 80% while keeping visual differences nearly imperceptible to the human eye. This is achieved by stripping invisible metadata and intelligently reducing color depth.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Are my compressed images uploaded to a server?</div>
            <div class="faq-answer">No. All compression happens directly on your device inside your web browser. No files are ever uploaded or stored on an external cloud server, ensuring absolute privacy for your personal or business files.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Is there a limit to how many images I can compress?</div>
            <div class="faq-answer">Because the processing is done entirely locally using your own hardware, our bulk image compressor has absolutely no artificial usage limits, no daily caps, and no paywalls. Compress as many images as you need for free.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">How do I compress an image to exactly 50KB or 100KB?</div>
            <div class="faq-answer">Our tool features a Target File Size setting. Simply select 'Under 50KB' or 'Under 100KB' before dragging your files into the drop zone. The compressor will iteratively adjust dimensions and quality to strictly meet your target threshold.</div>
          </div>
          <div class="faq-item">
            <div class="faq-question">Does this tool strip EXIF data?</div>
            <div class="faq-answer">Yes, to maximize compression, our tool dynamically strips unnecessary and bloated EXIF metadata such as camera GPS location, lens settings, and creation timestamps. This further protects your privacy when sharing images online.</div>
          </div>
        </div>
      </article>'''
            content = re.sub(old_article, new_article, content, flags=re.MULTILINE)

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Updated {f}")

update_compress_image()
