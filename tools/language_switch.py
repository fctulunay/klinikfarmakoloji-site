#!/usr/bin/env python3
"""TR / EN language switch in the header of every page (safe to re-run).

EN opens the same page through Google's page-translation service (<host>.translate.goog), which
translates the whole page (menus, sidebars, articles) and keeps the visitor in English as they
click through the site. TR returns to the original Turkish page.
Usage: python3 tools/language_switch.py
"""
import html, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOR = '<div class="region region-header-top-highlighted-second">'
BLOCK = r'''<div class="kfd-lang notranslate" translate="no">
<style>
.kfd-lang{display:flex;justify-content:flex-end;flex-wrap:wrap;gap:6px;padding:8px 4px 4px}
.kfd-lang button{display:inline-flex;padding:0;border:2px solid transparent;border-radius:3px;background:none;cursor:pointer;line-height:0;opacity:.8;box-shadow:0 0 0 1px rgba(0,0,0,.15)}
.kfd-lang button:hover{opacity:1}
.kfd-lang button.on{border-color:#651320;opacity:1;cursor:default}
@media (max-width:767px){.kfd-lang{justify-content:center;padding:6px 0 0}}
</style>
<button type="button" data-lang="tr" class="on" title="Türkçe" aria-label="Türkçe"><svg viewBox="0 0 1200 800" width="33" height="22" aria-hidden="true"><rect width="1200" height="800" fill="#E30A17"/><circle cx="425" cy="400" r="200" fill="#fff"/><circle cx="475" cy="400" r="160" fill="#E30A17"/><path fill="#fff" d="M583.334 400l180.901 58.779-111.804-153.885v190.212l111.804-153.885z"/></svg></button><button type="button" data-lang="en" class="" title="English" aria-label="English"><svg viewBox="0 0 1900 1000" width="42" height="22" aria-hidden="true"><rect width="1900" height="1000" fill="#B22234"/><rect y="76.9" width="1900" height="76.9" fill="#fff"/><rect y="230.8" width="1900" height="76.9" fill="#fff"/><rect y="384.6" width="1900" height="76.9" fill="#fff"/><rect y="538.5" width="1900" height="76.9" fill="#fff"/><rect y="692.3" width="1900" height="76.9" fill="#fff"/><rect y="846.2" width="1900" height="76.9" fill="#fff"/><rect width="760" height="538.5" fill="#3C3B6E"/><defs><polygon id="kfd-us-star" fill="#fff" points="0.0,-30.8 6.9,-9.5 29.3,-9.5 11.2,3.6 18.1,24.9 0.0,11.8 -18.1,24.9 -11.2,3.6 -29.3,-9.5 -6.9,-9.5"/></defs><use href="#kfd-us-star" x="63" y="54"/><use href="#kfd-us-star" x="189" y="54"/><use href="#kfd-us-star" x="315" y="54"/><use href="#kfd-us-star" x="441" y="54"/><use href="#kfd-us-star" x="567" y="54"/><use href="#kfd-us-star" x="693" y="54"/><use href="#kfd-us-star" x="126" y="108"/><use href="#kfd-us-star" x="252" y="108"/><use href="#kfd-us-star" x="378" y="108"/><use href="#kfd-us-star" x="504" y="108"/><use href="#kfd-us-star" x="630" y="108"/><use href="#kfd-us-star" x="63" y="162"/><use href="#kfd-us-star" x="189" y="162"/><use href="#kfd-us-star" x="315" y="162"/><use href="#kfd-us-star" x="441" y="162"/><use href="#kfd-us-star" x="567" y="162"/><use href="#kfd-us-star" x="693" y="162"/><use href="#kfd-us-star" x="126" y="216"/><use href="#kfd-us-star" x="252" y="216"/><use href="#kfd-us-star" x="378" y="216"/><use href="#kfd-us-star" x="504" y="216"/><use href="#kfd-us-star" x="630" y="216"/><use href="#kfd-us-star" x="63" y="270"/><use href="#kfd-us-star" x="189" y="270"/><use href="#kfd-us-star" x="315" y="270"/><use href="#kfd-us-star" x="441" y="270"/><use href="#kfd-us-star" x="567" y="270"/><use href="#kfd-us-star" x="693" y="270"/><use href="#kfd-us-star" x="126" y="324"/><use href="#kfd-us-star" x="252" y="324"/><use href="#kfd-us-star" x="378" y="324"/><use href="#kfd-us-star" x="504" y="324"/><use href="#kfd-us-star" x="630" y="324"/><use href="#kfd-us-star" x="63" y="378"/><use href="#kfd-us-star" x="189" y="378"/><use href="#kfd-us-star" x="315" y="378"/><use href="#kfd-us-star" x="441" y="378"/><use href="#kfd-us-star" x="567" y="378"/><use href="#kfd-us-star" x="693" y="378"/><use href="#kfd-us-star" x="126" y="432"/><use href="#kfd-us-star" x="252" y="432"/><use href="#kfd-us-star" x="378" y="432"/><use href="#kfd-us-star" x="504" y="432"/><use href="#kfd-us-star" x="630" y="432"/><use href="#kfd-us-star" x="63" y="486"/><use href="#kfd-us-star" x="189" y="486"/><use href="#kfd-us-star" x="315" y="486"/><use href="#kfd-us-star" x="441" y="486"/><use href="#kfd-us-star" x="567" y="486"/><use href="#kfd-us-star" x="693" y="486"/></svg></button><button type="button" data-lang="de" class="" title="Deutsch" aria-label="Deutsch"><svg viewBox="0 0 5 3" width="37" height="22" aria-hidden="true"><rect width="5" height="1" fill="#000"/><rect y="1" width="5" height="1" fill="#DD0000"/><rect y="2" width="5" height="1" fill="#FFCE00"/></svg></button><button type="button" data-lang="es" class="" title="Español" aria-label="Español"><svg viewBox="0 0 750 500" width="33" height="22" aria-hidden="true"><rect width="750" height="500" fill="#AA151B"/><rect y="125" width="750" height="250" fill="#F1BF00"/></svg></button><button type="button" data-lang="ru" class="" title="Русский" aria-label="Русский"><svg viewBox="0 0 9 6" width="33" height="22" aria-hidden="true"><rect width="9" height="2" fill="#fff"/><rect y="2" width="9" height="2" fill="#0039A6"/><rect y="4" width="9" height="2" fill="#D52B1E"/></svg></button><button type="button" data-lang="zh-CN" class="" title="中文" aria-label="中文"><svg viewBox="0 0 30 20" width="33" height="22" aria-hidden="true"><rect width="30" height="20" fill="#EE1C25"/><polygon fill="#FFDE00" points="5.00,2.00 5.67,4.07 7.85,4.07 6.09,5.35 6.76,7.43 5.00,6.15 3.24,7.43 3.91,5.35 2.15,4.07 4.33,4.07"/><polygon fill="#FFDE00" points="9.14,2.51 9.62,1.97 9.25,1.34 9.91,1.63 10.39,1.08 10.33,1.80 11.00,2.09 10.29,2.25 10.22,2.97 9.85,2.35"/><polygon fill="#FFDE00" points="11.01,4.14 11.66,3.82 11.56,3.10 12.07,3.62 12.72,3.30 12.38,3.95 12.88,4.47 12.17,4.34 11.83,4.99 11.73,4.27"/><polygon fill="#FFDE00" points="11.04,6.73 11.76,6.70 11.96,6.00 12.21,6.68 12.94,6.66 12.37,7.10 12.62,7.79 12.01,7.38 11.44,7.83 11.64,7.13"/><polygon fill="#FFDE00" points="9.22,8.38 9.90,8.63 10.35,8.06 10.32,8.79 11.00,9.05 10.30,9.24 10.26,9.96 9.87,9.36 9.16,9.55 9.62,8.98"/></svg></button><button type="button" data-lang="hi" class="" title="हिन्दी" aria-label="हिन्दी"><svg viewBox="0 0 30 20" width="33" height="22" aria-hidden="true"><rect width="30" height="20" fill="#fff"/><rect width="30" height="6.667" fill="#FF9933"/><rect y="13.333" width="30" height="6.667" fill="#138808"/><circle cx="15" cy="10" r="2.9" fill="none" stroke="#000080" stroke-width="0.5"/><line x1="15" y1="10" x2="17.60" y2="10.00" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="17.51" y2="10.67" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="17.25" y2="11.30" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="16.84" y2="11.84" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="16.30" y2="12.25" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="15.67" y2="12.51" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="15.00" y2="12.60" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="14.33" y2="12.51" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="13.70" y2="12.25" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="13.16" y2="11.84" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="12.75" y2="11.30" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="12.49" y2="10.67" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="12.40" y2="10.00" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="12.49" y2="9.33" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="12.75" y2="8.70" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="13.16" y2="8.16" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="13.70" y2="7.75" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="14.33" y2="7.49" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="15.00" y2="7.40" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="15.67" y2="7.49" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="16.30" y2="7.75" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="16.84" y2="8.16" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="17.25" y2="8.70" stroke="#000080" stroke-width="0.25"/><line x1="15" y1="10" x2="17.51" y2="9.33" stroke="#000080" stroke-width="0.25"/><circle cx="15" cy="10" r="0.6" fill="#000080"/></svg></button>
<script>
(function(){
  var S='.translate.goog', h=location.hostname, inTr=h.slice(-S.length)===S;
  var LANGS={en:'en',de:'de',es:'es',ru:'ru',zh:'zh-CN',hi:'hi',tr:'tr'};
  /* language the page was written in (most are Turkish; a few articles are English) */
  var SRC=(document.documentElement.getAttribute('data-kfd-src')||'tr');
  var cur=inTr?(new URLSearchParams(location.search).get('_x_tr_tl')||'en'):SRC;
  function origHost(){return h.slice(0,-S.length).replace(/--/g,'\u0000').replace(/-/g,'.').replace(/\u0000/g,'-');}
  function encHost(x){return x.replace(/-/g,'--').replace(/\./g,'-');}
  function save(l){try{localStorage.setItem('kfd-lang2',l);}catch(e){}}
  function saved(){try{return localStorage.getItem('kfd-lang2');}catch(e){return null;}}
  function toLang(l){
    if(l===SRC){location.href='https://'+(inTr?origHost():h)+location.pathname+'?kfd_lang='+l+location.hash;return;}
    var host=inTr?h:encHost(h)+S;
    location.href='https://'+host+location.pathname+'?_x_tr_sl='+SRC+'&_x_tr_tl='+l+'&_x_tr_hl='+l+location.hash;
  }
  /* the search page translates its own results: the flags just change its language */
  if(!inTr && location.pathname.indexOf('/arama/')===0){
    var sp=new URLSearchParams(location.search), sl=sp.get('lang')||'tr', fb=document.querySelectorAll('.kfd-lang button');
    for(var j=0;j<fb.length;j++){(function(b){ var l=b.getAttribute('data-lang'); b.className=(l===sl)?'on':'';
      b.onclick=function(){ save(l); if(l==='tr') sp.delete('lang'); else sp.set('lang',l); location.search=sp.toString(); }; })(fb[j]);}
    return;
  }
  /* buttons */
  var bs=document.querySelectorAll('.kfd-lang button');
  for(var i=0;i<bs.length;i++){(function(b){
    var l=b.getAttribute('data-lang'); b.className=(l===cur)?'on':'';
    b.onclick=function(){ if(l===cur) return; if(!inTr) save(l); toLang(l); };
  })(bs[i]);}
  if(inTr) return;
  /* a choice made on a translated page comes back as ?kfd_lang=… */
  var qs=new URLSearchParams(location.search), q=qs.get('kfd_lang');
  if(q){ save(q); qs.delete('kfd_lang'); var rest=qs.toString();
    history.replaceState(null,'',location.pathname+(rest?'?'+rest:'')+location.hash); return; }
  /* automatic language: the visitor's saved choice, otherwise their browser language */
  if(/bot|crawl|spider|slurp|preview|facebookexternalhit|embedly|lighthouse|headless|pagespeed/i.test(navigator.userAgent)) return;
  var want=saved();
  /* the visitor's country, read from the computer's time zone (no lookup needed) */
  if(!want){ try{ var z=Intl.DateTimeFormat().resolvedOptions().timeZone||'';
    if(/^(Europe|Asia)\/Istanbul$/.test(z)) want='tr';
    else if(/^(Europe\/(Berlin|Vienna|Zurich|Busingen|Vaduz))$/.test(z)) want='de';
    else if(/^(Europe\/Madrid|Atlantic\/Canary|Africa\/Ceuta|America\/(Mexico_City|Cancun|Merida|Monterrey|Matamoros|Chihuahua|Ciudad_Juarez|Ojinaga|Hermosillo|Mazatlan|Bahia_Banderas|Tijuana|Bogota|Lima|Santiago|Punta_Arenas|Argentina\/.*|Buenos_Aires|Caracas|Montevideo|Asuncion|La_Paz|Guayaquil|Havana|Santo_Domingo|Guatemala|El_Salvador|Tegucigalpa|Managua|Costa_Rica|Panama|Puerto_Rico))$/.test(z)) want='es';
    else if(/^(Europe\/(Moscow|Kaliningrad|Samara|Volgograd|Saratov|Ulyanovsk|Astrakhan|Kirov|Minsk)|Asia\/(Yekaterinburg|Omsk|Novosibirsk|Barnaul|Tomsk|Novokuznetsk|Krasnoyarsk|Irkutsk|Chita|Yakutsk|Khandyga|Vladivostok|Ust-Nera|Magadan|Sakhalin|Srednekolymsk|Kamchatka|Anadyr))$/.test(z)) want='ru';
    else if(/^Asia\/(Shanghai|Urumqi|Chongqing|Harbin|Hong_Kong|Macau)$/.test(z)) want='zh-CN';
    else if(/^Asia\/(Kolkata|Calcutta)$/.test(z)) want='hi';
    else if(/^(America\/(?!Sao_Paulo|Fortaleza|Recife|Bahia|Belem|Manaus|Cuiaba|Campo_Grande|Porto_Velho|Boa_Vista|Rio_Branco|Araguaina|Maceio|Santarem|Eirunepe|Noronha)|US\/|Canada\/|Pacific\/Honolulu|Europe\/(London|Dublin)|Australia\/|Pacific\/Auckland)/.test(z)) want='en';
  }catch(e){} }
  /* otherwise the browser language */
  if(!want){
    var list=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'tr'];
    for(var k=0;k<list.length;k++){ var code=String(list[k]).toLowerCase().split('-')[0]; if(LANGS[code]){ want=LANGS[code]; break; } }
  }
  if(want && want!==SRC && LANGS[want.split('-')[0]]) toLang(want);
})();
</script>
</div>'''
OLD = re.compile(r'\n?<div class="kfd-lang notranslate".*?</script>\n</div>', re.S)

