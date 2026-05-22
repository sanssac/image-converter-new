import glob
import os
import re

base_dir = r"c:\image converter new"
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

for filepath in html_files:
    if '.git' in filepath or 'node_modules' in filepath or '__pycache__' in filepath:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    headers = content.count('<header>') + content.count('<header ')
    theme_toggles = content.count('class="theme-toggle"') + content.count("class='theme-toggle'")
    moon_icons = content.count('class="moon-icon"') + content.count("class='moon-icon'")
    
    if headers > 1 or theme_toggles > 1 or moon_icons > 1:
        print(f"{os.path.relpath(filepath, base_dir)}: headers={headers}, theme_toggles={theme_toggles}, moon_icons={moon_icons}")
