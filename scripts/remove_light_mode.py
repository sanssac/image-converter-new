import glob
import re
import os

def process_html_files():
    html_files = glob.glob('**/*.html', recursive=True)
    print(f"Total HTML files found: {len(html_files)}")
    
    # 1. Regex to remove theme toggle button
    theme_toggle_regex = re.compile(r'[ \t]*<button[^>]*class=["\'][^"\']*theme-toggle[^"\']*["\'][^>]*>[\s\S]*?</button>\s*', re.IGNORECASE)
    
    # 2. Regex to remove/replace theme-color meta tags
    # We want: <meta name="theme-color" content="#09090b" /> (single dark tag, no media query needed since it's dark-only)
    light_meta_regex = re.compile(r'[ \t]*<meta\s+name=["\']theme-color["\'][^>]*content=["\']#f8fafc["\'][^>]*>\s*', re.IGNORECASE)
    dark_meta_regex = re.compile(r'[ \t]*<meta\s+name=["\']theme-color["\'][^>]*content=["\']#09090b["\'][^>]*media=["\'][^"\']*dark[^"\']*["\'][^>]*>\s*', re.IGNORECASE)
    
    # 3. Inline data-theme light rules (like in contact or compress-image)
    inline_light_theme_regex = re.compile(r'[ \t]*\[data-theme=["\']light["\']\][^{]*\{[^}]*\}\s*', re.IGNORECASE)
    
    modified_count = 0
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content
        
        # Remove theme toggle button
        content = theme_toggle_regex.sub('', content)
        
        # Remove light meta
        content = light_meta_regex.sub('', content)
        
        # Replace dark meta with media query with clean dark meta
        content = dark_meta_regex.sub('\n  <meta name="theme-color" content="#09090b" />\n', content)
        
        # Remove inline data-theme light rules
        content = inline_light_theme_regex.sub('', content)
        
        if content != orig_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            modified_count += 1
            
    print(f"Modified {modified_count} HTML files.")

if __name__ == '__main__':
    process_html_files()
