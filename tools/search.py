#!/usr/bin/env python3
"""Site search (Pagefind). Safe to re-run; run after any content change.

1. marks article pages for indexing (article text, title, section filter, image, date)
2. puts a search box in the header of every page
3. writes the results page /arama/
4. rebuilds the search index in /pagefind/ (needs Node: npx pagefind)
Usage: python3 tools/search.py
"""
import os, re, glob, html, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOR = '<div class="region region-header-top-highlighted-second">'
BOX = '''<form class="kfd-search notranslate" action="/arama/" method="get" role="search">
<style>
.kfd-search{display:flex;justify-content:flex-end;padding:6px 4px 2px;margin:0}
.kfd-search input{width:100%;max-width:230px;font:15px Georgia,serif;padding:6px 10px;border:1px solid #cdbfc3;border-right:0;border-radius:3px 0 0 3px;background:#fff;color:#222}
.kfd-search input:focus{outline:2px solid #651320;outline-offset:0}
.kfd-search button{font:bold 14px Georgia,serif;padding:6px 12px;border:1px solid #651320;background:#651320;color:#fff;border-radius:0 3px 3px 0;cursor:pointer}
@media (max-width:767px){.kfd-search{justify-content:center}.kfd-search input{max-width:none}}
</style>
<label for="kfd-q" class="visually-hidden">Sitede ara</label>
<input id="kfd-q" type="search" name="q" placeholder="Sitede ara…" autocomplete="off"><button type="submit">Ara</button>
</form>'''
OLD_BOX = re.compile(r'\n?<form class="kfd-search notranslate".*?</form>', re.S)

RESULTS = '''<div id="kfd-arama" data-pagefind-ignore>
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<style>
#kfd-arama{--pagefind-ui-primary:#651320;--pagefind-ui-text:#1c1a1b;--pagefind-ui-border:#d0c5b3;--pagefind-ui-tag:#f5eee0;--pagefind-ui-font:Georgia,"Times New Roman",serif;--pagefind-ui-scale:.95}
#kfd-arama .pagefind-ui__result-link{color:#651320}
#kfd-arama .pagefind-ui__result-title{font-size:1.1em}
#kfd-arama mark{background:#f1dfe3;color:inherit}
</style>
<div id="kfd-search-ui"></div>
<script src="/pagefind/pagefind-ui.js"></script>
<script>
window.addEventListener('DOMContentLoaded',function(){
  var ui=new PagefindUI({element:'#kfd-search-ui',showSubResults:true,showImages:true,resetStyles:false,
    translations:{placeholder:'Yazılarda ara (ör. biyoeşdeğerlik, TİTCK, statin)',zero_results:'"[SEARCH_TERM]" için sonuç bulunamadı',many_results:'"[SEARCH_TERM]" için [COUNT] sonuç',one_result:'"[SEARCH_TERM]" için [COUNT] sonuç',load_more:'Daha fazla sonuç',filters_label:'Bölüm',clear_search:'Temizle',searching:'"[SEARCH_TERM]" aranıyor…'}});
  var q=new URLSearchParams(location.search).get('q'); if(q){ui.triggerSearch(q);}
});
</script>
</div>'''

TAG = re.compile(r'<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>')
def span_end(t, s):
    name = TAG.match(t, s).group(2).lower(); d = 0
    for m in TAG.finditer(t, s):
        if m.group(2).lower() != name or m.group(3): continue
        d += -1 if m.group(1) else 1
        if d == 0: return m.end()

def pages():
    for fp in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', 'pagefind/', '.git/')): continue
        yield fp, rel

def mark_article(t):
    a = t.find('<article data-history-node-id')
    if a < 0 or 'node--view-mode-full' not in t[a:a + 400]: return t
    head = t[a:t.find('>', a) + 1]
    if 'data-pagefind-body' not in head:
        t = t[:a] + head.replace('<article ', '<article data-pagefind-body ', 1) + t[a + len(head):]
    t = re.sub(r'<h1 class="title page-title"(?![^>]*data-pagefind-meta)', '<h1 class="title page-title" data-pagefind-meta="title"', t, count=1)
    t = re.sub(r'(<div class="field field--name-field-yazi-turu[^"]*")(?![^>]*data-pagefind-filter)', r'\1 data-pagefind-filter="Bölüm"', t, count=1)
    t = re.sub(r'(<div class="field field--name-field-one-cikan-gorsel[^>]*>\s*<img )(?!data-pagefind-meta)', r'\1data-pagefind-meta="image[src]" ', t, count=1)
    for cls in ('kfd-like', 'a2a_kit', 'node__side'):
        t = re.sub(r'(<(?:div|span) class="' + cls + r'[^"]*")(?![^>]*data-pagefind-ignore)', r'\1 data-pagefind-ignore', t)
    return t

def build_results_page():
    tpl = open(os.path.join(ROOT, 'iletisim', 'index.html'), encoding='utf-8').read()
    s = tpl.find('id="block-topplus-lite-content"'); s = tpl.rfind('<', 0, s); e = span_end(tpl, s)
    page = tpl[:s] + '<div id="block-topplus-lite-content" class="clearfix block block-system block-system-main-block"><div class="content">' + RESULTS + '</div></div>' + tpl[e:]
    page = re.sub(r'<title>.*?</title>', '<title>Arama | Klinik Farmakoloji Dosyası</title>', page, count=1, flags=re.S)
    page = re.sub(r'(<h1 class="title page-title"[^>]*>)(.*?)(</h1>)', r'\1Arama\3', page, count=1, flags=re.S)
    page = re.sub(r'(<ol class="breadcrumb__items">.*?<span>)İletişim(</span>)', r'\1Arama\2', page, count=1, flags=re.S)
    page = re.sub(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="/arama/" />', page, count=1)
    page = page.replace('<head>', '<head>\n<meta name="robots" content="noindex, follow" />', 1)
    page = re.sub(r'\s*<meta property="og:url"[^>]*>', '', page)
    os.makedirs(os.path.join(ROOT, 'arama'), exist_ok=True)
    open(os.path.join(ROOT, 'arama', 'index.html'), 'w', encoding='utf-8').write(page)

def main():
    n = m = 0
    for fp, rel in pages():
        if rel.startswith('arama/'): continue
        t = open(fp, encoding='utf-8').read()
        t2 = mark_article(t)
        if ANCHOR in t2:
            t2 = OLD_BOX.sub('', t2)
            li = t2.find('<div class="kfd-lang notranslate"')
            le = t2.find('</script>\n</div>', li) + len('</script>\n</div>') if li >= 0 else -1
            t2 = (t2[:le] + '\n' + BOX + t2[le:]) if li >= 0 else t2.replace(ANCHOR, ANCHOR + '\n' + BOX, 1)
        if t2 != t:
            open(fp, 'w', encoding='utf-8').write(t2); n += 1
        if 'data-pagefind-body' in t2: m += 1
    build_results_page()
    print(f'search box/markers updated on {n} pages; {m} article pages indexed')
    r = subprocess.run(['npx', '-y', 'pagefind@1', '--site', ROOT, '--glob', '**/index.html', '--force-language', 'tr'],
                       capture_output=True, text=True)
    print(r.stdout[-800:] or r.stderr[-800:])

if __name__ == '__main__':
    main()
