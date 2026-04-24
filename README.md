# 🖼️ Image Converter

A fast, private, 100% client-side image converter built with Vanilla HTML/CSS/JS. No server uploads — all conversion happens inside the browser.

**Live site:** `https://yourwebsite.com` ← update this

---

## 📁 Project Structure

```
image-converter/
│
├── index.html                  # Homepage — main converter (JPG/PNG/WEBP)
│
├── ── Tool Pages ──────────────────────────────────────────
├── jpg-to-png/                 # /jpg-to-png/  — JPG → PNG converter
├── png-to-jpg/                 # /png-to-jpg/  — PNG → JPG converter
├── webp-to-jpg/                # /webp-to-jpg/ — WebP → JPG converter
├── webp-to-png/                # /webp-to-png/ — WebP → PNG converter
├── heic-to-jpg/                # /heic-to-jpg/ — HEIC → JPG converter
├── jpeg-to-webp/               # /jpeg-to-webp/— JPEG → WebP converter
├── jpg-to-avif/                # /jpg-to-avif/ — JPG → AVIF converter
├── png-to-avif/                # /png-to-avif/ — PNG → AVIF converter
├── png-to-ico/                 # /png-to-ico/  — PNG → ICO converter
├── svg-to-jpg/                 # /svg-to-jpg/  — SVG → JPG converter
├── compress-image/             # /compress-image/ — Image compressor
│
├── ── Content Pages ───────────────────────────────────────
├── blog/                       # /blog/ — Blog index
│   ├── how-to-convert-jpg-to-png/
│   ├── best-image-formats-explained/
│   └── reduce-image-size/
├── about/                      # /about/
├── contact/                    # /contact/
├── privacy-policy/             # /privacy-policy/
├── terms/                      # /terms/
│
├── ── Internationalization ────────────────────────────────
├── es/                         # /es/ — Spanish homepage
├── fr/                         # /fr/ — French homepage
├── de/                         # /de/ — German homepage
│
├── ── Assets ──────────────────────────────────────────────
├── assets/
│   ├── css/style.css           # Global stylesheet (glassmorphism + dark/light)
│   └── js/app.js               # Core conversion engine + UI logic
│
├── ── PWA & SEO ───────────────────────────────────────────
├── sw.js                       # Service Worker (Stale-While-Revalidate caching)
├── manifest.json               # PWA manifest
├── favicon.svg                 # Site icon
├── robots.txt                  # Search engine directives
├── sitemap.xml                 # All URLs for crawlers
├── googlefda0e304c8ec12dc.html # Google Search Console verification (DO NOT DELETE)
│
├── ── Deployment ──────────────────────────────────────────
├── vercel.json                 # Vercel config (headers, caching, clean URLs)
│
└── ── Developer Scripts ───────────────────────────────────
    └── scripts/
        └── sync_components.py  # Global nav sync — run after editing navigation
```

---

## 🚀 How To Run Locally

This is a pure static site — just open `index.html` in your browser. No build step needed.

For Vercel-style routing locally, use any static server:
```bash
npx serve .
```

---

## 🛠️ How To Update Navigation Globally

If you add or change a navigation link, run the sync script once — it updates all 15+ HTML files automatically:

```bash
python scripts/sync_components.py
```

---

## 🔧 Key Technical Details

| Concern | Solution |
|---|---|
| **Conversion** | HTML5 Canvas API + `canvas.toBlob()` |
| **HEIC support** | `heic2any` library (CDN) |
| **Batch ZIP** | `JSZip` library (CDN) |
| **Offline** | Service Worker (Stale-While-Revalidate) |
| **Privacy** | 100% client-side, zero server uploads |
| **Styling** | Glassmorphism, dark/light theme, CSS animations |
| **SEO** | FAQPage schema, canonical tags, i18n pages |

---

## ⚠️ Before Going Live

1. Replace all `https://yourwebsite.com` references with your real domain:
   ```bash
   # PowerShell one-liner:
   Get-ChildItem -Recurse -Include *.html,*.xml,*.txt | ForEach-Object { (Get-Content $_) -replace 'yourwebsite.com', 'yourrealsite.com' | Set-Content $_ }
   ```
2. Update Google Search Console with your real domain
3. Submit `sitemap.xml` to Google Search Console

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
