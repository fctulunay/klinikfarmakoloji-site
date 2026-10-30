#!/usr/bin/env python3
"""Language versions of the 'Kadınlarda Obezite' infographic (supplied by the author, 836x843 after
trimming the screenshot edges) and a 1500x800 cover built from its artwork.
The artwork is kept; every text area is softly covered and re-set in each language.
-> out/kadin_obezite_info.<lang>.png, out/kadin_obezite_kapak.<lang>.png (lang incl. tr for the cover)"""
import os, html, base64, io
from PIL import Image
from playwright.sync_api import sync_playwright
from i18n import FONT
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '../../sites/default/files/yazi-gorselleri/cms/kadinlarda-obezite-infografik.png')
os.makedirs(f'{HERE}/out', exist_ok=True)
im = Image.open(SRC).convert('RGB'); W, H = im.size
buf = io.BytesIO(); im.save(buf, 'PNG'); B64 = base64.b64encode(buf.getvalue()).decode()

# (title segments [(text, yellow?)], subtitle a, subtitle b,
#  [(head, text)] x4, sex head, sex text, pill, glp text, glp right, src label, src note)
T = {
 'tr': ([('KADINLARDA ', 0), ('OBEZİTE', 1)], 'Ergenlikten menopoza: ', 'hormonlar, metabolizma ve cinsel sağlık',
        [('ERGENLİK', 'Artan yağlanma, daha erken ergenlik ve ilk adetle ilişkilidir.'),
         ('ÜREME VE GEBELİK', 'Yumurtlama sorunları, gebelik diyabeti ve preeklampsi riski artabilir.'),
         ('DOĞUM SONRASI', 'Uyku kaybı, stres ve bakım yükü kilo yönetimini zorlaştırabilir.'),
         ('MENOPOZ', 'Karın içi yağlanma artabilir; kas kütlesini korumak önemlidir.')],
        'CİNSEL SAĞLIK DA ETKİLENEBİLİR', 'İstek, uyarılma ve cinsel doyum; diyabet, uyku, ruh sağlığı ve beden algısıyla birlikte etkilenebilir.',
        'Her kadında cinsel işlev bozukluğu gelişmez.', 'Hızlı çözüm değil, uzun vadeli tedavi planı.', 'Gebelikte kilo verme amacıyla kullanılmaz.',
        'Kaynak:', 'Cinsel sağlık bölümü ek bilimsel literatüre dayanmaktadır.'),
 'en': ([('OBESITY', 1), (' IN WOMEN', 0)], 'From puberty to menopause: ', 'hormones, metabolism and sexual health',
        [('PUBERTY', 'Increased body fat is linked to earlier puberty and an earlier first period.'),
         ('REPRODUCTION AND PREGNANCY', 'Ovulation problems and the risk of gestational diabetes and preeclampsia may increase.'),
         ('AFTER CHILDBIRTH', 'Sleep loss, stress and the burden of care can make weight management harder.'),
         ('MENOPAUSE', 'Visceral (abdominal) fat may increase; preserving muscle mass is important.')],
        'SEXUAL HEALTH CAN BE AFFECTED TOO', 'Desire, arousal and sexual satisfaction may be affected, together with diabetes, sleep, mental health and body image.',
        'Not every woman develops sexual dysfunction.', 'Not a quick fix, a long-term treatment plan.', 'Not used for weight loss during pregnancy.',
        'Sources:', 'The sexual health section draws on additional scientific literature.'),
 'de': ([('ADIPOSITAS', 1), (' BEI FRAUEN', 0)], 'Von der Pubertät bis zur Menopause: ', 'Hormone, Stoffwechsel und sexuelle Gesundheit',
        [('PUBERTÄT', 'Mehr Körperfett ist mit früherer Pubertät und früherer erster Regelblutung verbunden.'),
         ('FORTPFLANZUNG UND SCHWANGERSCHAFT', 'Eisprungstörungen sowie das Risiko für Schwangerschaftsdiabetes und Präeklampsie können zunehmen.'),
         ('NACH DER GEBURT', 'Schlafmangel, Stress und Betreuungslast können das Gewichtsmanagement erschweren.'),
         ('MENOPAUSE', 'Das Bauchinnenfett kann zunehmen; der Erhalt der Muskelmasse ist wichtig.')],
        'AUCH DIE SEXUELLE GESUNDHEIT KANN LEIDEN', 'Lust, Erregung und sexuelle Zufriedenheit können zusammen mit Diabetes, Schlaf, psychischer Gesundheit und Körperbild beeinträchtigt sein.',
        'Nicht jede Frau entwickelt eine sexuelle Funktionsstörung.', 'Keine schnelle Lösung, sondern ein langfristiger Therapieplan.', 'In der Schwangerschaft nicht zur Gewichtsabnahme angewendet.',
        'Quellen:', 'Der Abschnitt zur sexuellen Gesundheit stützt sich auf weitere wissenschaftliche Literatur.'),
 'es': ([('OBESIDAD', 1), (' EN LA MUJER', 0)], 'De la pubertad a la menopausia: ', 'hormonas, metabolismo y salud sexual',
        [('PUBERTAD', 'El aumento de grasa corporal se asocia con una pubertad y una primera menstruación más tempranas.'),
         ('REPRODUCCIÓN Y EMBARAZO', 'Pueden aumentar los problemas de ovulación y el riesgo de diabetes gestacional y preeclampsia.'),
         ('POSPARTO', 'La falta de sueño, el estrés y la carga de cuidados pueden dificultar el control del peso.'),
         ('MENOPAUSIA', 'Puede aumentar la grasa visceral; es importante conservar la masa muscular.')],
        'LA SALUD SEXUAL TAMBIÉN PUEDE VERSE AFECTADA', 'El deseo, la excitación y la satisfacción sexual pueden afectarse junto con la diabetes, el sueño, la salud mental y la imagen corporal.',
        'No todas las mujeres desarrollan disfunción sexual.', 'No es una solución rápida, sino un plan de tratamiento a largo plazo.', 'No se usa para adelgazar durante el embarazo.',
        'Fuentes:', 'La sección de salud sexual se basa en literatura científica adicional.'),
 'ru': ([('ОЖИРЕНИЕ', 1), (' У ЖЕНЩИН', 0)], 'От полового созревания до менопаузы: ', 'гормоны, обмен веществ и сексуальное здоровье',
        [('ПОЛОВОЕ СОЗРЕВАНИЕ', 'Избыток жира связан с более ранним половым созреванием и первой менструацией.'),
         ('РЕПРОДУКЦИЯ И БЕРЕМЕННОСТЬ', 'Могут возрасти нарушения овуляции и риск гестационного диабета и преэклампсии.'),
         ('ПОСЛЕ РОДОВ', 'Недосып, стресс и нагрузка по уходу могут затруднять контроль веса.'),
         ('МЕНОПАУЗА', 'Может увеличиться висцеральный жир; важно сохранять мышечную массу.')],
        'СТРАДАЕТ И СЕКСУАЛЬНОЕ ЗДОРОВЬЕ', 'Влечение, возбуждение и сексуальное удовлетворение могут нарушаться вместе с диабетом, сном, психическим здоровьем и образом тела.',
        'Сексуальная дисфункция развивается не у каждой женщины.', 'Не быстрое решение, а долгосрочный план лечения.', 'Не применяется для снижения веса при беременности.',
        'Источники:', 'Раздел о сексуальном здоровье основан на дополнительной научной литературе.'),
 'zh': ([('女性', 0), ('肥胖', 1)], '从青春期到更年期：', '激素、代谢与性健康',
        [('青春期', '体脂增加与青春期提前和初潮提前有关。'),
         ('生育与妊娠', '排卵问题以及妊娠糖尿病和子痫前期风险可能增加。'),
         ('产后', '睡眠不足、压力和照护负担会使体重管理更加困难。'),
         ('更年期', '内脏脂肪可能增加；保持肌肉量很重要。')],
        '性健康也可能受到影响', '性欲、性唤起和性满足可能与糖尿病、睡眠、心理健康和身体意象一同受到影响。',
        '并非每位女性都会出现性功能障碍。', '不是速效方案，而是长期治疗计划。', '妊娠期不用于减重。',
        '来源：', '性健康部分参考了其他科学文献。'),
 'hi': ([('महिलाओं में ', 0), ('मोटापा', 1)], 'किशोरावस्था से रजोनिवृत्ति तक: ', 'हार्मोन, चयापचय और यौन स्वास्थ्य',
        [('किशोरावस्था', 'बढ़ी हुई चर्बी जल्दी यौवन और जल्दी पहले मासिक धर्म से जुड़ी है।'),
         ('प्रजनन और गर्भावस्था', 'ओव्यूलेशन की समस्याएँ, गर्भावधि मधुमेह और प्रीएक्लेम्पसिया का जोखिम बढ़ सकता है।'),
         ('प्रसव के बाद', 'नींद की कमी, तनाव और देखभाल का बोझ वज़न प्रबंधन को कठिन बना सकते हैं।'),
         ('रजोनिवृत्ति', 'पेट के अंदर की चर्बी बढ़ सकती है; मांसपेशियों को बनाए रखना ज़रूरी है।')],
        'यौन स्वास्थ्य भी प्रभावित हो सकता है', 'इच्छा, उत्तेजना और यौन संतुष्टि मधुमेह, नींद, मानसिक स्वास्थ्य और शारीरिक छवि के साथ प्रभावित हो सकती हैं।',
        'हर महिला में यौन क्रिया विकार नहीं होता।', 'त्वरित समाधान नहीं, दीर्घकालिक उपचार योजना।', 'गर्भावस्था में वज़न घटाने के लिए उपयोग नहीं किया जाता।',
        'स्रोत:', 'यौन स्वास्थ्य खंड अतिरिक्त वैज्ञानिक साहित्य पर आधारित है।'),
 'ja': ([('女性の', 0), ('肥満', 1)], '思春期から更年期まで：', 'ホルモン、代謝、性の健康',
        [('思春期', '体脂肪の増加は、思春期と初経の早まりに関連する。'),
         ('生殖と妊娠', '排卵障害、妊娠糖尿病、妊娠高血圧腎症のリスクが高まりうる。'),
         ('産後', '睡眠不足、ストレス、育児の負担が体重管理を難しくしうる。'),
         ('更年期', '内臓脂肪が増えうる。筋肉量の維持が大切。')],
        '性の健康も影響を受けうる', '性欲、性的興奮、性的満足は、糖尿病、睡眠、心の健康、ボディイメージとともに影響を受けうる。',
        'すべての女性に性機能障害が起こるわけではない。', '即効策ではなく、長期的な治療計画。', '妊娠中に減量目的では使用しない。',
        '出典：', '性の健康の項は追加の科学文献に基づく。'),
}
SRCS = 'Healio, 29.10.2026; ASRM 2021; Greendale 2019; Wilding 2022.'

