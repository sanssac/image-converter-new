import os
import glob

base_dir = r"c:\image converter new"
old_domain = "image-converter-rho-six.vercel.app"
new_domain = "imglabconverter.vercel.app"

# We want to check all html files, the sitemap, robots.txt, etc.
# Basically everything text-based.
file_types = ['**/*.html', '**/*.xml', '**/*.txt', '**/*.js', '**/*.json', '**/*.md']
files_to_check = []

for ext in file_types:
    files_to_check.extend(glob.glob(os.path.join(base_dir, ext), recursive=True))

count = 0
for filepath in files_to_check:
    if '.git' in filepath:
        continue
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if old_domain in content:
            updated_content = content.replace(old_domain, new_domain)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            count += 1
            print(f"Updated {os.path.relpath(filepath, base_dir)}")
    except Exception as e:
        pass

print(f"\nSuccessfully updated the domain in {count} files.")
