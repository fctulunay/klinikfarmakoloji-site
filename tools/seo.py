#!/usr/bin/env python3
"""Search-engine tidy-up. Safe to re-run after any content change.

1. every page's canonical link = its full address on https://klinikfarmakoloji.com
   (no trailing slash, the form Google has indexed for years), so www / http /
   slash variants and the Google-translate copies all count as one page
2. a <meta name="description"> on every page that has a share description
3. sitemap.xml lists every real page in that same form
Usage: python3 tools/seo.py
"""
import os, re, glob, html, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://klinikfarmakoloji.com'
SKIP = ('index.php/', 'node/', 'tools/', 'pagefind/', '.git/', 'sites/', 'core/', 'modules/', 'themes/', 'libraries/')
NOINDEX = ('arama/', 'yeni-tasarim/')

def page_path(rel):
    d = os.path.dirname(rel).replace(os.sep, '/')
    return '/' if d in ('', '.') else '/' + d

def main():
    n = 0; urls = []
    for fp in sorted(glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(SKIP): continue
        t = open(fp, encoding='utf-8').read()
        if 'http-equiv="refresh"' in t[:3000]: continue          # redirect stubs
        path = page_path(rel)
        canon = SITE + urllib.parse.quote(path)
        tag = f'<link rel="canonical" href="{canon}" />'
        t2 = re.sub(r'<link rel="canonical" href="[^"]*" ?/?>', tag, t, count=1)
        if tag not in t2: t2 = t2.replace('</title>', '</title>\n' + tag, 1)
        t2 = re.sub(r'<meta name="description" content="\s*" ?/?>\s*', '', t2)   # empty ones from the old site
        def tidy(m):
            d = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()
            if len(d) > 160: d = d[:157].rsplit(' ', 1)[0] + '…'
            return '<meta name="description" content="' + html.escape(d, quote=True) + '" />'
        t2 = re.sub(r'<meta name="description" content="([^"]*)" ?/?>', tidy, t2)
        if '<meta name="description"' not in t2:
            m = re.search(r'<meta property="og:description" content="([^"]*)"', t2)
            if m and m.group(1).strip():
                d = html.unescape(m.group(1)).strip()
                if len(d) > 160: d = d[:157].rsplit(' ', 1)[0] + '…'
                t2 = t2.replace(tag, tag + '\n<meta name="description" content="' + html.escape(d, quote=True) + '" />', 1)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
        if not rel.startswith(NOINDEX) and '/page/' not in path and 'noindex' not in t2[:5000]:
            urls.append(canon)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    print(f'seo: {n} pages updated, sitemap has {len(urls)} addresses')

if __name__ == '__main__':
    main()
