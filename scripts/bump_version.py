import os
import glob

workspace = "c:\\image converter new"
old_version = "v=20260507"
new_version = "v=20260522"

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

with open(os.path.join(workspace, 'sw.js'), 'r', encoding='utf-8') as f:
    sw_content = f.read()
sw_content = sw_content.replace('image_converter_cache_v11', 'image_converter_cache_v12')
with open(os.path.join(workspace, 'sw.js'), 'w', encoding='utf-8') as f:
    f.write(sw_content)
print("Updated sw.js")
