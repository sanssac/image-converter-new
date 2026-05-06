import os
import glob

workspace = "c:\\image converter new"
old_version = "v=20260424"
new_version = "v=20260506"

html_files = glob.glob(os.path.join(workspace, "**", "*.html"), recursive=True)

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_version in content:
        content = content.replace(old_version, new_version)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Updated {count} files with new version tag: {new_version}")
