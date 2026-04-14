import re
import glob

count_fixed = 0

for filepath in glob.glob('**/*.html', recursive=True):
    if '.gemini' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # We need to insert `</div></div>` immediately before `<!-- Related SEO Internal Links -->`.
    # Let's ensure we don't accidentally double-inject it.
    if '</div>\n    </div>\n\n      <!-- Related SEO Internal Links -->' in html or '</div></div><!-- Related' in html.replace(' ',''):
        continue

    # Regex replaces the gap between the last copy button and the Related SEO comment.
    fixed = re.sub(r'(</button>)\s*(<!-- Related SEO Internal Links -->)', r'\1\n      </div>\n    </div>\n\n      \2', html)
    
    # Also check other potential missing tags if seo isn't there
    if fixed != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        count_fixed += 1

print(f"Fixed {count_fixed} files with broken DOM tags.")
