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
.kfd-lang button{border:1px solid #651320;background:#fff;color:#651320;font:bold 13px/1 Georgia,serif;padding:6px 11px;border-radius:3px;cursor:pointer;letter-spacing:.5px}
.kfd-lang button.on{background:#651320;color:#fff;cursor:default}
@media (max-width:767px){.kfd-lang{justify-content:center;padding:6px 0 0}}
</style>
<button type="button" id="kfd-tr" class="on" title="Türkçe">TR</button><button type="button" id="kfd-en" title="English (automatic translation)">EN</button>
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