TR_CHARS = set('ğüşıöçĞÜŞİÖÇ')
EN_WORDS = re.compile(r'\b(the|and|of|to|in|is|that|with|for|are|this|was)\b', re.I)
TR_WORDS = re.compile(r'\b(ve|bir|bu|ile|için|olarak|da|de|olan|gibi|daha)\b', re.I)

def body_text(t):
    m = re.search(r'<div property="schema:text"[^>]*class="[^"]*field--name-body[^"]*"[^>]*>', t)
    if not m: return ''
    i = m.end(); d = 1
    for x in re.finditer(r'<(/?)div\b', t[i:]):
        d += -1 if x.group(1) else 1
        if d == 0: break
    seg = t[i:i + x.start()] if d == 0 else t[i:i + 200000]
    seg = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', seg, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', seg))[:20000]

def detect_lang(t):
    """'en' when the article text is clearly English, otherwise 'tr'."""
    s = body_text(t)
    words = re.findall(r'\w+', s)
    if len(words) < 80: return 'tr'
    en = len(EN_WORDS.findall(s)); tr = len(TR_WORDS.findall(s))
    trc = sum(c in TR_CHARS for c in s) / max(1, len(s))
    return 'en' if en > 3 * max(tr, 1) and trc < 0.004 else 'tr'

def mark_source_language(t):
    m = re.search(r'<html\b[^>]*>', t)
    if not m: return t
    tag = re.sub(r'\s+data-kfd-src="[^"]*"', '', m.group(0))
    lang = detect_lang(t) if 'node--view-mode-full' in t else 'tr'
    if lang != 'tr':
        tag = tag[:-1] + f' data-kfd-src="{lang}">'
        tag = re.sub(r'\blang="tr"', f'lang="{lang}"', tag)
    else:
        tag = re.sub(r'\blang="en"', 'lang="tr"', tag)
    return t[:m.start()] + tag + t[m.end():]

def main():
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', '.git/')): continue
        t = open(fp, encoding='utf-8').read()
        if ANCHOR not in t: continue
        t2 = OLD.sub('', t)
        t2 = t2.replace(ANCHOR, ANCHOR + '\n' + BLOCK, 1)
        t2 = mark_source_language(t2)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
    print(f'language switch on {n} pages')

if __name__ == '__main__':
    main()
