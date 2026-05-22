import re

file_path = r"c:\image converter new\scripts\translate_locales.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's find all the keys in TOOL_TRANSLATIONS
keys = re.findall(r"['\"]([a-zA-Z0-9_-]+\.html|[a-zA-Z0-9_-]+)['\"]\s*:\s*\{", content)
print("Keys found in TOOL_TRANSLATIONS:", keys)
