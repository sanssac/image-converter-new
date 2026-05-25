import os
import re

def fix_html_files():
    workspace = r"c:\image converter new"
    pattern = re.compile(r'(<div class="trust-badge">[\s\S]*?<\/div>)\s*<\/div>(\s*<div class="file-gallery")', re.IGNORECASE)
    
    count = 0
    for root, dirs, files in os.walk(workspace):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if pattern.search(content):
                    new_content = pattern.sub(r"\1\2", content)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed extra </div> in: {path}")
                    count += 1
                    
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    fix_html_files()
