#!/usr/bin/env python3
"""Put a Lyket "like" button under every article (safe to re-run).

The button is identified by section (namespace) + article slug, so likes stay attached to the
article even if its page is rebuilt. Only the public Lyket key goes into the pages.
Usage: python3 tools/like_button.py
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LYKET_PUBLIC_KEY = 'pt_54ac6607631f8847d5b34222e5502f'
SCRIPT = f'<script src="https://unpkg.com/@lyket/widget@latest/dist/lyket.js?apiKey={LYKET_PUBLIC_KEY}" defer></script>'
OLD = re.compile(r'\n?<div class="kfd-like".*?</div></div>|\n?<script src="https://unpkg\.com/@lyket/widget[^"]*"[^>]*></script>', re.S)

def block(namespace, slug):
    return ('\n<div class="kfd-like" style="margin:28px 0 10px; padding-top:14px; border-top:1px solid #d0c5b3; '
            'display:flex; align-items:center; gap:12px; flex-wrap:wrap">'
            '<span style="font-family:Georgia,serif; font-size:15px; color:#651320">Bu yazıyı beğendiniz mi?</span>'
            f'<div data-lyket-type="like" data-lyket-namespace="{namespace}" data-lyket-id="{slug}" '
            'data-lyket-template="simple" data-lyket-color-primary="#651320" data-lyket-color-secondary="#efd9dc" '
            'data-lyket-color-highlight="#651320"></div></div>')

def main():
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        parts = rel.split(os.sep)
        if len(parts) != 3 or parts[0] in ('index.php', 'node', 'tools') or parts[1] == 'page': continue
        t = open(fp, encoding='utf-8').read()
        a = (lambda _m: _m.start() if _m else -1)(re.search(r'<article[^>]*data-history-node-id', t))
        if a < 0 or 'node--view-mode-full' not in t[a:a + 400]: continue
        t = OLD.sub('', t)
        a = (lambda _m: _m.start() if _m else -1)(re.search(r'<article[^>]*data-history-node-id', t))
        b = t.find('property="schema:text"', a)
        if b < 0: continue
        # end of the body field div
        s = t.rfind('<div', 0, b); depth = 0; i = s
        for m in re.finditer(r'<(/?)div\b[^>]*>', t[s:]):
            depth += -1 if m.group(1) else 1
            if depth == 0: i = s + m.end(); break
        t = t[:i] + block(parts[0], parts[1]) + t[i:]
        t = t.replace('</body>', SCRIPT + '\n</body>', 1)
        open(fp, 'w', encoding='utf-8').write(t); n += 1
    print(f'like button on {n} article pages')

if __name__ == '__main__':
    main()
