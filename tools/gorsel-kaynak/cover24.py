#!/usr/bin/env python3
"""1500x800 cover for the longevity article in Turkish + 7 languages -> out/b24_longevity_kapak.<lang>.png (tr = no suffix)."""
import os, html
from playwright.sync_api import sync_playwright
from i18n import FONT
from batch24 import T
HERE = os.path.dirname(os.path.abspath(__file__))
T = dict(T); T['tr'] = ("YENİ ALDATMACA", "Longevity klinikleri ve longevity koçluğu", "Ölçmek, yaşamı uzatmak değildir")
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;height:800px;background:#7A1F2B;color:#fff;font-family:'DejaVu Sans',sans-serif;display:flex;flex-direction:column;overflow:hidden}
.m{flex:1;display:flex;align-items:center;padding:0 80px;gap:60px}
.tx{flex:1}.k{color:#E9C46A;font-weight:bold;letter-spacing:5px;font-size:44px;margin-bottom:26px}
h1{font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;font-size:76px;line-height:1.1}
.s{font-size:34px;margin-top:28px;opacity:.95;line-height:1.3}
.bar{height:10px;background:#E9C46A}
.f{height:64px;background:#2B1A1E;display:flex;align-items:center;justify-content:space-between;padding:0 80px;font-size:22px}
.f b{color:#E9C46A}svg{flex:none}'''
SVG = '''<svg width="300" height="420" viewBox="0 0 300 420"><g fill="none" stroke="#E9C46A" stroke-width="12" stroke-linecap="round" stroke-linejoin="round">
<path d="M40 30H260M40 390H260"/><path d="M65 30C65 150 150 170 150 210C150 250 65 270 65 390M235 30C235 150 150 170 150 210C150 250 235 270 235 390"/></g>
<path d="M95 95H205C195 140 160 160 150 185C140 160 105 140 95 95Z" fill="#F7F0E3"/><path d="M150 205V300" stroke="#F7F0E3" stroke-width="5" stroke-dasharray="4 12"/>
<g fill="#E9C46A" stroke="#7A1F2B" stroke-width="4"><ellipse cx="150" cy="368" rx="62" ry="13"/><ellipse cx="150" cy="350" rx="62" ry="13"/><ellipse cx="150" cy="332" rx="62" ry="13"/><ellipse cx="150" cy="314" rx="62" ry="13"/></g>
<text x="150" y="321" text-anchor="middle" font-size="20" font-weight="bold" fill="#7A1F2B" font-family="DejaVu Sans">$</text></svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 800})
    for lang, (k, t, s) in T.items():
        fx = (lambda x: x.replace('İ', 'I').replace('ı', 'i')) if lang in ('zh', 'ja') else (lambda x: x)
        e = lambda x: html.escape(fx(x), quote=False)
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="m"><div class="tx"><div class="k">{e(k)}</div><h1>{e(t)}</h1><div class="s">{e(s)}</div></div>{SVG}</div><div class="bar"></div><div class="f"><b>klinikfarmakoloji.com</b><span>Prof. Dr. F. Cankat Tulunay</span></div></body></html>')
        if lang in FONT: pg.add_style_tag(content=FONT[lang])
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(120)
        over = pg.evaluate("()=>document.querySelector('.m').scrollHeight>document.querySelector('.m').clientHeight+2")
        pg.screenshot(path=f'{HERE}/out/b24_longevity_kapak.{lang}.png')
        if over: print('OVERFLOW', lang)
    b.close()
