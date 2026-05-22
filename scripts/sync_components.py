import glob
import re
import os

TRANSLATIONS = {
    'en': {
        'all_tools': 'All Tools',
        'blog': 'Blog',
        'logo_prefix': '',
        'popular': 'Popular Converters',
        'advanced': 'Advanced Formats',
        'nextgen': 'Next-Gen Formats',
        'tools': 'Tools & Filters',
        'lang_name': 'English',
        'multi': ('Multi-Format', 'Any format to any format'),
        'jpg_png': ('JPG → PNG', 'Lossless with transparency'),
        'png_jpg': ('PNG → JPG', 'Smaller file size'),
        'webp_jpg': ('WebP → JPG', 'Universal compatibility'),
        'jpeg_webp': ('JPEG → WebP', 'Modern web format'),
        'svg_png': ('SVG → PNG', 'Rasterize vectors'),
        'svg_jpg': ('SVG → JPG', 'Vector to photo format'),
        'heic_jpg': ('HEIC → JPG', 'iPhone photos support'),
        'png_ico': ('PNG → ICO', 'Favicon generator'),
        'webp_png': ('WebP → PNG', 'Lossless from WebP'),
        'jpg_avif': ('JPG → AVIF', 'Ultra-small files'),
        'png_avif': ('PNG → AVIF', 'Next-gen compression'),
        'resize': ('Resize Image', 'Change dimensions'),
        'watermark': ('Watermark', 'Add text overlays'),
        'jpg_pdf': ('JPG to PDF', 'Document compiler'),
        'compress': ('Compress', 'Auto quality optimizer')
    },
    'de': {
        'all_tools': 'Alle Werkzeuge',
        'blog': 'Blog',
        'logo_prefix': '/de',
        'popular': 'Beliebte Konverter',
        'advanced': 'Erweiterte Formate',
        'nextgen': 'Next-Gen-Formate',
        'tools': 'Werkzeuge & Filter',
        'lang_name': 'Deutsch',
        'multi': ('Multi-Format', 'Beliebiges Format umwandeln'),
        'jpg_png': ('JPG → PNG', 'Verlustfrei mit Transparenz'),
        'png_jpg': ('PNG → JPG', 'Kleinere Dateigröße'),
        'webp_jpg': ('WebP → JPG', 'Universelle Kompatibilität'),
        'jpeg_webp': ('JPEG → WebP', 'Modernes Webformat'),
        'svg_png': ('SVG → PNG', 'Vektorgrafiken rastern'),
        'svg_jpg': ('SVG → JPG', 'Vektor zu Fotoformat'),
        'heic_jpg': ('HEIC → JPG', 'iPhone-Fotos unterstützen'),
        'png_ico': ('PNG → ICO', 'Favicon-Generator'),
        'webp_png': ('WebP → PNG', 'Verlustfrei aus WebP'),
        'jpg_avif': ('JPG → AVIF', 'Extrem kleine Dateien'),
        'png_avif': ('PNG → AVIF', 'Next-Gen-Kompression'),
        'resize': ('Bildgröße ändern', 'Dimensionen anpassen'),
        'watermark': ('Wasserzeichen', 'Text-Overlays hinzufügen'),
        'jpg_pdf': ('JPG in PDF', 'Dokumenten-Compiler'),
        'compress': ('Komprimieren', 'Auto-Qualitätsoptimierung')
    },
    'es': {
        'all_tools': 'Todas las Herramientas',
        'blog': 'Blog',
        'logo_prefix': '/es',
        'popular': 'Convertidores Populares',
        'advanced': 'Formatos Avanzados',
        'nextgen': 'Formatos Next-Gen',
        'tools': 'Herramientas y Filtros',
        'lang_name': 'Español',
        'multi': ('Multi-Formato', 'Cualquier formato a cualquier formato'),
        'jpg_png': ('JPG → PNG', 'Sin pérdidas con transparencia'),
        'png_jpg': ('PNG → JPG', 'Tamaño de archivo más pequeño'),
        'webp_jpg': ('WebP → JPG', 'Compatibilidad universal'),
        'jpeg_webp': ('JPEG → WebP', 'Formato web moderno'),
        'svg_png': ('SVG → PNG', 'Rasterizar vectores'),
        'svg_jpg': ('SVG → JPG', 'Vector a formato de foto'),
        'heic_jpg': ('HEIC → JPG', 'Soporte para fotos de iPhone'),
        'png_ico': ('PNG → ICO', 'Generador de favicons'),
        'webp_png': ('WebP → PNG', 'Sin pérdidas desde WebP'),
        'jpg_avif': ('JPG → AVIF', 'Archivos ultra pequeños'),
        'png_avif': ('PNG → AVIF', 'Compresión de próxima generación'),
        'resize': ('Redimensionar', 'Cambiar dimensiones'),
        'watermark': ('Marca de Agua', 'Añadir superposiciones de texto'),
        'jpg_pdf': ('JPG a PDF', 'Compilador de documentos'),
        'compress': ('Comprimir', 'Optimización automática')
    },
    'fr': {
        'all_tools': 'Tous les Outils',
        'blog': 'Blog',
        'logo_prefix': '/fr',
        'popular': 'Convertisseurs Populaires',
        'advanced': 'Formats Avancés',
        'nextgen': 'Formats Next-Gen',
        'tools': 'Outils & Filtres',
        'lang_name': 'Français',
        'multi': ('Multi-Format', "N'importe quel format"),
        'jpg_png': ('JPG → PNG', 'Sans perte avec transparence'),
        'png_jpg': ('PNG → JPG', 'Taille de fichier réduite'),
        'webp_jpg': ('WebP → JPG', 'Compatibilité universelle'),
        'jpeg_webp': ('JPEG → WebP', 'Format web moderne'),
        'svg_png': ('SVG → PNG', 'Pixelliser les vecteurs'),
        'svg_jpg': ('SVG → JPG', 'Vecteur vers format photo'),
        'heic_jpg': ('HEIC → JPG', 'Photos iPhone prises en charge'),
        'png_ico': ('PNG → ICO', 'Générateur de favicon'),
        'webp_png': ('WebP → PNG', 'Sans perte depuis WebP'),
        'jpg_avif': ('JPG → AVIF', 'Fichiers ultra-petits'),
        'png_avif': ('PNG → AVIF', 'Compression de nouvelle génération'),
        'resize': ('Redimensionner', 'Changer les dimensions'),
        'watermark': ('Filigrane', 'Ajouter des superpositions de texte'),
        'jpg_pdf': ('JPG en PDF', 'Compilateur de documents'),
        'compress': ('Compresser', 'Optimisation automatique')
    },
    'hi': {
        'all_tools': 'सभी टूल्स',
        'blog': 'ब्लॉग',
        'logo_prefix': '/hi',
        'popular': 'लोकप्रिय कन्वर्टर्स',
        'advanced': 'उन्नत प्रारूप',
        'nextgen': 'नेक्स्ट-जेन प्रारूप',
        'tools': 'टूल्स और फिल्टर्स',
        'lang_name': 'हिन्दी',
        'multi': ('मल्टी-फॉर्मेट', 'किसी भी फॉर्मेट को बदलें'),
        'jpg_png': ('JPG → PNG', 'पारदर्शिता के साथ दोषरहित'),
        'png_jpg': ('PNG → JPG', 'छोटा फ़ाइल आकार'),
        'webp_jpg': ('WebP → JPG', 'सार्वभौमिक अनुकूलता'),
        'jpeg_webp': ('JPEG → WebP', 'आधुनिक वेब फॉर्मेट'),
        'svg_png': ('SVG → PNG', 'वेक्टर को रास्टर करें'),
        'svg_jpg': ('SVG → JPG', 'वेक्टर से फोटो फॉर्मेट'),
        'heic_jpg': ('HEIC → JPG', 'आईफोन फोटो सपोर्ट'),
        'png_ico': ('PNG → ICO', 'फेविकॉन जनरेटर'),
        'webp_png': ('WebP → PNG', 'वेबपी से दोषरहित पीएनजी'),
        'jpg_avif': ('JPG → AVIF', 'अल्ट्रा-छोटी फाइलें'),
        'png_avif': ('PNG → AVIF', 'नेक्स्ट-जेन कंप्रेशन'),
        'resize': ('आकार बदलें', 'आयाम बदलें'),
        'watermark': ('वॉटरमार्क', 'टेक्स्ट जोड़ें'),
        'jpg_pdf': ('JPG से PDF', 'दस्तावेज़ संकलक'),
        'compress': ('कंप्रेस', 'स्वचालित गुणवत्ता अनुकूलक')
    },
    'zh': {
        'all_tools': '所有工具',
        'blog': '博客',
        'logo_prefix': '/zh',
        'popular': '常用转换器',
        'advanced': '高级格式',
        'nextgen': '新一代格式',
        'tools': '工具与滤镜',
        'lang_name': '中文',
        'multi': ('多格式转换', '支持任何格式相互转换'),
        'jpg_png': ('JPG → PNG', '无损且支持透明度'),
        'png_jpg': ('PNG → JPG', '更小的文件体积'),
        'webp_jpg': ('WebP → JPG', '通用兼容性'),
        'jpeg_webp': ('JPEG → WebP', '现代网页图片格式'),
        'svg_png': ('SVG → PNG', '矢量图栅格化'),
        'svg_jpg': ('SVG → JPG', '矢量转静态图片'),
        'heic_jpg': ('HEIC → JPG', '支持苹果手机HEIC格式'),
        'png_ico': ('PNG → ICO', '网页图标生成器'),
        'webp_png': ('WebP → PNG', 'WebP转无损PNG'),
        'jpg_avif': ('JPG → AVIF', '极小文件体积'),
        'png_avif': ('PNG → AVIF', '新一代高效压缩'),
        'resize': ('调整大小', '修改图片尺寸'),
        'watermark': ('添加水印', '添加文字水印叠加'),
        'jpg_pdf': ('JPG转PDF', '图片合成PDF文档'),
        'compress': ('图片压缩', '自动质量优化器')
    }
}

