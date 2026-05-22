import re

file_path = r"c:\image converter new\scripts\translate_locales.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's find the 'jpeg-to-webp' dictionary in the file
start_idx = content.find("'jpeg-to-webp': {")
if start_idx == -1:
    start_idx = content.find('"jpeg-to-webp": {')

if start_idx != -1:
    print(content[start_idx:start_idx+1500])
else:
    print("Not found jpeg-to-webp dictionary")
