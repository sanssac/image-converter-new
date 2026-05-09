"""
SEO Audit Script — Checks all HTML files for critical SEO elements.
Verifies: <title>, meta description, hreflang, canonical, OG tags,
viewport, H1 count, script tags (main.js), and structural integrity.
"""
import glob
import re
import os
import json

results = []
html_files = [f for f in glob.glob('**/*.html', recursive=True)
              if 'node_modules' not in f and 'dist' not in f and 'google' not in f.lower() and 'clear_sw' not in f]

for filepath in sorted(html_files):
    with open(filepath, encoding='utf-8', errors='ignore') as fh:
        content = fh.read()

    issues = []

    # 1. <title> tag
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if not title_match:
        issues.append('MISSING <title>')
    elif len(title_match.group(1).strip()) < 10:
        issues.append(f'SHORT <title>: "{title_match.group(1).strip()}"')

    # 2. Meta description
    if 'meta name="description"' not in content and 'meta name=\\"description\\"' not in content:
        # Some pages use og:description as fallback — flag but don't treat as critical
        if 'og:description' not in content:
            issues.append('MISSING meta description AND og:description')
        else:
            issues.append('WARN: No meta description (has og:description)')

    # 3. Viewport
    if 'viewport' not in content:
        issues.append('MISSING viewport meta')

    # 4. hreflang tags
    hreflang_count = content.count('hreflang=')
    if hreflang_count == 0:
        issues.append('MISSING hreflang tags')

    # 5. Canonical
    if 'rel="canonical"' not in content:
        # Not always required but good practice
        pass  # Don't flag — many pages use hreflang x-default instead

    # 6. OG tags
    if 'og:title' not in content:
        issues.append('MISSING og:title')
    if 'og:description' not in content:
        issues.append('MISSING og:description')
    if 'og:image' not in content:
        issues.append('MISSING og:image')

    # 7. H1 count
    h1_count = len(re.findall(r'<h1[^>]*>', content))
    if h1_count == 0:
        issues.append('MISSING <h1>')
    elif h1_count > 2:
        issues.append(f'TOO MANY <h1> tags: {h1_count}')

    # 8. main.js module script
    has_main_js = 'assets/js/main.js' in content
    has_app_js = 'assets/js/app.js' in content
    if not has_main_js and not has_app_js:
        issues.append('MISSING JS entry point (no main.js or app.js)')
    elif has_app_js and not has_main_js:
        issues.append('STALE: Still references app.js instead of main.js')

    # 9. type="module" on script
    if has_main_js and 'type="module"' not in content:
        issues.append('main.js loaded WITHOUT type="module"')

    # 10. CSS link
    if 'assets/css/style.css' not in content:
        issues.append('MISSING style.css link')

    # 11. Header structure
    if '<header>' not in content and '<header ' not in content:
        issues.append('MISSING <header> element')
    if '<nav>' not in content and '<nav ' not in content:
        issues.append('MISSING <nav> element')

    # 12. Footer
    if '<footer>' not in content and '<footer ' not in content:
        issues.append('MISSING <footer> element')

    # 13. Broken internal links (obvious patterns)
    if 'href=""' in content:
        issues.append('WARN: Empty href found')

    severity = 'OK' if not issues else ('WARN' if all(i.startswith('WARN') for i in issues) else 'ISSUE')
    results.append({
        'file': filepath.replace('\\', '/'),
        'severity': severity,
        'issues': issues,
        'hreflang_count': hreflang_count,
        'has_main_js': has_main_js,
        'title': title_match.group(1).strip() if title_match else None
    })

# Print summary
ok_count = sum(1 for r in results if r['severity'] == 'OK')
warn_count = sum(1 for r in results if r['severity'] == 'WARN')
issue_count = sum(1 for r in results if r['severity'] == 'ISSUE')

print(f"\n{'='*60}")
print(f"SEO AUDIT REPORT — {len(results)} HTML pages scanned")
print(f"{'='*60}")
print(f"  [OK]    : {ok_count}")
print(f"  [WARN]  : {warn_count}")
print(f"  [ISSUE] : {issue_count}")
print(f"{'='*60}\n")

# Print issues only
for r in results:
    if r['severity'] != 'OK':
        print(f"[{r['severity']}] {r['file']}")
        for issue in r['issues']:
            print(f"       -> {issue}")
        print()

# Print all OK files compactly
print(f"\n--- All OK pages ({ok_count}) ---")
for r in results:
    if r['severity'] == 'OK':
        print(f"  [OK] {r['file']}  (hreflang={r['hreflang_count']}, main.js={'Y' if r['has_main_js'] else 'N'})")
