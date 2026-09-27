#!/usr/bin/env python3
"""Report internal links/images that point to files missing from the static site."""
import os,re,html,urllib.parse,collections
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTR=re.compile(r'''\s(?:href|src|data-src|srcset)\s*=\s*["']([^"']+)["']''',re.I)
CSSU=re.compile(r'''url\(\s*['"]?([^'")]+)['"]?\s*\)''')
def exists(p):
    p=urllib.parse.unquote(p.split('#')[0].split('?')[0])
    fp=os.path.join(ROOT,p.lstrip('/'))
    return os.path.isfile(fp) or os.path.isfile(os.path.join(fp,'index.html'))
broken=collections.defaultdict(set)
for root,dirs,files in os.walk(ROOT):
    dirs[:]=[d for d in dirs if d not in ('.git','tools')]
    for f in files:
        if not f.endswith(('.html','.css')): continue
        fp=os.path.join(root,f); rel='/'+os.path.relpath(fp,ROOT)
        t=open(fp,encoding='utf-8',errors='replace').read()
        for u in ATTR.findall(t)+CSSU.findall(t):
            u=html.unescape(u.strip().split(' ')[0])
            if not u or u.startswith(('#','mailto:','tel:','javascript:','data:','http:','https:','//')): continue
            if not u.startswith('/'): u=urllib.parse.urljoin(rel,u)
            if not exists(u): broken[u].add(rel)
print('broken targets:',len(broken))
for u,s in sorted(broken.items(),key=lambda x:-len(x[1])): print(len(s),u,'<-',sorted(s)[0])