PANEL = '17,44,84'; STRIP = '27,66,114'; HEAD = '11,35,66'
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:%dpx;height:%dpx;position:relative;overflow:hidden;font-family:Inter,'DejaVu Sans',sans-serif;color:#fff}
.bg{position:absolute;inset:0;background:url(data:image/png;base64,%s) 0 0/%dpx %dpx no-repeat}
.c{position:absolute;display:flex;padding:0 4px;flex-direction:column;justify-content:center;overflow:hidden;border-radius:10px;
   backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
.y{color:#f5dd4f}.w{color:#fff}.lb{color:#8fe0ea}
.h{font-weight:900;color:#f5dd4f;line-height:1.05;letter-spacing:.2px}
.t{font-weight:600;line-height:1.22;margin-top:8px}
#title h1{font-weight:900;font-size:66px;line-height:1;letter-spacing:-1px}
#title .s{font-weight:700;font-size:23px;margin-top:10px;line-height:1.2}
.pill{border:2px solid #63c6d3;border-radius:22px;padding:6px 16px;color:#8fe0ea;font-weight:700;font-size:20px;margin-top:10px;display:flex;gap:10px;align-items:center}
.glp{font-weight:800;font-size:27px;line-height:1.1}
.src{font-size:12.5px;line-height:1.35;color:#d9dde6}
'''

def box(id_, x, y, w, h, rgb, inner, a=.93, extra=''):
    y -= 10  # coordinates measured on the untrimmed screenshot
    return (f'<div class="c" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:rgba({rgb},{a});{extra}">{inner}</div>')

FIT = r'''()=>{ const out=[];
 for(const b of document.querySelectorAll('.c')){ let i=0;
   const bad=()=>b.scrollHeight>b.clientHeight+1||[...b.querySelectorAll('*')].some(e=>e.scrollWidth>b.clientWidth-4);
   while(bad()&&i<60){
     b.querySelectorAll('*').forEach(e=>{const f=parseFloat(getComputedStyle(e).fontSize); e.style.fontSize=(f*0.96)+'px';}); i++; }
   if(bad()) out.push(b.id); }
 return out; }'''

def info_html(lang):
    tt, sa, sb, panels, sh, st, pill, glp, glpr, sl, sn = T[lang]
    e = lambda s: html.escape(s, quote=False)
    h1 = ''.join(f'<span class="{"y" if y else "w"}">{e(s)}</span>' for s, y in tt)
    parts = [box('title', 22, 22, 636, 120, HEAD, f'<h1>{h1}</h1><div class="s"><span class="w">{e(sa)}</span><span class="lb">{e(sb)}</span></div>', .96)]
    pos = [(198, 168, 214, 166), (592, 168, 232, 166), (200, 360, 212, 170), (612, 360, 212, 170)]
    for i, ((hd, tx), (x, y, w, hh)) in enumerate(zip(panels, pos)):
        parts.append(box(f'p{i}', x, y, w, hh, PANEL, f'<div class="h" style="font-size:30px">{e(hd)}</div><div class="t" style="font-size:20px">{e(tx)}</div>'))
    parts.append(box('sex', 240, 556, 588, 156, PANEL,
                     f'<div class="h" style="font-size:34px">{e(sh)}</div><div class="t" style="font-size:19px">{e(st)}</div>'
                     f'<div class="pill"><span>💡</span><span>{e(pill)}</span></div>'))
    parts.append(box('glp', 88, 727, 516, 60, STRIP, f'<div class="glp"><span class="y">GLP-1: </span><span class="w">{e(glp)}</span></div>'))
    parts.append(box('glpr', 668, 726, 164, 62, STRIP, f'<div style="font-weight:700;font-size:15px;line-height:1.2">{e(glpr)}</div>'))
    parts.append(box('srcb', 18, 793, 560, 46, HEAD, f'<div class="src"><b>{e(sl)}</b> {SRCS}<br>{e(sn)}</div>', .97))
    css = CSS % (W, H, B64, W, H)
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="bg"></div>{"".join(parts)}</body></html>'

# ---- cover: 1500x800, title left, four artwork crops right
CROPS = [(14, 147, 196, 332), (428, 147, 588, 332), (14, 344, 200, 527), (428, 344, 620, 527)]
def crop64(b):
    c = im.crop(b); bb = io.BytesIO(); c.save(bb, 'PNG'); return base64.b64encode(bb.getvalue()).decode()
CROP64 = [crop64(b) for b in CROPS]
CCSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;height:800px;overflow:hidden;background:radial-gradient(circle at 25% 30%,#173a6b,#0b2342 70%);font-family:Inter,'DejaVu Sans',sans-serif;color:#fff;display:flex}
.l{width:760px;padding:70px 40px 60px 70px;display:flex;flex-direction:column;justify-content:center}
.l h1{white-space:nowrap;overflow:hidden;font-weight:900;font-size:110px;line-height:.98;letter-spacing:-2px}
.l .s{font-weight:700;font-size:36px;line-height:1.25;margin-top:26px}
.l .ln{height:4px;width:420px;background:#f5dd4f;margin-top:30px;border-radius:2px}
.l .site{margin-top:22px;font-size:24px;color:#cfd6e3;font-weight:600}
.y{color:#f5dd4f}.lb{color:#8fe0ea}
.r{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:50px 60px 50px 10px}
.r div{border-radius:18px;background-size:cover;background-position:center top;box-shadow:0 6px 18px rgba(0,0,0,.35);position:relative;overflow:hidden}
.r span{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;background:linear-gradient(transparent,rgba(8,26,52,.92) 45%);font-weight:900;color:#f5dd4f;font-size:24px;line-height:1.05}
'''
def cover_html(lang):
    tt, sa, sb, panels = T[lang][:4]
    e = lambda s: html.escape(s, quote=False)
    h1 = ''.join(f'<span class="{"y" if y else ""}">{e(s.strip())}</span><br>' for s, y in tt)
    tiles = ''.join(f'<div style="background-image:url(data:image/png;base64,{c})"><span>{e(p[0])}</span></div>' for c, p in zip(CROP64, panels))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CCSS}</style></head><body>'
            f'<div class="l" id="cl"><h1>{h1}</h1><div class="s">{e(sa)}<span class="lb">{e(sb)}</span></div><div class="ln"></div>'
            f'<div class="site">klinikfarmakoloji.com</div></div><div class="r">{tiles}</div></body></html>')
CFIT = r'''()=>{const b=document.getElementById('cl');let i=0;const h=b.querySelector('h1');while((b.scrollHeight>b.clientHeight+1||h.scrollWidth>h.clientWidth+1)&&i<60){b.querySelectorAll('h1,.s').forEach(e=>{const f=parseFloat(getComputedStyle(e).fontSize);e.style.fontSize=(f*0.96)+'px'});i++;}
 document.querySelectorAll('.r span').forEach(s=>{let j=0;while(s.scrollWidth>s.clientWidth+1&&j<30){const f=parseFloat(getComputedStyle(s).fontSize);s.style.fontSize=(f*0.95)+'px';j++;}});
 return b.scrollHeight>b.clientHeight+1;}'''

def fx(lang, s):  # CJK fonts break dotted capital I
    return s.replace('İ', 'I').replace('ı', 'i') if lang in ('zh', 'ja') else s

with sync_playwright() as p:
    br = p.chromium.launch()
    for lang in T:
        if lang != 'tr':
            pg = br.new_page(viewport={'width': W, 'height': H})
            pg.set_content(fx(lang, info_html(lang)))
            if lang in FONT: pg.add_style_tag(content=FONT[lang])
            pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
            left = pg.evaluate(FIT)
            if left: print(lang, 'info OVERFLOW', left)
            pg.screenshot(path=f'{HERE}/out/kadin_obezite_info.{lang}.png'); pg.close()
        pg = br.new_page(viewport={'width': 1500, 'height': 800})
        pg.set_content(cover_html(lang))
        if lang in FONT: pg.add_style_tag(content=FONT[lang])
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        if pg.evaluate(CFIT): print(lang, 'cover OVERFLOW')
        pg.screenshot(path=f'{HERE}/out/kadin_obezite_kapak.{lang}.png'); pg.close()
    br.close()
print('done')
