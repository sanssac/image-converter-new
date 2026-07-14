# 🖼️ ImgLab Converter

A lightning-fast, privacy-first, 100% client-side image converter built with Vanilla HTML, CSS, and JavaScript. All image conversions happen directly in your browser—no files are ever uploaded to a server.

**Live Site:** [https://www.imglabconverter.com](https://www.imglabconverter.com)

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Platform: Web](https://img.shields.io/badge/Platform-Web-blue.svg)]()
[![Privacy: Client-Side](https://img.shields.io/badge/Privacy-100%25_Client--Side-brightgreen.svg)]()

---

## ✨ Features

- **100% Private:** No server-side processing or storage. Your files never leave your device.
- **Multiple Formats:** Support for converting between JPG, PNG, WEBP, AVIF, HEIC, ICO, and SVG.
- **Batch Processing:** Convert and compress multiple images simultaneously and download them in a single ZIP file.
- **Modern UI:** A clean glassmorphism design with system-wide dark/light theme support.
- **SEO & Internationalization:** Fully optimized meta tags, hreflang annotations, and localized directory layouts for English, Spanish, French, German, Hindi, and Chinese.
- **PWA Ready:** Installable app with offline support powered by service workers.

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
├── compress-image/             # /compress-image/ — General image compressor
│
├── ── Content Pages ───────────────────────────────────────
├── blog/                       # /blog/ — Informative blogs on image editing
├── about/                      # /about/
├── contact/                    # /contact/
├── privacy-policy/             # /privacy-policy/
├── terms/                      # /terms/
│
├── ── Internationalization ────────────────────────────────
├── es/                         # Spanish localization
├── fr/                         # French localization
├── de/                         # German localization
├── hi/                         # Hindi localization
├── zh/                         # Chinese localization
│
├── ── Assets & Config ─────────────────────────────────────
├── assets/
│   ├── css/style.css           # Global glassmorphism style rules
│   └── js/app.js               # Conversion engine & client-side routing logic
├── sw.js                       # Service Worker for PWA asset caching
├── manifest.json               # PWA configuration
├── robots.txt                  # Search engine directives
├── sitemap.xml                 # Sitemap containing all localized pages
├── vercel.json                 # Vercel deployment cache and header overrides
│
└── ── Developer Scripts ───────────────────────────────────
    └── scripts/
        └── sync_components.py  # Script to synchronize global navigation changes
```

---

## 🚀 Run Locally

Since this is a fully static application, you can run it directly:

1. Double-click the `index.html` file to open it in any browser.
2. For local testing with clean Vercel-style routing, run a static server:
   ```bash
   npx serve .
   ```

---

## 🛠️ Syncing Global Navigation

If you modify the header, footer, or navigation bar, you can sync the changes across all 15+ tool and language pages instantly using the helper Python script:

```bash
python scripts/sync_components.py
```

---

## 🔧 Technology Stack

| Feature | Tech / Implementation |
|---|---|
| **Core Canvas Operations** | HTML5 Canvas API + `canvas.toBlob()` |
| **HEIC Image Support** | [heic2any](https://github.com/alexcorvi/heic2any) via CDN |
| **Multi-File Batch Downloads** | [JSZip](https://github.com/Stuk/jszip) via CDN |
| **Offline Capabilities** | Custom PWA Service Worker (Stale-While-Revalidate caching) |
| **Theme & UI Animations** | Modern CSS Variables, CSS Transitions, Grid Layouts |
| **Analytics & Core Vitals** | Vercel Analytics integration |

---

## 📄 License

This project is open-source and licensed under the [MIT License](LICENSE).

