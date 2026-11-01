#!/usr/bin/env python3
"""Bilingual (TR/EN) infographic 1080x1350 and cover 1500x800 for
'TIBBİ ARAŞTIRMALARDA ÇOCUKLAR',
in the same style as part (1). Output goes straight to sites/default/files/yazi-gorselleri/cms/."""
import os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '../../sites/default/files/yazi-gorselleri/cms/')

ICON = {
 'child': '<circle cx="12" cy="6" r="3"/><path d="M8 21v-6l-2-3 3-2h6l3 2-2 3v6"/><path d="M12 12v9"/>',
 'warn': '<path d="M12 3 2 20h20Z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6"/>',
 'pill': '<rect x="3" y="9" width="18" height="6" rx="3" transform="rotate(-35 12 12)"/><path d="m9.5 8.5 5 7"/>',
 'scale': '<path d="M12 3v18M5 21h14M4 7h16"/><path d="m4 7-3 6a3 3 0 0 0 6 0Z"/><path d="m20 7-3 6a3 3 0 0 0 6 0Z"/>',
 'flag': '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
}
def ic(name, col):
    return (f'<span class="ic" style="background:{col}"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg></span>')

def panel(col, icon, tr, en, inner):
    return (f'<div class="p" style="border-color:{col}"><div class="ph">{ic(icon, col)}<div>'
            f'<div class="pt" style="color:{col}">{tr}</div><div class="pe" style="color:{col}">{en}</div></div></div>{inner}</div>')

def li(b, t, e):
    return f'<li><b>{b}</b> {t}<span class="en">{e}</span></li>'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#f5ede1;font-family:'DejaVu Serif',Georgia,serif;color:#2a1a14}
