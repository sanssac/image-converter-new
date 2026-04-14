import os, re, glob

# The bug: after </div></div> (closing action-row + result-card),
# the related-tools section and seo-article are outside <main>.
# They need to be INSIDE <main> before </main>.
# Fix: move the orphaned blocks to be inside main, just before </main>.

PATTERN = re.compile(
    r'(      </div>\n    </div>\n)\n'   # action-row + result-card close
    r'(\s*<!-- Related SEO Internal Links -->.*?</article>\n)\n'  # orphaned content
    r'(\s*</main>)',                     # closing main
    re.DOTALL
)

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find closing of result-card then orphaned section/article THEN </main>
    # We will find the result-card close, then look for the pattern where
    # related-tools and article are outside main indentation
    
    # Pattern: result-card closes, then we have indented-wrong blocks before </main>
    old_pattern = re.compile(
        r'(      </div>\r?\n    </div>\r?\n)'       # closes action-row then result-card
        r'(\r?\n      <!-- Related SEO.*?</article>\r?\n)'  # orphaned seo content  
        r'(\r?\n    </main>)',                        # main close
        re.DOTALL
    )
    
    def replacer(m):
        # Put the orphaned content INSIDE <main> with correct indentation
        seo_block = m.group(2)
        # Re-indent from 6 spaces to 4 spaces to put it inside main
        seo_block = re.sub(r'^      ', '    ', seo_block, flags=re.MULTILINE)
        return m.group(1) + seo_block + m.group(3)
    
    new_content, count = old_pattern.subn(replacer, content)
    
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Fixed: {path}")
        return True
    else:
        print(f"  Skip (no match): {path}")
        return False

fixed = 0
for filepath in glob.glob('**\\*.html', recursive=True):
    if '.git' in filepath or 'scratch' in filepath:
        continue
    if fix_file(filepath):
        fixed += 1

print(f"\nTotal fixed: {fixed} files")
