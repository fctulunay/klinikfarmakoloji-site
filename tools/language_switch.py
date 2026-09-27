#!/usr/bin/env python3
"""TR / EN language switch in the header of every page (safe to re-run).

EN opens the same page through Google's page-translation service (<host>.translate.goog), which
translates the whole page (menus, sidebars, articles) and keeps the visitor in English as they
click through the site. TR returns to the original Turkish page.
Usage: python3 tools/language_switch.py
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOR = '<div class="region region-header-top-highlighted-second">'
BLOCK = '''<div class="kfd-lang notranslate" translate="no">
<style>
.kfd-lang{display:flex;justify-content:flex-end;gap:6px;padding:8px 4px 4px;font-family:Georgia,serif}
.kfd-lang button{display:inline-flex;padding:0;border:2px solid transparent;border-radius:3px;background:none;cursor:pointer;line-height:0;opacity:.8;box-shadow:0 0 0 1px rgba(0,0,0,.15)}
.kfd-lang button:hover{opacity:1}
.kfd-lang button.on{border-color:#651320;opacity:1;cursor:default}
@media (max-width:767px){.kfd-lang{justify-content:center;padding:6px 0 0}}
</style>
<button type="button" id="kfd-tr" class="on" title="Türkçe" aria-label="Türkçe"><svg viewBox="0 0 1200 800" width="33" height="22" aria-hidden="true"><rect width="1200" height="800" fill="#E30A17"/><circle cx="425" cy="400" r="200" fill="#fff"/><circle cx="475" cy="400" r="160" fill="#E30A17"/><path fill="#fff" d="M583.334 400l180.901 58.779-111.804-153.885v190.212l111.804-153.885z"/></svg></button><button type="button" id="kfd-en" title="English (automatic translation)" aria-label="English"><svg viewBox="0 0 1900 1000" width="42" height="22" aria-hidden="true"><rect width="1900" height="1000" fill="#B22234"/><rect y="76.9" width="1900" height="76.9" fill="#fff"/><rect y="230.8" width="1900" height="76.9" fill="#fff"/><rect y="384.6" width="1900" height="76.9" fill="#fff"/><rect y="538.5" width="1900" height="76.9" fill="#fff"/><rect y="692.3" width="1900" height="76.9" fill="#fff"/><rect y="846.2" width="1900" height="76.9" fill="#fff"/><rect width="760" height="538.5" fill="#3C3B6E"/><defs><polygon id="kfd-us-star" fill="#fff" points="0.0,-30.8 6.9,-9.5 29.3,-9.5 11.2,3.6 18.1,24.9 0.0,11.8 -18.1,24.9 -11.2,3.6 -29.3,-9.5 -6.9,-9.5"/></defs><use href="#kfd-us-star" x="63" y="54"/><use href="#kfd-us-star" x="189" y="54"/><use href="#kfd-us-star" x="315" y="54"/><use href="#kfd-us-star" x="441" y="54"/><use href="#kfd-us-star" x="567" y="54"/><use href="#kfd-us-star" x="693" y="54"/><use href="#kfd-us-star" x="126" y="108"/><use href="#kfd-us-star" x="252" y="108"/><use href="#kfd-us-star" x="378" y="108"/><use href="#kfd-us-star" x="504" y="108"/><use href="#kfd-us-star" x="630" y="108"/><use href="#kfd-us-star" x="63" y="162"/><use href="#kfd-us-star" x="189" y="162"/><use href="#kfd-us-star" x="315" y="162"/><use href="#kfd-us-star" x="441" y="162"/><use href="#kfd-us-star" x="567" y="162"/><use href="#kfd-us-star" x="693" y="162"/><use href="#kfd-us-star" x="126" y="216"/><use href="#kfd-us-star" x="252" y="216"/><use href="#kfd-us-star" x="378" y="216"/><use href="#kfd-us-star" x="504" y="216"/><use href="#kfd-us-star" x="630" y="216"/><use href="#kfd-us-star" x="63" y="270"/><use href="#kfd-us-star" x="189" y="270"/><use href="#kfd-us-star" x="315" y="270"/><use href="#kfd-us-star" x="441" y="270"/><use href="#kfd-us-star" x="567" y="270"/><use href="#kfd-us-star" x="693" y="270"/><use href="#kfd-us-star" x="126" y="324"/><use href="#kfd-us-star" x="252" y="324"/><use href="#kfd-us-star" x="378" y="324"/><use href="#kfd-us-star" x="504" y="324"/><use href="#kfd-us-star" x="630" y="324"/><use href="#kfd-us-star" x="63" y="378"/><use href="#kfd-us-star" x="189" y="378"/><use href="#kfd-us-star" x="315" y="378"/><use href="#kfd-us-star" x="441" y="378"/><use href="#kfd-us-star" x="567" y="378"/><use href="#kfd-us-star" x="693" y="378"/><use href="#kfd-us-star" x="126" y="432"/><use href="#kfd-us-star" x="252" y="432"/><use href="#kfd-us-star" x="378" y="432"/><use href="#kfd-us-star" x="504" y="432"/><use href="#kfd-us-star" x="630" y="432"/><use href="#kfd-us-star" x="63" y="486"/><use href="#kfd-us-star" x="189" y="486"/><use href="#kfd-us-star" x="315" y="486"/><use href="#kfd-us-star" x="441" y="486"/><use href="#kfd-us-star" x="567" y="486"/><use href="#kfd-us-star" x="693" y="486"/></svg></button>
<script>
(function(){
  var S='.translate.goog', h=location.hostname, inEN=h.slice(-S.length)===S;
  var tr=document.getElementById('kfd-tr'), en=document.getElementById('kfd-en');
  function origHost(){return h.slice(0,-S.length).replace(/--/g,'\\u0000').replace(/-/g,'.').replace(/\\u0000/g,'-');}
  function encHost(x){return x.replace(/-/g,'--').replace(/\\./g,'-');}
  if(inEN){tr.className='';en.className='on';}
  tr.onclick=function(){if(inEN){location.href='https://'+origHost()+location.pathname+location.hash;}};
  en.onclick=function(){if(!inEN){location.href='https://'+encHost(h)+S+location.pathname+'?_x_tr_sl=tr&_x_tr_tl=en&_x_tr_hl=en'+location.hash;}};
})();
</script>
</div>'''
OLD = re.compile(r'\n?<div class="kfd-lang notranslate".*?</script>\n</div>', re.S)

def main():
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', '.git/')): continue
        t = open(fp, encoding='utf-8').read()
        if ANCHOR not in t: continue
        t2 = OLD.sub('', t)
        t2 = t2.replace(ANCHOR, ANCHOR + '\n' + BLOCK, 1)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
    print(f'language switch on {n} pages')

if __name__ == '__main__':
    main()
