#!/usr/bin/env python3
"""1500x800 cover for the peptide therapy article, Turkish + 7 languages -> out/b29_peptit_kapak.<lang>.png"""
import os, html
from playwright.sync_api import sync_playwright
from i18n import FONT
HERE = os.path.dirname(os.path.abspath(__file__))
K = {
 'tr': ("ACI İLAÇ", "PEPTİT TEDAVİSİ: BİLİM Mİ, KANDIRMACA MI?", "Siyasi destek, klinik kanıtın yerini tutmaz"),
 'en': ("BITTER MEDICINE", "PEPTIDE THERAPY: SCIENCE OR DECEPTION?", "Political support is no substitute for clinical evidence"),
 'de': ("BITTERE MEDIZIN", "PEPTIDTHERAPIE: WISSENSCHAFT ODER TÄUSCHUNG?", "Politische Unterstützung ersetzt keine klinische Evidenz"),
 'es': ("MEDICINA AMARGA", "TERAPIA CON PÉPTIDOS: ¿CIENCIA O ENGAÑO?", "El apoyo político no sustituye a la evidencia clínica"),
 'ru': ("ГОРЬКОЕ ЛЕКАРСТВО", "ПЕПТИДНАЯ ТЕРАПИЯ: НАУКА ИЛИ ОБМАН?", "Политическая поддержка не заменяет клинических доказательств"),
 'zh': ("苦口良药", "肽疗法：科学还是骗局？", "政治支持不能取代临床证据"),
 'hi': ("कड़वी दवा", "पेप्टाइड थेरेपी: विज्ञान या छल?", "राजनीतिक समर्थन नैदानिक साक्ष्य की जगह नहीं ले सकता"),
 'ja': ("苦い薬", "ペプチド療法：科学か、ごまかしか？", "政治的支持は臨床的根拠の代わりにならない"),
}
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;height:800px;background:#7A1F2B;color:#fff;font-family:'DejaVu Sans',sans-serif;display:flex;flex-direction:column;overflow:hidden}
.m{flex:1;display:flex;align-items:center;padding:0 80px;gap:60px}
.tx{flex:1}.k{color:#E9C46A;font-weight:bold;letter-spacing:5px;font-size:40px;margin-bottom:24px}
h1{font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;font-size:70px;line-height:1.1}
.s{font-size:34px;margin-top:28px;opacity:.95;line-height:1.3}
.bar{height:10px;background:#E9C46A}
.f{height:64px;background:#2B1A1E;display:flex;align-items:center;justify-content:space-between;padding:0 80px;font-size:22px}
.f b{color:#E9C46A}svg{flex:none}'''
# a vial with a question mark, and a peptide chain
SVG = '''<svg width="360" height="420" viewBox="0 0 360 420">
<rect x="110" y="40" width="140" height="50" rx="8" fill="#E9C46A"/><rect x="125" y="90" width="110" height="26" fill="#F7F0E3"/>
<path d="M100 116h160v230a26 26 0 0 1-26 26H126a26 26 0 0 1-26-26z" fill="#F7F0E3"/>
<path d="M100 240h160v106a26 26 0 0 1-26 26H126a26 26 0 0 1-26-26z" fill="#2A9D8F"/>
<text x="180" y="225" text-anchor="middle" font-size="120" font-weight="bold" fill="#7A1F2B" font-family="DejaVu Sans">?</text>
<g fill="#E9C46A" stroke="#7A1F2B" stroke-width="4"><circle cx="40" cy="380" r="18"/><circle cx="80" cy="400" r="18"/><circle cx="300" cy="400" r="18"/><circle cx="340" cy="380" r="18"/></g>
</svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 800})
    for lang, (k, t, s) in K.items():
        e = lambda x: html.escape(x, quote=False)
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="m"><div class="tx"><div class="k">{e(k)}</div><h1>{e(t)}</h1><div class="s">{e(s)}</div></div>{SVG}</div><div class="bar"></div><div class="f"><b>klinikfarmakoloji.com</b><span>Prof. Dr. F. Cankat Tulunay</span></div></body></html>')
        if lang in FONT: pg.add_style_tag(content=FONT[lang])
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
        if pg.evaluate("()=>{const t=document.querySelector('.tx');return t.scrollHeight>t.parentElement.clientHeight}"): print(lang, 'OVERFLOW')
        pg.screenshot(path=f'{HERE}/out/b29_peptit_kapak.{lang}.png')
