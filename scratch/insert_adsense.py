import glob
import os
import re

def main():
    base_dir = r"c:\image converter new"
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    
    count = 0
    for filepath in html_files:
        if '.git' in filepath or 'googlefda0e304c8ec12dc.html' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match the meta tag, followed by empty space/newlines, followed by the script tag
        pattern = re.compile(
            r'<meta name="google-adsense-account" content="ca-pub-3257318580709851">\s*\n(\s*)<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-3257318580709851" crossorigin="anonymous"></script>'
        )
        
        # Replace to remove any blank lines and keep standard matching indentation
        new_content, sub_count = pattern.subn(
            r'<meta name="google-adsense-account" content="ca-pub-3257318580709851">\n\1<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3257318580709851" crossorigin="anonymous"></script>',
            content
        )
        
        if sub_count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            
    print(f"Cleaned up blank lines in {count} HTML files successfully!")

if __name__ == "__main__":
    main()
