#!/usr/bin/env python3
"""Lists article pictures that still have no language versions.

Looks at pictures in sites/default/files/yazi-gorselleri/cms/ (where the editor uploads go) and
in the <YYYY-MM>/ folders from 2026-10 onward (everything older was handled by hand, see batch1..12) and prints those with no
"<name>.en.png" next to them. Names listed in skip.txt (already English or bilingual
pictures, logos, photos without words) are left out.
Usage: python3 tools/gorsel-kaynak/pending.py
"""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
G = os.path.join(ROOT, 'sites/default/files/yazi-gorselleri')
LANG = re.compile(r'\.(en|de|es|ru|zh|hi|ja)\.(png|jpe?g|webp|gif)$', re.I)
skip = set()
if os.path.exists(HERE + '/skip.txt'):
    skip = {l.strip() for l in open(HERE + '/skip.txt') if l.strip() and not l.startswith('#')}
for d in sorted(os.listdir(G)):
    if d != 'cms' and (not re.match(r'^\d{4}-\d{2}$', d) or d < '2026-10'):
        continue
    for f in sorted(os.listdir(os.path.join(G, d))):
        if LANG.search(f) or not re.search(r'\.(png|jpe?g|webp|gif)$', f, re.I):
            continue
        base = f.rsplit('.', 1)[0]
        rel = d + '/' + base
        if rel in skip or glob.glob(os.path.join(G, d, base + '.en.*')):
            continue
        print(rel + '\t' + f)
