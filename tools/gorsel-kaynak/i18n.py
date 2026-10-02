#!/usr/bin/env python3
"""extract:  i18n.py extract tpl            -> prints JSON list of translatable keys
   render:   i18n.py render tpl[:WxH] ...   -> tpl.<lang>.png for every language in tpl.i18n.json"""
import sys, json, os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
DEVA = '/home/claude/fonts/node_modules/@fontsource/noto-sans-devanagari/files/noto-sans-devanagari-devanagari-%s-normal.woff2'
FONT = {'hi': "@font-face{font-family:KFDDeva;font-weight:400;src:url('file://%s')}@font-face{font-family:KFDDeva;font-weight:700;src:url('file://%s')}*{font-family:KFDDeva,'DejaVu Sans',sans-serif !important}" % (DEVA % '400', DEVA % '700'),
        'zh': "*{font-family:'Noto Sans CJK SC','Noto Sans CJK TC','DejaVu Sans',sans-serif !important}",
        'ja': "*{font-family:'Noto Sans CJK JP','Noto Sans CJK TC','DejaVu Sans',sans-serif !important}"}
JS = r'''
(tr)=>{
 const INL=new Set(['B','I','EM','STRONG','SMALL','BR','SPAN','U','SUP','SUB']);
 const norm=s=>s.replace(/\s+/g,' ').trim();
 const keys=[],miss=[];
 function leaf(el){ if(![...el.childNodes].some(n=>n.nodeType===3&&n.nodeValue.trim())&&!el.children.length) return false;
   return [...el.children].every(c=>INL.has(c.tagName.toUpperCase())&&leafInline(c)); }
 function leafInline(el){ return [...el.children].every(c=>INL.has(c.tagName.toUpperCase())&&leafInline(c)); }
 function hasLetters(s){ return /[A-Za-zÀ-ɏ]{2,}/.test(s.replace(/<[^>]+>/g,'')); }
 function walk(el){
   const tag=el.tagName.toLowerCase();
   if(tag==='style'||tag==='script') return;
   if(tag==='text'||tag==='tspan'){ const k=norm(el.textContent); if(k&&hasLetters(k)){ keys.push(k); if(tr){ if(tr[k]!==undefined) el.textContent=tr[k]; else miss.push(k);} } return; }
   if(el.namespaceURI&&el.namespaceURI.indexOf('svg')>0){ [...el.children].forEach(walk); return; }
   if(norm(el.textContent)&&leaf(el)){ const k=norm(el.innerHTML); if(hasLetters(k)){ keys.push(k); if(tr){ if(tr[k]!==undefined) el.innerHTML=tr[k]; else miss.push(k);} } return; }
   [...el.childNodes].forEach(n=>{ if(n.nodeType===3){ const k=norm(n.nodeValue); if(k&&hasLetters(k)){ keys.push(k); if(tr){ if(tr[k]!==undefined) n.nodeValue=tr[k]; else miss.push(k);} } } else if(n.nodeType===1) walk(n); });
 }
 walk(document.body);
 return {keys,miss};
}'''
FIT = r'''
()=>{
 const H=document.body.clientHeight, W=document.body.clientWidth;
 const texty=el=>[...el.childNodes].some(n=>n.nodeType===3&&n.nodeValue.trim());
 function shrink(root,f){ const els=[root,...root.querySelectorAll('*')]; const sizes=els.map(e=>parseFloat(getComputedStyle(e).fontSize));
   els.forEach((e,i)=>{ if(e.namespaceURI.indexOf('svg')>0) return; e.style.fontSize=(sizes[i]*f)+'px'; }); }
 function over(){ const out=[]; document.querySelectorAll('body *').forEach(e=>{ if(e.namespaceURI.indexOf('svg')>0) return; const cs=getComputedStyle(e); if(cs.display==='inline') return;
   if(!e.textContent.trim()) return;
   if(e.scrollHeight>e.clientHeight*(e.clientHeight<120?1.15:1.03)+3||e.scrollWidth>e.clientWidth+2){ out.push(e); } }); 
   return out.filter(e=>!out.some(o=>o!==e&&e.contains(o))); }
 function flowBad(){ const foot=[...document.querySelectorAll('.foot')].filter(f=>getComputedStyle(f).position==='absolute'); if(!foot.length) return false;
   const top=Math.min(...foot.map(f=>f.getBoundingClientRect().top)); let b=0;
   [...document.body.children].forEach(c=>{ if(getComputedStyle(c).position==='absolute'||c.tagName==='STYLE'||c.tagName==='SCRIPT') return; b=Math.max(b,c.getBoundingClientRect().bottom); });
   return b>top-8; }
 // svg text with data-max
 document.querySelectorAll('text[data-max]').forEach(t=>{ const m=+t.getAttribute('data-max'); let fs=parseFloat(getComputedStyle(t).fontSize),n=0; while(t.getComputedTextLength()>m&&n++<40){ fs*=0.95; t.style.fontSize=fs+'px'; } });
 for(let i=0;i<60;i++){ const o=over(); if(!o.length) break; o.forEach(e=>shrink(e,0.95)); }
 for(let i=0;i<40&&(flowBad()||document.documentElement.scrollHeight>H+2);i++){ shrink(document.body,0.97); }
 for(let i=0;i<30;i++){ const o=over(); if(!o.length) break; o.forEach(e=>shrink(e,0.95)); }
 return over().map(e=>(e.className||e.tagName)+': '+e.textContent.trim().slice(0,30));
}'''
def main():
    mode = sys.argv[1]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for a in sys.argv[2:]:
            tpl, _, size = a.partition(':'); w, h = (size or '1080x1080').split('x')
            pg = b.new_page(viewport={'width': int(w), 'height': int(h)})
            url = f'file://{HERE}/{tpl}.html'
            if mode == 'extract':
                pg.goto(url); print(json.dumps(list(dict.fromkeys(pg.evaluate(JS, None)['keys'])), ensure_ascii=False, indent=0)); continue
            tr = json.load(open(f'{HERE}/{tpl}.i18n.json', encoding='utf-8'))
            for lang, table in tr.items():
                pg.goto(url)
                if lang in FONT: pg.add_style_tag(content=FONT[lang])
                r = pg.evaluate(JS, table)
                pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
                left = pg.evaluate(FIT)
                pg.screenshot(path=f'{HERE}/out/{tpl}.{lang}.png')
                if r['miss'] or left: print(tpl, lang, 'MISSING:', r['miss'], 'OVERFLOW:', left)
            pg.close()
        b.close()
if __name__=="__main__": main()
