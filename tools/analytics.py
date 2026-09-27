#!/usr/bin/env python3
"""Add the GoatCounter visit counter (private statistics, no cookies) to every page. Safe to re-run.
Dashboard: https://klinikfarmakoloji.goatcounter.com
Usage: python3 tools/analytics.py
"""
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = 'klinikfarmakoloji'
TAG = f'<script data-goatcounter="https://{CODE}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
OLD = re.compile(r'\n?<script data-goatcounter="[^"]*"[^>]*></script>')

def main():
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', '.git/')): continue
        t = open(fp, encoding='utf-8').read()
        if 'http-equiv="refresh"' in t[:600] or '</body>' not in t: continue
        t2 = OLD.sub('', t).replace('</body>', TAG + '\n</body>', 1)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
    print(f'visit counter on {n} pages')

if __name__ == '__main__':
    main()
