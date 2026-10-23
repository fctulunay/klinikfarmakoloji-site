#!/usr/bin/env python3
"""Language versions of the author's 'Felçte Nalokson' poster (846x878): the artwork band is kept,
the title band (top) and the message panel (bottom) are re-set in each language.
-> out/b31_nalokson_kapak.<lang>.png"""
import os, html, base64
from playwright.sync_api import sync_playwright
from i18n import FONT
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '../../sites/default/files/yazi-gorselleri/cms/felcte-nalokson-kapak.png')
os.makedirs(f'{HERE}/out', exist_ok=True)
K = {
 'en': ('NALOXONE IN PARALYSIS', 'A forgotten story from San Francisco to Ankara', 'History is written with documents.', 'A clinical observation is not a proven treatment.', 'Naloxone is not a proven standard treatment in stroke.'),
 'de': ('NALOXON BEI LÄHMUNG', 'Eine vergessene Geschichte von San Francisco nach Ankara', 'Geschichte wird mit Dokumenten geschrieben.', 'Eine klinische Beobachtung ist keine bewiesene Therapie.', 'Naloxon ist beim Schlaganfall keine bewiesene Standardtherapie.'),
 'es': ('NALOXONA EN LA PARÁLISIS', 'Una historia olvidada de San Francisco a Ankara', 'La historia se escribe con documentos.', 'Una observación clínica no es un tratamiento probado.', 'La naloxona no es un tratamiento estándar probado en el ictus.'),
 'ru': ('НАЛОКСОН ПРИ ПАРАЛИЧЕ', 'Забытая история: от Сан-Франциско до Анкары', 'История пишется документами.', 'Клиническое наблюдение не есть доказанное лечение.', 'Налоксон не является доказанным стандартным лечением инсульта.'),
 'zh': ('纳洛酮与瘫痪', '从旧金山到安卡拉，一段被遗忘的历史', '历史要用文献来书写。', '临床观察不等于已证实的治疗。', '纳洛酮并非已证实的卒中标准治疗。'),
 'hi': ('लकवे में नालोक्सोन', 'सैन फ्रांसिस्को से अंकारा तक एक भूली हुई कहानी', 'इतिहास दस्तावेज़ों से लिखा जाता है।', 'नैदानिक अवलोकन सिद्ध उपचार नहीं है।', 'नालोक्सोन स्ट्रोक में सिद्ध मानक उपचार नहीं है।'),
 'ja': ('麻痺とナロキソン', 'サンフランシスコからアンカラへ、忘れられた物語', '歴史は記録によって書かれる。', '臨床観察は証明された治療ではない。', 'ナロキソンは脳卒中の証明された標準治療ではない。'),
}
B64 = base64.b64encode(open(SRC, 'rb').read()).decode()
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:846px;height:878px;position:relative;overflow:hidden;font-family:'DejaVu Serif',Georgia,serif}
.bg{position:absolute;inset:0;background:url(data:image/png;base64,B64) 0 0/846px 878px no-repeat}
.top{position:absolute;left:0;top:0;width:846px;height:222px;background:linear-gradient(#0d1a30,#14284a 88%,rgba(20,40,74,0));
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px 30px 18px}
.top h1{color:#e8c46a;font-size:50px;line-height:1.05;letter-spacing:1px;text-shadow:0 2px 4px rgba(0,0,0,.6)}
.top .s{color:#f4ecd8;font-size:24px;margin-top:10px;font-weight:bold}
.orn{width:300px;height:2px;background:#c9a24a;margin-top:12px}
.bot{position:absolute;left:58px;top:612px;width:730px;height:248px;background:#f1e6cf;
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:6px 26px;color:#14213a}
.bot h2{font-size:38px;line-height:1.1}
.bot .a{font-size:21px;margin-top:12px;font-weight:bold}
.bot .b{font-size:16px;margin-top:6px}
.bot .ln{width:330px;height:1px;background:#b48a3c;margin:12px 0 8px}
.bot .au{font-size:18px;font-weight:bold}.bot .w{font-size:12px;letter-spacing:2px;margin-top:2px}'''.replace('B64', B64)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 846, 'height': 878})
    for lang, (t, s, m, a, b) in K.items():
        e = lambda x: html.escape(x, quote=False)
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bg"></div>'
                       f'<div class="top"><h1>{e(t)}</h1><div class="s">{e(s)}</div><div class="orn"></div></div>'
                       f'<div class="bot"><h2>{e(m)}</h2><div class="a">{e(a)}</div><div class="b">{e(b)}</div><div class="ln"></div>'
                       f'<div class="au">Prof. Dr. F. Cankat Tulunay</div><div class="w">klinikfarmakoloji.com</div></div></body></html>')
        if lang in FONT: pg.add_style_tag(content=FONT[lang])
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        if lang not in ("zh", "ja"): pg.evaluate("()=>{for(const [sel,q] of [['.top h1',''],['.top .s',''],['.bot h2',''],['.bot .a','']]){const el=document.querySelector(sel);let f=parseFloat(getComputedStyle(el).fontSize);const lh=parseFloat(getComputedStyle(el).lineHeight)||f*1.2;while(el.getBoundingClientRect().height>f*1.35&&f>12){f-=1;el.style.fontSize=f+'px'}}}")
        for sel in ('.top', '.bot'):
            if pg.evaluate(f"()=>{{const t=document.querySelector('{sel}');return t.scrollHeight>t.clientHeight+1||t.scrollWidth>t.clientWidth+1}}"): print(lang, sel, 'OVERFLOW')
        pg.screenshot(path=f'{HERE}/out/b31_nalokson_kapak.{lang}.png')
    br.close()
print('done')
