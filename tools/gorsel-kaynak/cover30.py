#!/usr/bin/env python3
"""1500x800 cover for the weight-loss injections news piece, Turkish + 7 languages -> out/b30_zayiflama_kapak.<lang>.png"""
import os, html
from playwright.sync_api import sync_playwright
from i18n import FONT
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f'{HERE}/out', exist_ok=True)
K = {
 'tr': ('HABER', 'CANAN KARATAY HASTALARI VE KAMUOYUNU YANILTIYOR', 'Zayıflama iğneleri: kalp, böbrek, karaciğer iddiaları ve klinik kanıt'),
 'en': ('NEWS', 'CANAN KARATAY IS MISLEADING PATIENTS AND THE PUBLIC', 'Weight-loss injections: heart, kidney and liver claims and clinical evidence'),
 'de': ('NACHRICHTEN', 'CANAN KARATAY FÜHRT PATIENTEN UND ÖFFENTLICHKEIT IN DIE IRRE', 'Abnehmspritzen: Behauptungen zu Herz, Niere, Leber und klinische Evidenz'),
 'es': ('NOTICIAS', 'CANAN KARATAY ENGAÑA A LOS PACIENTES Y A LA OPINIÓN PÚBLICA', 'Inyecciones para adelgazar: afirmaciones sobre corazón, riñón e hígado y evidencia clínica'),
 'ru': ('НОВОСТИ', 'КАНАН КАРАТАЙ ВВОДИТ В ЗАБЛУЖДЕНИЕ ПАЦИЕНТОВ И ОБЩЕСТВО', 'Уколы для похудения: утверждения о сердце, почках, печени и клинические данные'),
 'zh': ('新闻', 'CANAN KARATAY误导患者和公众', '减肥针：关于心脏、肾脏、肝脏的说法与临床证据'),
 'hi': ('समाचार', 'कनान करताय मरीज़ों और जनता को गुमराह कर रही हैं', 'वज़न घटाने के इंजेक्शन: हृदय, गुर्दा, यकृत के दावे और नैदानिक साक्ष्य'),
 'ja': ('ニュース', 'カナン・カラタイ氏は患者と世論を誤らせている', '痩せる注射：心臓・腎臓・肝臓をめぐる主張と臨床的根拠'),
}
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;height:800px;background:#7A1F2B;color:#fff;font-family:'DejaVu Sans',sans-serif;display:flex;flex-direction:column;overflow:hidden}
.m{flex:1;display:flex;align-items:center;padding:0 80px;gap:60px}
.tx{flex:1}.k{color:#E9C46A;font-weight:bold;letter-spacing:5px;font-size:40px;margin-bottom:24px}
h1{font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;font-size:62px;line-height:1.1}
.s{font-size:34px;margin-top:28px;opacity:.95;line-height:1.3}
.bar{height:10px;background:#E9C46A}
.f{height:64px;background:#2B1A1E;display:flex;align-items:center;justify-content:space-between;padding:0 80px;font-size:22px}
.f b{color:#E9C46A}svg{flex:none}'''
# an injection pen above a balance scale
SVG = '''<svg width="360" height="440" viewBox="0 0 360 440">
<g transform="rotate(-35 180 110)">
<rect x="40" y="88" width="230" height="44" rx="22" fill="#F7F0E3"/><rect x="150" y="96" width="70" height="28" rx="6" fill="#2A9D8F"/>
<rect x="270" y="96" width="34" height="28" rx="6" fill="#E9C46A"/><rect x="304" y="107" width="34" height="6" fill="#F7F0E3"/>
<rect x="14" y="94" width="28" height="32" rx="8" fill="#E9C46A"/></g>
<rect x="174" y="230" width="12" height="160" fill="#F7F0E3"/><rect x="110" y="388" width="140" height="18" rx="9" fill="#F7F0E3"/>
<rect x="60" y="228" width="240" height="10" rx="5" fill="#F7F0E3"/><circle cx="180" cy="228" r="14" fill="#E9C46A"/>
<path d="M70 238 L40 318 M70 238 L100 318" stroke="#F7F0E3" stroke-width="4"/><path d="M290 238 L260 318 M290 238 L320 318" stroke="#F7F0E3" stroke-width="4"/>
<path d="M30 318 H110 A40 26 0 0 1 30 318Z" fill="#2A9D8F"/><path d="M250 318 H330 A40 26 0 0 1 250 318Z" fill="#E76F51"/>
<text x="70" y="306" text-anchor="middle" font-size="40" font-weight="bold" fill="#F7F0E3" font-family="DejaVu Sans">+</text>
<text x="290" y="306" text-anchor="middle" font-size="40" font-weight="bold" fill="#F7F0E3" font-family="DejaVu Sans">−</text>
</svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 800})
    for lang, (k, t, s) in K.items():
        e = lambda x: html.escape(x, quote=False)
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="m"><div class="tx"><div class="k">{e(k)}</div><h1>{e(t)}</h1><div class="s">{e(s)}</div></div>{SVG}</div><div class="bar"></div><div class="f"><b>klinikfarmakoloji.com</b><span>Prof. Dr. F. Cankat Tulunay</span></div></body></html>')
        if lang in FONT: pg.add_style_tag(content=FONT[lang])
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
        if pg.evaluate("()=>{const t=document.querySelector('.tx');return t.scrollHeight>t.parentElement.clientHeight}"): print(lang, 'OVERFLOW')
        pg.screenshot(path=f'{HERE}/out/b30_zayiflama_kapak.{lang}.png')
