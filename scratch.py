import re
with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    d = f.read()
d = re.sub(r'\s*<span class="mega-badge (popular|new-tool)">[^<]*</span>', '', d)
with open('assets/js/app.js', 'w', encoding='utf-8') as f:
    f.write(d)
