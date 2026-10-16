#!/usr/bin/env python3
"""1200x640 cover for the Vykat XR news piece, Turkish + 7 languages -> out/b28_vykat_kapak.<lang>.png"""
import os, html
from PIL import Image
from playwright.sync_api import sync_playwright
from i18n import FONT
from batch28 import K
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
# a balance: evidence on one pan, a stack of coins on the heavier pan
SVG = '''<svg width="380" height="420" viewBox="0 0 380 420">
<rect x="180" y="60" width="20" height="300" fill="#F7F0E3"/><rect x="110" y="360" width="160" height="26" rx="6" fill="#F7F0E3"/>
<circle cx="190" cy="56" r="16" fill="#E9C46A"/>
<line x1="40" y1="110" x2="340" y2="150" stroke="#F7F0E3" stroke-width="12" stroke-linecap="round"/>
<g stroke="#F7F0E3" stroke-width="4"><line x1="50" y1="112" x2="20" y2="210"/><line x1="50" y1="112" x2="110" y2="210"/><line x1="330" y1="148" x2="300" y2="250"/><line x1="330" y1="148" x2="360" y2="250"/></g>
<path d="M10 210H120C116 236 92 246 65 246S14 236 10 210Z" fill="#F7F0E3"/>
<path d="M290 250H370C366 274 348 282 330 282S294 274 290 250Z" fill="#E9C46A"/>
<rect x="38" y="168" width="54" height="42" rx="3" fill="#2A9D8F"/><g stroke="#F7F0E3" stroke-width="3"><line x1="46" y1="180" x2="84" y2="180"/><line x1="46" y1="190" x2="84" y2="190"/><line x1="46" y1="200" x2="72" y2="200"/></g>
<g fill="#E9C46A" stroke="#7A1F2B" stroke-width="3"><ellipse cx="330" cy="244" rx="32" ry="9"/><ellipse cx="330" cy="232" rx="32" ry="9"/><ellipse cx="330" cy="220" rx="32" ry="9"/><ellipse cx="330" cy="208" rx="32" ry="9"/><ellipse cx="330" cy="196" rx="32" ry="9"/></g>
<text x="330" y="202" text-anchor="middle" font-size="18" font-weight="bold" fill="#7A1F2B" font-family="DejaVu Sans">$</text>
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
        f = f'{HERE}/out/b28_vykat_kapak.{lang}.png'; pg.screenshot(path=f)
        Image.open(f).resize((1200, 640), Image.LANCZOS).save(f)
    b.close()