def get_route(filepath):
    path = filepath.replace('\\', '/')
    parts = [p for p in path.split('/') if p]
    if len(parts) == 0:
        return '/'
    
    if parts[0] in ['de', 'es', 'fr', 'hi', 'zh']:
        parts = parts[1:]
        
    if len(parts) == 0 or parts[0] == 'index.html':
        return '/'
        
    tool_name = parts[0]
    return f'/{tool_name}/'

def make_mega_link(tool_key, tool_path, lang_prefix, trans):
    name, desc = trans[tool_key]
    svg_map = {
        'multi': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
        'jpg_png': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        'png_jpg': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        'webp_jpg': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        'jpeg_webp': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        'svg_png': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>',
        'svg_jpg': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>',
        'heic_jpg': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        'png_ico': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7h10v10H7z"/></svg>',
        'webp_png': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        'jpg_avif': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        'png_avif': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        'resize': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>',
        'watermark': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
        'jpg_pdf': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        'compress': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
    }
    
    href = f"{lang_prefix}{tool_path}"
    href = href.replace('//', '/')
    if not href:
        href = '/'
    
    svg = svg_map.get(tool_key, '')
    return f'''              <a href="{href}" class="mega-link">
                <div class="mega-icon-wrap">{svg}</div>
                <div class="mega-link-text"><span class="mega-link-name">{name}</span><span class="mega-link-desc">{desc}</span></div>
              </a>'''

