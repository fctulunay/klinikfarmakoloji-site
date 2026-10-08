#!/usr/bin/env python3
"""Condensed multilingual article cards. usage: cards.py batchmodule  -> out/<id>.<lang>.png"""
import sys, os, html, importlib
from playwright.sync_api import sync_playwright
from i18n import FIT, FONT
HERE=os.path.dirname(os.path.abspath(__file__))
AI={'en':'Prepared with AI support','de':'Mit KI-Unterstützung erstellt','es':'Elaborado con apoyo de IA','ru':'Подготовлено с помощью ИИ','zh':'借助人工智能编写','hi':'AI की सहायता से तैयार','ja':'AIの支援を受けて作成'}
THEMES={'burg':('#7A1F2B','#E9C46A','#F7F0E3','#2A9D8F'),'navy':('#12305c','#5ec8ff','#eef4fb','#e2572e'),'teal':('#1d6f6a','#f2c14e','#f1f7f5','#d2452e'),'dark':('#1c1f2b','#f2b632','#f3f1ec','#c0392b'),'blue':('#2552b0','#ffd166','#f2f6fd','#2a9d8f'),'purple':('#4b2a7a','#f4c95d','#f6f2fb','#d2452e')}
CSS='''*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1080px;display:flex;flex-direction:column;background:VAR_BG;font-family:'DejaVu Sans',sans-serif;color:#1f2430;overflow:hidden}
.hd{background:VAR_C;color:#fff;padding:34px 48px 30px}
.k{color:VAR_A;font-weight:bold;letter-spacing:3px;font-size:19px;margin-bottom:10px}
h1{font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;font-size:58px;line-height:1.08}
.s{font-size:23px;line-height:1.3;margin-top:12px;opacity:.95}
.stats{display:flex;gap:14px;margin:22px 48px 0;height:190px;flex:none}
.st{flex:1;background:#fff;border-radius:14px;border-top:7px solid VAR_C;padding:14px 16px;box-shadow:0 2px 6px rgba(0,0,0,.08);overflow:hidden}
.st b{display:block;color:VAR_C;font-size:40px;line-height:1.1;font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;white-space:nowrap}
.st span{display:block;font-size:19px;line-height:1.25;margin-top:6px}
.ph{margin:20px 48px 0;font-weight:bold;letter-spacing:2px;color:VAR_C;font-size:19px;flex:none}
.pts{flex:1;min-height:0;margin:14px 48px 14px;display:flex;flex-direction:column;gap:11px;justify-content:center}
.pt{flex:none;background:#fff;border-radius:12px;border-left:7px solid VAR_D;padding:13px 18px;font-size:21px;line-height:1.3;box-shadow:0 1px 4px rgba(0,0,0,.07)}
.pt b{color:VAR_C}
.msg{flex:none;margin:0 48px 14px;background:VAR_A;color:#2a1a08;border-radius:14px;padding:15px 20px;font-size:24px;font-weight:bold;text-align:center;line-height:1.25}
.src{flex:none;margin:0 48px 10px;font-size:14px;color:#555;text-align:center}
.foot{flex:none;height:48px;background:VAR_C;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 48px;font-size:15px;white-space:nowrap;gap:12px}
body.poster .hd{flex:1;display:flex;flex-direction:column;justify-content:center;text-align:center;padding:60px 70px}
body.poster h1{font-size:92px}body.poster .k{font-size:26px;margin-bottom:26px}body.poster .s{font-size:32px;margin-top:26px}
'''
GROW=r'''()=>{const p=document.querySelector('.pts'); if(!p) return; const need=()=>{let h=0;[...p.children].forEach(c=>h+=c.offsetHeight);return h+(p.children.length-1)*11;};
 const els=[...p.querySelectorAll('*')]; let f=1;
 for(let i=0;i<30;i++){ const sizes=els.map(e=>parseFloat(getComputedStyle(e).fontSize)); if(Math.max(...sizes)>=31) break; els.forEach((e,j)=>e.style.fontSize=(sizes[j]*1.04)+'px');
   if(need()>p.clientHeight-6||p.scrollWidth>p.clientWidth+2){ els.forEach((e,j)=>e.style.fontSize=sizes[j]+'px'); break; } } }'''
def page(d, lang, theme):
    c,a,bg,dd=THEMES[theme]; css=CSS.replace('VAR_BG',bg).replace('VAR_C',c).replace('VAR_A',a).replace('VAR_D',dd)
    fx=(lambda s: s.replace('İ','I').replace('ı','i')) if lang in ('zh','ja') else (lambda s: s)  # CJKFIX: CJK fonts break dotted capital I
    e=lambda s: html.escape(fx(s),quote=False)
    poster=not d.get('stats') and not d.get('pts')
    h=[f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body class="{"poster" if poster else ""}">','<div class="hd">']
    if d.get('k'): h.append(f'<div class="k">{e(d["k"])}</div>')
    h.append(f'<h1>{e(d["t"])}</h1>')
    if d.get('s'): h.append(f'<div class="s">{e(d["s"])}</div>')
    h.append('</div>')
    if d.get('stats'): h.append('<div class="stats">'+''.join(f'<div class="st"><b>{e(n)}</b><span>{e(l)}</span></div>' for n,l in d['stats'])+'</div>')
    if d.get('ph'): h.append(f'<div class="ph">{e(d["ph"])}</div>')
    if d.get('pts'): h.append('<div class="pts">'+''.join(f'<div class="pt"><b>{e(l)}</b>{" " if x else ""}{e(x)}</div>' for l,x in d['pts'])+'</div>')
    if d.get('msg'): h.append(f'<div class="msg">{e(d["msg"])}</div>')
    if d.get('src'): h.append(f'<div class="src">{e(d["src"])}</div>')
    h.append(f'<div class="foot"><span>klinikfarmakoloji.com</span><span>Prof. Dr. F. Cankat Tulunay</span></div></body></html>')
    return ''.join(h)
def main():
    mod=importlib.import_module(sys.argv[1]); os.makedirs(HERE+'/out',exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1080})
        for aid,(theme,langs) in mod.CARDS.items():
            for lang,d in langs.items():
                pg.set_content(page(d,lang,theme))
                if lang in FONT: pg.add_style_tag(content=FONT[lang])
                pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(120)
                left=pg.evaluate(FIT)
                pg.evaluate(GROW)
                pg.screenshot(path=f'{HERE}/out/{aid}.{lang}.png')
                if left: print(aid,lang,'OVERFLOW',left)
        b.close()
if __name__=='__main__': main()
