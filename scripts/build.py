import os
import glob
import re
import datetime

workspace = "c:\\image converter new"
version = datetime.datetime.now().strftime("%Y%m%d%H%M")

def build_css():
    css_files = [
        "assets/css/base.css",
        "assets/css/layout.css",
        "assets/css/components.css",
        "assets/css/utilities.css"
    ]
    
    combined_css = ""
    for file in css_files:
        path = os.path.join(workspace, file)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                combined_css += f"/* --- {file} --- */\n"
                combined_css += f.read() + "\n\n"
                
    out_path = os.path.join(workspace, "assets", "css", "style.css")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(combined_css)
    print("Built style.css from modules.")

def update_html_versions():
    html_files = glob.glob(os.path.join(workspace, "**", "*.html"), recursive=True)
    pattern_js = re.compile(r'<script type="module" src="/assets/js/main\.js(\?v=[^"]*)?"></script>')
    pattern_css = re.compile(r'<link rel="stylesheet" href="/assets/css/style\.css(\?v=[^"]*)?" />')
    
    count = 0
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = pattern_js.sub(f'<script type="module" src="/assets/js/main.js?v={version}"></script>', content)
        content = pattern_css.sub(f'<link rel="stylesheet" href="/assets/css/style.css?v={version}" />', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
    print(f"Updated {count} HTML files with version: v={version}")

def update_sw():
    path = os.path.join(workspace, 'sw.js')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r"const CACHE_NAME = 'image_converter_cache_v\d+';", f"const CACHE_NAME = 'image_converter_cache_{version}';", content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated sw.js cache name.")

if __name__ == "__main__":
    print("Starting build process...")
    build_css()
    update_html_versions()
    update_sw()
    print("Build complete!")
