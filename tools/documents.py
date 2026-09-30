#!/usr/bin/env python3
"""İndirilebilir Belgeler: the /belgeler/ page and the sidebar box on every page.

The list itself lives in data/belgeler.json, which is edited from the Pages CMS
screen (app.pagescms.org). Pages read that file when they open, so a document
added there appears on the site as soon as the deploy finishes; no rebuild needed.
Usage: python3 tools/documents.py   (only needed if this script changes)
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# shared script: fetch the list (from this host, which also works inside Google's translation window)
LOADER = r"""function kfdBelgeler(cb){var o=location.origin;fetch(o+'/data/belgeler.json?'+Date.now()).then(function(r){return r.json();})
.then(function(l){l=(Array.isArray(l)?l:[]).filter(function(b){return b&&b.baslik&&b.dosya;});
l.sort(function(a,b){return String(b.tarih||'').localeCompare(String(a.tarih||''));});cb(l);}).catch(function(){});}
function kfdEsc(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;}
function kfdHref(f){f=String(f||'');return /^https?:/.test(f)?f:'https://klinikfarmakoloji.com'+(f.charAt(0)==='/'?'':'/')+f;}
function kfdType(f){var m=String(f).toLowerCase().match(/\.([a-z0-9]+)(?:$|\?)/);return m?m[1].toUpperCase():'';}"""

SIDEBAR = '''<div class="view-content kfd-belge-box"><div class="views-row"><div class="views-field views-field-title"><span class="field-content"><a href="/belgeler">Tüm belgeler</a></span></div></div></div>
<script>(function(){''' + LOADER + '''
var box=document.currentScript.previousElementSibling;
kfdBelgeler(function(l){ if(!l.length) return;
  box.innerHTML=l.slice(0,5).map(function(b){return '<div class="views-row"><div class="views-field views-field-title"><span class="field-content"><a href="'+kfdHref(b.dosya)+'" target="_blank" rel="noopener">'+kfdEsc(b.baslik)+'</a></span></div></div>';}).join('')
   +'<div class="views-row"><div class="views-field views-field-title"><span class="field-content"><a href="/belgeler"><b>Tüm belgeler »</b></a></span></div></div>';
});})();</script>'''

PAGE_BODY = '''<div id="kfd-belgeler">
<style>
#kfd-belgeler{font-family:Georgia,"Times New Roman",serif;color:#1c1a1b}
.kfd-belge{display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-bottom:1px dotted #d0c5b3}
.kfd-belge .ft{flex:0 0 52px;text-align:center;font:bold 13px Georgia,serif;color:#fff;background:#651320;border-radius:3px;padding:10px 0}
.kfd-belge a.t{font-weight:bold;color:#651320;font-size:1.08em;text-decoration:none}
.kfd-belge a.t:hover{text-decoration:underline}
.kfd-belge p{margin:4px 0 0;font-size:.95em;line-height:1.45}
.kfd-belge .d{font-size:.8em;color:#666}
</style>
<div id="kfd-belge-list"><p>Belgeler yükleniyor…</p></div>
<script>(function(){''' + LOADER + '''
var el=document.getElementById('kfd-belge-list');
kfdBelgeler(function(l){
  if(!l.length){ el.innerHTML='<p>Henüz belge eklenmemiş.</p>'; return; }
  el.innerHTML=l.map(function(b){ var t=b.tarih?String(b.tarih).slice(0,10).split('-').reverse().join('.'):'';
    return '<div class="kfd-belge"><div class="ft">'+(kfdType(b.dosya)||'DOSYA')+'</div><div><a class="t" href="'+kfdHref(b.dosya)+'" target="_blank" rel="noopener">'+kfdEsc(b.baslik)+'</a>'
      +(t?'<div class="d">'+t+'</div>':'')+(b.aciklama?'<p>'+kfdEsc(b.aciklama)+'</p>':'')+'</div></div>'; }).join('');
});})();</script>
</div>'''

BLOCK_ID = 'id="block-views-block-indirilebilir-belgeler-block-1"'
TAG = re.compile(r'<(/?)div\b')

def div_end(t, s):
    d = 0
    for m in TAG.finditer(t, s):
        d += -1 if m.group(1) else 1
        if d == 0: return t.find('>', m.start()) + 1

def sidebar(t):
    i = t.find(BLOCK_ID)
    if i < 0: return t
    b = t.rfind('<div', 0, i); e = div_end(t, b)
    blk = t[b:e]
    c = blk.find('<div class="content">')
    if c < 0: return t
    ce = div_end(blk, c)
    new = blk[:c] + '<div class="content">' + SIDEBAR + '</div>' + blk[ce:]
    return t[:b] + new + t[e:]

def build_page():
    tpl = open(os.path.join(ROOT, 'iletisim', 'index.html'), encoding='utf-8').read()
    s = tpl.find('id="block-topplus-lite-content"'); s = tpl.rfind('<', 0, s); e = div_end(tpl, s)
    page = tpl[:s] + '<div id="block-topplus-lite-content" class="clearfix block block-system block-system-main-block"><div class="content">' + PAGE_BODY + '</div></div>' + tpl[e:]
    page = re.sub(r'<title>.*?</title>', '<title>İndirilebilir Belgeler | Klinik Farmakoloji Dosyası</title>', page, count=1, flags=re.S)
    page = re.sub(r'(<h1 class="title page-title"[^>]*>)(.*?)(</h1>)', r'\1İndirilebilir Belgeler\3', page, count=1, flags=re.S)
    page = re.sub(r'(<ol class="breadcrumb__items">.*?<span>)İletişim(</span>)', r'\1İndirilebilir Belgeler\2', page, count=1, flags=re.S)
    page = re.sub(r'<meta name="description" content="[^"]*" ?/?>', '<meta name="description" content="Klinik Farmakoloji Dosyası: indirilebilir belgeler, kitapçıklar ve raporlar." />', page, count=1)
    page = re.sub(r'<meta property="og:(url|title|description)"[^>]*>\s*', '', page)
    page = sidebar(page)
    os.makedirs(os.path.join(ROOT, 'belgeler'), exist_ok=True)
    open(os.path.join(ROOT, 'belgeler', 'index.html'), 'w', encoding='utf-8').write(page)

def main():
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', '.git/', 'pagefind/', 'belgeler/')): continue
        t = open(fp, encoding='utf-8').read(); t2 = sidebar(t)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
    build_page()
    print(f'documents box on {n} pages; /belgeler/ page written')

if __name__ == '__main__':
    main()
