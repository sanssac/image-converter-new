import glob
import os
import re

def main():
    base_dir = r"c:\image converter new"
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    
    adsense_id = "ca-pub-325731850709851"
    adsense_script = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_id}" crossorigin="anonymous"></script>'
    
    count_updated = 0
    count_inserted = 0
    count_skipped = 0
    
    # 1. Regex for files that have the placeholder block
    placeholder_pattern = re.compile(
        r'(<!--\s*<script async src="https://www.googletagmanager.com/gtag/js\?id=G-XXXXXXXXXX"></script>\s*\n\s*'
        r'<script> window\.dataLayer = window\.dataLayer \|\| \[\]; function gtag\(\)\{dataLayer\.push\(arguments\);\} gtag\(\'js\', new Date\(\)\); gtag\(\'config\', \'G-XXXXXXXXXX\'\); </script>\s*\n\s*'
        r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-XXXXXXXXXXXXX" crossorigin="anonymous"></script>\s*-->)',
        re.DOTALL
    )
    
    for filepath in html_files:
        if '.git' in filepath or 'googlefda0e304c8ec12dc.html' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already has active adsense script
        if adsense_id in content:
            count_skipped += 1
            continue
            
        # Try to find and replace placeholder first
        new_content, sub_count = placeholder_pattern.subn(
            f'<!-- <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>\n  <script> window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag(\'js\', new Date()); gtag(\'config\', \'G-XXXXXXXXXX\'); </script> -->\n  {adsense_script}',
            content
        )
        
        if sub_count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count_updated += 1
            print(f"Updated placeholder in: {filepath}")
        else:
            # If no placeholder, insert after Vercel Web Analytics
            vercel_pattern = re.compile(
                r'(\s*)<!-- Vercel Web Analytics -->\s*\n(\s*)<script defer src="/_vercel/insights/script.js"></script>',
                re.DOTALL
            )
            
            new_content, sub_count = vercel_pattern.subn(
                r'\1<!-- Vercel Web Analytics -->\n\2<script defer src="/_vercel/insights/script.js"></script>\n\2' + adsense_script,
                content
            )
            
            if sub_count > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count_inserted += 1
                print(f"Inserted script in: {filepath}")
            else:
                print(f"WARNING: Vercel Web Analytics script not found in: {filepath}")
                
    print(f"\nExecution Summary:")
    print(f"Updated placeholders: {count_updated}")
    print(f"Inserted script tags: {count_inserted}")
    print(f"Skipped (already configured): {count_skipped}")

if __name__ == "__main__":
    main()