.top{background:#5e1320;color:#fbf3e6;padding:30px 40px 24px}
.top h1{font-size:44px;white-space:nowrap;line-height:1.08;letter-spacing:.5px}
.top h1 em{font-style:normal;color:#e6c27c}
.top .sub{font-style:italic;font-weight:bold;color:#e6c27c;font-size:24px;margin-top:10px}
.top .s2{font-size:17px;margin-top:8px;color:#f1e3cf}.top .s2 i{color:#e6c27c}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:15px;padding:16px 26px 0}
.p{background:#fcf7ee;border:2px solid;border-radius:10px;padding:14px 14px 12px;height:505px;overflow:hidden}
.ph{display:flex;gap:10px;align-items:center;margin-bottom:10px}
.ic{flex:none;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.ic svg{width:25px;height:25px}
.pt{font-weight:bold;font-size:20px;line-height:1.1}.pe{font-style:italic;font-weight:bold;font-size:14px;opacity:.85;margin-top:2px}
ul{list-style:none}li{font-size:15.5px;line-height:1.28;margin-bottom:7px;padding-left:12px;position:relative}
li:before{content:'';position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;background:#8a7a70}
.en{display:block;font-style:italic;color:#6d5d55;font-size:13px;line-height:1.25;margin-top:1px}
p.t{font-size:15.5px;line-height:1.3;margin-bottom:6px}
.num{display:flex;gap:8px;align-items:baseline;margin-bottom:5px}
.num b{flex:none;width:132px;text-align:right;font-size:22px;white-space:nowrap;color:#3d4a7a}
.num div{font-size:14px;line-height:1.2}
.steps{display:flex;flex-direction:column;gap:6px;margin:4px 0 8px}
.yr{border-radius:7px;padding:7px 10px;font-size:14.5px;line-height:1.25;color:#fff}
.yr b{font-size:17px}
.tag{display:inline-block;background:#2f5d50;color:#fff;border-radius:5px;padding:4px 8px;font-size:13px;font-weight:bold;margin:2px 2px 2px 0}
.q{margin:18px 26px 0;background:#2b1a14;border-left:8px solid #c9a35a;border-radius:9px;padding:15px 20px;text-align:center}
.q .a{color:#fbf3e6;font-style:italic;font-size:22px}.q .b{color:#d9b876;font-style:italic;font-size:16px;margin-top:4px}
.foot{text-align:center;color:#5e1320;font-weight:bold;letter-spacing:3px;font-size:19px;margin-top:15px}
"""

R, O, G, B, Y, N = '#7a1f2b', '#b4621f', '#2f5d50', '#3d4a7a', '#8a6d2a', '#5e1320'
p1 = panel(R, 'child', 'Küçük yetişkin değil', 'Not a small adult', '<ul>' +
    li('Onam veremez:', 'kararı anne baba ya da vasi verir.', 'Cannot consent: parents or guardians decide.') +
    li('Olgunlaşmamış', 'karaciğer enzimleri, sınırlı böbrek fonksiyonu.', 'Immature liver enzymes, limited kidney function.') +
    li('Farklı', 'vücut suyu ve yağ oranı; daha geçirgen kan beyin bariyeri.', 'Different body water and fat; a more permeable blood-brain barrier.') +
    li('Aynı mg/kg doz,', 'bambaşka kan düzeyi ve etki.', 'Same mg/kg dose, very different levels and effects.') + '</ul>')
p2 = panel(O, 'warn', '1. tehlike: Denek yapmak', 'Danger 1: used as subjects', '<ul>' +
    li('Monster Study, 1939:', 'yetimhanede 22 çocuk.', 'Iowa: 22 orphans, no consent.') +
    li('Fernald, 1940-50\'ler:', 'radyoaktif yulaf lapası.', 'Radioactive oatmeal for a "Science Club".') +
    li('Willowbrook, 1956-71:', 'kasıtlı hepatit; kuruma girişin bedeli.', 'Deliberate hepatitis as the price of admission.') +
    li('Kennedy Krieger, 1993-95:', 'çocuğun kanı, temizliğin ölçüsü.', 'Children\'s blood lead as the yardstick.') +
    li('Kano, 1996:', 'onaysız ilaç, sahte etik kurul belgesi.', 'Unapproved drug, forged ethics approval.') + '</ul>')
p3 = panel(G, 'pill', '2. tehlike: Dışlamak', 'Danger 2: exclusion', '<p class="t">Shirkey, 1968: <b>"terapötik yetimler"</b><span class="en">"Therapeutic orphans": drugs never tested in children.</span></p><ul>' +
    li('1937:', 'Elixir Sulfanilamide; yüzü aşkın ölüm.', 'Elixir Sulfanilamide: over 100 deaths.') +
    li('1956:', 'prematürelerde sülfonamid, kernikterus.', 'Sulfonamide in preterm infants: kernicterus.') +
    li('1959:', 'kloramfenikol, "gri bebek".', 'Chloramphenicol: "grey baby" syndrome.') +
    '</ul><p class="t" style="margin-top:6px"><i>Araştırma yapılmadığı için öldüler.</i><span class="en">They died because the research was not done.</span></p>')
p4 = panel(B, 'scale', 'Kano: çocuğun bedeli', 'Kano: the price of a child', ''.join(
    f'<div class="num"><b>{n}</b><div>{t}<span class="en">{e}</span></div></div>' for n, t, e in [
    ('200', 'çocuk; yarısına ağızdan Trovan', 'children; half given oral Trovan'),
    ('1/3', 'doz: zayıflatılmış seftriakson kolu', 'dose: weakened ceftriaxone arm'),
    ('11', 'çocuk öldü (5 + 6)', 'children died (5 + 6)'),
    ('75 M$', 'uzlaşma, sorumluluk kabulü yok', 'settlement, no admission of liability'),
    ('175.000 $', 'aile başına ödeme (2011)', 'paid per family (2011)'),
    ('0', 'mahkûmiyet', 'convictions')]))
p5 = panel(N, 'flag', 'Türkiye: TCK 90/3', 'Turkey: Penal Code 90/3',
    '<div class="steps"><div class="yr" style="background:#7a1f2b"><b>2004</b> "Çocuklar üzerinde bilimsel deney hiçbir surette yapılamaz."'
    '<span class="en" style="color:#f1d9c0">Absolute ban: "under no circumstances".</span></div>'
    '<div class="yr" style="background:#2f5d50"><b>2005</b> 5328 sayılı Kanun: yürürlükten önce koşullu izin.'
    '<span class="en" style="color:#d5eadf">Changed before it took effect: conditional permission.</span></div></div><ul>' +
    li('Gereklilik:', 'bilgi yetişkinde elde edilemiyorsa.', 'Necessity: only if adults cannot provide the data.') +
    li('Çift onay:', 'çocuğun rızası + ebeveyn yazılı onayı.', 'Dual consent: child assent + parental permission.') +
    li('Kurulda', 'çocuk sağlığı uzmanı.', 'A paediatrician on the ethics board.') + '</ul>')
p6 = panel(Y, 'globe', 'Dünyanın cevabı', 'How the world solved it',
    '<p class="t">Dışlamak değil, <b>daha sıkı kurallarla</b> katmak.<span class="en">Not exclusion, but inclusion under stricter rules.</span></p>'
    '<div><span class="tag">45 CFR 46-D</span><span class="tag">Oviedo</span><span class="tag">FDAMA · BPCA · PREA</span><span class="tag">AB 1901/2006</span></div>'
    '<p class="t" style="margin-top:8px"><b>Gölge:</b> 6 ay ek tekel; çalışmalar en çok kazandıran ilaçlara gidiyor.'
    '<span class="en">The shadow: 6 extra months of exclusivity; trials go to the most profitable drugs.</span></p>'
    '<p class="t"><i>Kendi çocuğumuza razı olur muyduk?</i><span class="en">Would we accept it for our own child?</span></p>')

INFO = f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="top"><h1>TIBBİ ARAŞTIRMALARDA <em>ÇOCUKLAR</em></h1>
<div class="sub">Children in Medical Research</div>
<div class="s2">En korunmasız gönüllüler: istismar ile ihmal arasında · <i>Between exploitation and neglect</i></div></div>
<div class="grid">{p1}{p2}{p3}{p4}{p5}{p6}</div>
<div class="q"><div class="a">"Çocuklar için en tehlikeli araştırma, adı araştırma olmayan araştırmadır."</div>
<div class="b">"The most dangerous research for children is research that is not called research."</div></div>
<div class="foot">klinikfarmakoloji.com</div></body></html>"""

COVER = """<html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1500px;height:800px;font-family:'DejaVu Serif',Georgia,serif;color:#fbf3e6;
background:radial-gradient(ellipse at 70% 40%,#7a1d2a 0%,#5e1320 45%,#3e0c15 100%);position:relative;overflow:hidden}
.k{position:absolute;left:110px;top:150px;color:#d9b072;font-weight:bold;letter-spacing:5px;font-size:24px}
h1{position:absolute;left:110px;top:200px;width:880px;font-size:76px;line-height:1.02}
h1 em{font-style:normal;color:#e6c27c}
.en{position:absolute;left:110px;top:470px;color:#e6c27c;font-style:italic;font-weight:bold;font-size:34px}
.bar{position:absolute;left:110px;top:540px;width:140px;height:4px;background:#d9b072}
.q{position:absolute;left:110px;top:575px;width:880px;font-style:italic;font-size:25px;color:#f1e3cf;line-height:1.35}
.f{position:absolute;left:110px;bottom:28px;color:#d9b072;font-weight:bold;letter-spacing:4px;font-size:20px}
svg{position:absolute;right:45px;top:140px}
</style></head><body>
<div class="k">ACI İLAÇ · ARAŞTIRMA ETİĞİ</div>
<h1>TIBBİ<br>ARAŞTIRMALARDA<br><em>ÇOCUKLAR</em></h1>
<div class="en">Children in Medical Research</div>
<div class="bar"></div>
<div class="q">"Çocuklar tıbbi araştırmanın hem en çok istismar edilen hem de en çok ihmal edilen grubudur."</div>
<div class="f">KLINIKFARMAKOLOJI.COM</div>
<svg width="470" height="520" viewBox="-15 -10 470 520">
 <defs><filter id="sh"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-opacity=".35"/></filter></defs>
 <g filter="url(#sh)">
  <rect x="212" y="70" width="16" height="360" rx="4" fill="#d9b072"/>
  <rect x="140" y="420" width="160" height="22" rx="8" fill="#d9b072"/>
  <circle cx="220" cy="66" r="18" fill="#e6c27c"/>
  <g transform="rotate(-8 220 110)">
   <rect x="40" y="100" width="360" height="12" rx="6" fill="#e6c27c"/>
   <path d="M70 110 L20 240 M70 110 L120 240" stroke="#e6c27c" stroke-width="3"/>
   <path d="M370 110 L320 240 M370 110 L420 240" stroke="#e6c27c" stroke-width="3"/>
   <path d="M10 240 Q70 300 130 240 Z" fill="#f6efe4"/>
   <path d="M310 240 Q370 300 430 240 Z" fill="#f6efe4"/>
   <text x="70" y="335" text-anchor="middle" font-size="25" font-weight="bold" fill="#e6c27c">İSTİSMAR</text>
   <text x="70" y="362" text-anchor="middle" font-size="17" font-style="italic" fill="#f1e3cf">exploitation</text>
   <text x="370" y="335" text-anchor="middle" font-size="25" font-weight="bold" fill="#e6c27c">İHMAL</text>
   <text x="370" y="362" text-anchor="middle" font-size="17" font-style="italic" fill="#f1e3cf">neglect</text>
  </g>
  <g transform="translate(220 200)">
   <circle cx="0" cy="0" r="62" fill="#3e0c15" stroke="#d9b072" stroke-width="6"/>
   <circle cx="0" cy="-22" r="13" fill="#f6efe4"/>
   <path d="M-20 34 V8 Q-20 -4 -8 -4 H8 Q20 -4 20 8 V34 Z" fill="#f6efe4"/>
  </g>
 </g>
</svg></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for html_, w, h, name in [(INFO, 1080, 1350, 'tibbi-arastirmalarda-cocuklar-infografik.png'), (COVER, 1500, 800, 'tibbi-arastirmalarda-cocuklar-kapak.png')]:
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_content(html_)
        over = pg.evaluate("[...document.querySelectorAll('.p')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.querySelector('.pt').textContent)")
        if over: print('OVERFLOW', over)
        pg.screenshot(path=OUT + name); print('wrote', name)
    b.close()