def generate_header(current_lang, route):
    trans = TRANSLATIONS.get(current_lang, TRANSLATIONS['en'])
    lang_prefix = trans['logo_prefix']
    
    logo_href = f"{lang_prefix}/"
    logo_href = logo_href.replace('//', '/')
    
    # 1. Language Options Switcher Build
    lang_options = ""
    lang_names = {'en': 'English', 'es': 'Español', 'de': 'Deutsch', 'fr': 'Français', 'hi': 'हिन्दी', 'zh': '中文'}
    for code, name in lang_names.items():
        new_path = route if code == 'en' else f"/{code}{route}"
        new_path = new_path.replace('//', '/')
        active_class = "active" if code == current_lang else ""
        lang_options += f'          <a href="{new_path}" class="lang-opt {active_class}">{name}</a>\n'

    # 2. Localized Mega Menu Grid Build
    mega_col1 = "\n".join([
        make_mega_link('multi', '/', lang_prefix, trans),
        make_mega_link('jpg_png', '/jpg-to-png', lang_prefix, trans),
        make_mega_link('png_jpg', '/png-to-jpg', lang_prefix, trans),
        make_mega_link('webp_jpg', '/webp-to-jpg', lang_prefix, trans),
        make_mega_link('jpeg_webp', '/jpeg-to-webp', lang_prefix, trans),
    ])
    
    mega_col2 = "\n".join([
        make_mega_link('svg_png', '/svg-to-png', lang_prefix, trans),
        make_mega_link('svg_jpg', '/svg-to-jpg', lang_prefix, trans),
        make_mega_link('heic_jpg', '/heic-to-jpg', lang_prefix, trans),
        make_mega_link('png_ico', '/png-to-ico', lang_prefix, trans),
        make_mega_link('webp_png', '/webp-to-png', lang_prefix, trans),
    ])
    
    mega_col3 = "\n".join([
        make_mega_link('jpg_avif', '/jpg-to-avif', lang_prefix, trans),
        make_mega_link('png_avif', '/png-to-avif', lang_prefix, trans),
    ])
    
    mega_col4 = "\n".join([
        make_mega_link('resize', '/resize-image', lang_prefix, trans),
        make_mega_link('watermark', '/watermark-image', lang_prefix, trans),
        make_mega_link('jpg_pdf', '/jpg-to-pdf', lang_prefix, trans),
        make_mega_link('compress', '/compress-image', lang_prefix, trans),
    ])

    header_html = f'''  <header>
    <a href="{logo_href}" class="logo-link">
      <div class="logo">
        <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path><path d="M12 12v9"></path><path d="m8 17 4 4 4-4"></path></svg>
      </div>
      <div class="site-title">Image <span>Converter</span></div>
    </a>
    <div class="header-right">
      <nav>
        <div class="mega-menu-wrapper">
          <button class="mega-btn" aria-expanded="false">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
            {trans['all_tools']}
            <svg class="mega-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
        </div>
        <a href="/blog">{trans['blog']}</a>
        <div class="lang-switcher">
          <button class="lang-btn" aria-expanded="false" aria-haspopup="true">
            <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            <span>{trans['lang_name']}</span>
            <svg class="lang-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="lang-menu">
{lang_options}          </div>
        </div>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" aria-label="Toggle theme" style="background:none; border:none; color:inherit; cursor:pointer; display:flex; align-items:center; transition:0.2s;">
          <svg class="sun-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none;"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg class="moon-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
      </div>
    </div>
  </header>
  <div class="mega-dropdown">
    <div class="mega-grid">
      <div class="mega-column">
        <h4>{trans['popular']}</h4>
{mega_col1}
      </div>
      <div class="mega-column">
        <h4>{trans['advanced']}</h4>
{mega_col2}
      </div>
      <div class="mega-column">
        <h4>{trans['nextgen']}</h4>
{mega_col3}
      </div>
      <div class="mega-column">
        <h4>{trans['tools']}</h4>
{mega_col4}
      </div>
    </div>
  </div>'''
    return header_html

