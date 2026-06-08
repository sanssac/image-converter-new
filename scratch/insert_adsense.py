import glob
import os
import re

def main():
    base_dir = r"c:\image converter new"
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    
    correct_id = "ca-pub-3257318580709851"
    incorrect_id = "ca-pub-325731850709851"
    meta_tag_str = f'<meta name="google-adsense-account" content="{correct_id}">'
    
    count_corrected = 0
    count_meta_inserted = 0
    count_skipped = 0
    
    for filepath in html_files:
        if '.git' in filepath or 'googlefda0e304c8ec12dc.html' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. Correct the typo in the script tag if the incorrect ID exists
        if incorrect_id in content:
            content = content.replace(incorrect_id, correct_id)
            modified = True
            count_corrected += 1
            
        # 2. Check if the meta tag is already present in the file
        if meta_tag_str not in content:
            # Find the correct script tag and insert the meta tag right before it
            script_pattern = re.compile(
                r'(\s*)<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=ca-pub-3257318580709851" crossorigin="anonymous"></script>'
            )
            
            # Match the script tag and insert the meta tag on the line above with matching indentation
            content, count_sub = script_pattern.subn(
                r'\1' + meta_tag_str + r'\n\1<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3257318580709851" crossorigin="anonymous"></script>',
                content
            )
            
            if count_sub > 0:
                modified = True
                count_meta_inserted += 1
            else:
                print(f"WARNING: Correct script tag not found in {filepath}")
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            count_skipped += 1
            
    print(f"\nExecution Summary:")
    print(f"Corrected ID typos: {count_corrected}")
    print(f"Inserted meta tags: {count_meta_inserted}")
    print(f"Skipped (already correct): {count_skipped}")

if __name__ == "__main__":
    main()
