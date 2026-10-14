#!/usr/bin/env python3
"""1200x640 cover for the FDA advisory committee news piece, Turkish + 7 languages -> out/b27_fda_kapak.<lang>.png"""
import os, html
from PIL import Image
from playwright.sync_api import sync_playwright
from i18n import FONT
from batch27 import K
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;height:800px;background:#7A1F2B;color:#fff;font-family:'DejaVu Sans',sans-serif;display:flex;flex-direction:column;overflow:hidden}
.m{flex:1;display:flex;align-items:center;padding:0 80px;gap:60px}
.tx{flex:1}.k{color:#E9C46A;font-weight:bold;letter-spacing:5px;font-size:40px;margin-bottom:24px}
h1{font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;font-size:70px;line-height:1.1}
.s{font-size:34px;margin-top:28px;opacity:.95;line-height:1.3}
.bar{height:10px;background:#E9C46A}
.f{height:64px;background:#2B1A1E;display:flex;align-items:center;justify-content:space-between;padding:0 80px;font-size:22px}
.f b{color:#E9C46A}svg{flex:none}'''
# a building ($) feeding coins to a seat at the committee table
SVG = '''<svg width="380" height="420" viewBox="0 0 380 420">
<rect x="20" y="40" width="130" height="190" rx="6" fill="#F7F0E3"/>
<g fill="#7A1F2B"><rect x="40" y="65" width="28" height="28"/><rect x="102" y="65" width="28" height="28"/><rect x="40" y="115" width="28" height="28"/><rect x="102" y="115" width="28" height="28"/><rect x="70" y="175" width="30" height="55"/></g>
<path d="M150 120C230 110 270 150 280 215" fill="none" stroke="#E9C46A" stroke-width="12" stroke-linecap="round" stroke-dasharray="2 26"/>
<circle cx="250" cy="70" r="40" fill="#E9C46A"/><text x="250" y="86" text-anchor="middle" font-size="46" font-weight="bold" fill="#7A1F2B" font-family="DejaVu Sans">$</text>
<rect x="30" y="300" width="330" height="22" rx="6" fill="#E9C46A"/>
<g fill="#F7F0E3"><circle cx="110" cy="262" r="22"/><path d="M80 300C80 278 140 278 140 300Z"/><circle cx="195" cy="262" r="22"/><path d="M165 300C165 278 225 278 225 300Z"/></g>
<circle cx="280" cy="258" r="24" fill="#2A9D8F"/><path d="M248 300C248 274 312 274 312 300Z" fill="#2A9D8F"/>
<g stroke="#F7F0E3" stroke-width="10" stroke-linecap="round"><line x1="60" y1="322" x2="60" y2="400"/><line x1="330" y1="322" x2="330" y2="400"/></g>
</svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 800})
    for lang, (k, t, s) in K.items():
        fx = (lambda x: x.replace('İ', 'I').replace('ı', 'i')) if lang in ('zh', 'ja') else (lambda x: x)
        e = lambda x: html.escape(fx(x), quote=False)
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="m"><div class="tx"><div class="k">{e(k)}</div><h1>{e(t)}</h1><div class="s">{e(s)}</div></div>{SVG}</div><div class="bar"></div><div class="f"><b>klinikfarmakoloji.com</b><span>Prof. Dr. F. Cankat Tulunay</span></div></body></html>')
        if lang in FONT: pg.add_style_tag(content=FONT[lang])
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
        over = pg.evaluate("()=>{const t=document.querySelector('.tx');return t.scrollHeight>t.parentElement.clientHeight}")
        if over: print(lang, 'OVERFLOW')
        f = f'{HERE}/out/b27_fda_kapak.{lang}.png'; pg.screenshot(path=f)
        Image.open(f).resize((1200, 640), Image.LANCZOS).save(f)
    b.close()