def remove_mega_dropdown(html):
    while True:
        start_tag = '<div class="mega-dropdown"'
        start_idx = html.find(start_tag)
        if start_idx == -1:
            break
            
        tag_close_idx = html.find('>', start_idx)
        if tag_close_idx == -1:
            break
            
        idx = tag_close_idx + 1
        depth = 1
        found = False
        
        while depth > 0 and idx < len(html):
            next_open = html.find('<div', idx)
            next_close = html.find('</div>', idx)
            
            if next_open == -1 and next_close == -1:
                break
                
            if next_open != -1 and (next_close == -1 or next_open < next_close):
                depth += 1
                idx = next_open + 4
            else:
                depth -= 1
                idx = next_close + 6
                if depth == 0:
                    trailing_ws_len = 0
                    while idx + trailing_ws_len < len(html) and html[idx + trailing_ws_len] in ' \t\r\n':
                        trailing_ws_len += 1
                    html = html[:start_idx] + html[idx + trailing_ws_len:]
                    found = True
                    break
        if not found:
            break
    return html

def main():
    base_dir = r"c:\image converter new"
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    
    count = 0
    for filepath in html_files:
        if '.git' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse language
        match = re.search(r'<html\s+[^>]*lang=["\']([a-zA-Z-]+)["\']', content)
        lang = match.group(1).lower() if match else 'en'
        lang = lang[:2]
        if lang not in TRANSLATIONS:
            lang = 'en'
            
        # Compute route
        rel_path = os.path.relpath(filepath, base_dir)
        route = get_route(rel_path)
        
        # Generate the beautiful, pre-rendered static header HTML block
        header_block = generate_header(lang, route)
        
        # Robust replacement: strip any existing pre-rendered mega-dropdown first
        content = remove_mega_dropdown(content)
        
        # Replace the entire <header>...</header> block
        content_new, sub_count = re.subn(r'<header>.*?</header>', header_block, content, flags=re.DOTALL)
        
        if sub_count > 0:
            # Also clean up duplicate script injection if any
            content_new = re.sub(r'<script[^>]*jszip\.min\.js[^>]*></script>\s*', '', content_new)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_new)
            count += 1
            
    print(f"Statically pre-rendered localized navigation headers for {count} pages successfully!")

if __name__ == "__main__":
    main()
