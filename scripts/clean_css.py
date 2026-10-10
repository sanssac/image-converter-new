import re

def clean_css():
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Match rule blocks for data-theme="light"
    rule_pattern = re.compile(r'[ \t]*\[data-theme=["\']light["\']\][^{]*\{[^}]*\}\s*', re.MULTILINE)

    # Theme toggle rules
    toggle_pattern = re.compile(r'[ \t]*\.theme-toggle[^{]*\{[^}]*\}\s*', re.MULTILINE)

    # Theme transition rules
    trans_pattern = re.compile(r'/\*\s*── Interactive Smooth Theme Transitions ──\s*\*/\s*body\.theme-transitioning[\s\S]*?\}\s*', re.MULTILINE)
    trans_body_pattern = re.compile(r'body\.theme-transitioning[\s\S]*?\}\s*', re.MULTILINE)

    # Remove headers/comments related to light mode
    comment_patterns = [
        re.compile(r'/\*[^*]*Light Mode[^*]*\*/\s*', re.IGNORECASE),
        re.compile(r'/\* -- Light Mode Theme Drawer Styles -- \*/\s*', re.IGNORECASE),
        re.compile(r'/\* ── UI Improvement #1: Sticky Header Light Mode ── \*/\s*', re.IGNORECASE),
        re.compile(r'/\* ── Light Mode Theme Engine ────────── \*/\s*', re.IGNORECASE),
        re.compile(r'/\* light mega-link overrides moved above \*/\s*', re.IGNORECASE)
    ]

    new_css = rule_pattern.sub('', css)
    new_css = toggle_pattern.sub('', new_css)
    new_css = trans_pattern.sub('', new_css)
    new_css = trans_body_pattern.sub('', new_css)

    for cp in comment_patterns:
        new_css = cp.sub('', new_css)

    # Compress multiple newlines
    new_css = re.sub(r'\n{3,}', '\n\n', new_css)

    remaining = [l for l in new_css.splitlines() if 'data-theme' in l or 'theme-toggle' in l or 'theme-transitioning' in l]
    print(f"Original length: {len(css)}, New length: {len(new_css)}")
    print(f"Remaining theme lines: {remaining}")

    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(new_css)
    print("style.css updated successfully!")

if __name__ == '__main__':
    clean_css()
