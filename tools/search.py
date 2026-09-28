#!/usr/bin/env python3
"""Site search (Pagefind). Safe to re-run; run after any content change.

1. marks article pages for indexing (article text, title, section filter, image, date)
2. puts a search box in the header of every page
3. writes the results page /arama/
4. rebuilds the search index in /pagefind/ (needs Node: npx pagefind)
Usage: python3 tools/search.py
"""
import os, re, glob, html, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOR = '<div class="region region-header-top-highlighted-second">'
BOX = r'''<form class="kfd-search notranslate" action="/arama/" method="get" role="search">
<style>
.kfd-search{display:flex;justify-content:flex-end;padding:6px 4px 2px;margin:0}
.kfd-search input{width:100%;max-width:230px;font:15px Georgia,serif;padding:6px 10px;border:1px solid #cdbfc3;border-right:0;border-radius:3px 0 0 3px;background:#fff;color:#222}
.kfd-search input:focus{outline:2px solid #651320;outline-offset:0}
.kfd-search button{font:bold 14px Georgia,serif;padding:6px 12px;border:1px solid #651320;background:#651320;color:#fff;border-radius:0 3px 3px 0;cursor:pointer}
@media (max-width:767px){.kfd-search{justify-content:center}.kfd-search input{max-width:none}}
</style>
<label for="kfd-q" class="visually-hidden">Sitede ara</label>
<input id="kfd-q" type="search" name="q" placeholder="Sitede ara…" autocomplete="off"><button type="submit">Ara</button>
<script>
(function(){
  var S='.translate.goog', inTr=location.hostname.slice(-S.length)===S, P=new URLSearchParams(location.search);
  var f=document.currentScript.parentNode, ui=(inTr?(P.get('_x_tr_tl')||'en'):(location.pathname.indexOf('/arama/')===0?(P.get('lang')||'tr'):(document.documentElement.getAttribute('data-kfd-src')||'tr'))).split('-')[0];
  var L={tr:['Sitede ara…','Ara'],en:['Search the site…','Search'],de:['Website durchsuchen…','Suchen'],es:['Buscar en el sitio…','Buscar'],ru:['Поиск по сайту…','Найти'],zh:['站内搜索…','搜索'],hi:['साइट में खोजें…','खोजें']}[ui];
  if(L){ f.querySelector('input').placeholder=L[0]; f.querySelector('button').textContent=L[1]; }
  f.onsubmit=function(ev){ ev.preventDefault(); var v=f.querySelector('input').value.trim(); if(!v) return;
    var host=inTr?location.hostname.slice(0,-S.length).replace(/--/g,'\u0000').replace(/-/g,'.').replace(/\u0000/g,'-'):location.hostname;
    var lang=inTr?(P.get('_x_tr_tl')||'en'):(location.pathname.indexOf('/arama/')===0?(P.get('lang')||'tr'):'tr');
    location.href='https://'+host+'/arama/?q='+encodeURIComponent(v)+(lang!=='tr'?'&lang='+encodeURIComponent(lang):''); };
})();
</script>
</form>'''
OLD_BOX = re.compile(r'\n?<form class="kfd-search notranslate".*?</form>', re.S)

RESULTS = r'''<div id="kfd-arama" data-pagefind-ignore>
<style>
#kfd-arama{font-family:Georgia,"Times New Roman",serif;color:#1c1a1b}
#kfd-arama form{display:flex;margin:0 0 14px}
#kfd-arama input{flex:1;font:17px Georgia,serif;padding:9px 12px;border:1px solid #cdbfc3;border-right:0;border-radius:3px 0 0 3px}
#kfd-arama input:focus{outline:2px solid #651320}
#kfd-arama button.kfd-go{font:bold 15px Georgia,serif;padding:9px 16px;border:1px solid #651320;background:#651320;color:#fff;border-radius:0 3px 3px 0;cursor:pointer}
#kfd-status{font-weight:bold;margin:0 0 10px;color:#651320}
#kfd-filters{margin:0 0 12px}
#kfd-filters button{font:14px Georgia,serif;margin:0 6px 6px 0;padding:4px 10px;border:1px solid #d0c5b3;background:#f5eee0;border-radius:14px;cursor:pointer;color:#1c1a1b}
#kfd-filters button.on{background:#651320;color:#fff;border-color:#651320}
.kfd-res{display:flex;gap:12px;padding:10px 0;border-bottom:1px dotted #d0c5b3}
.kfd-res img{width:120px;height:auto;flex:0 0 120px;border-radius:3px;align-self:flex-start}
.kfd-res a.t{font-weight:bold;color:#651320;font-size:1.08em;text-decoration:none}
.kfd-res a.t:hover{text-decoration:underline}
.kfd-res p{margin:4px 0 0;font-size:.95em;line-height:1.45}
.kfd-res mark{background:#f1dfe3;color:inherit}
.kfd-res .sec{font-size:.8em;color:#666}
#kfd-more{display:none;margin:14px 0;font:bold 15px Georgia,serif;padding:8px 16px;border:1px solid #651320;background:#fff;color:#651320;border-radius:3px;cursor:pointer}
@media (max-width:600px){.kfd-res img{width:90px;flex-basis:90px}}
</style>
<form id="kfd-form" class="notranslate"><input id="kfd-input" type="search" name="q" autocomplete="off"><button class="kfd-go" type="submit">Ara</button></form>
<div id="kfd-status"></div>
<div id="kfd-filters"></div>
<div id="kfd-results"></div>
<button id="kfd-more" type="button">Daha fazla sonuç</button>
<script>
(function(){
  var S='.translate.goog', h=location.hostname, inTr=h.slice(-S.length)===S, P=new URLSearchParams(location.search);
  function origHost(x){return x.slice(0,-S.length).replace(/--/g,'\u0000').replace(/-/g,'.').replace(/\u0000/g,'-');}
  function encHost(x){return x.replace(/-/g,'--').replace(/\./g,'-');}
  /* the search runs on the site itself (Google's translation window can't load the search index) */
  if(inTr){ location.replace('https://'+origHost(h)+'/arama/?q='+encodeURIComponent(P.get('q')||'')+'&lang='+encodeURIComponent(P.get('_x_tr_tl')||'en')); return; }
  var LANG=(P.get('lang')||'tr'), UI=LANG.split('-')[0];
  var T={
    tr:{ph:'Sitede ara…',go:'Ara',h:'Arama Sonuçları',ing:'aranıyor…',res:'sonuç',none:'için sonuç bulunamadı.',for_:'için',more:'Daha fazla sonuç',err:'Arama şu anda yüklenemedi. Lütfen sayfayı yenileyin.',home:'Ana Sayfa'},
    en:{ph:'Search the site…',go:'Search',h:'Search Results',ing:'searching…',res:'results',none:'no results found.',for_:'for',more:'More results',err:'Search could not load. Please refresh the page.',home:'Home'},
    de:{ph:'Website durchsuchen…',go:'Suchen',h:'Suchergebnisse',ing:'wird gesucht…',res:'Ergebnisse',none:'keine Ergebnisse.',for_:'für',more:'Weitere Ergebnisse',err:'Die Suche konnte nicht geladen werden.',home:'Startseite'},
    es:{ph:'Buscar en el sitio…',go:'Buscar',h:'Resultados de búsqueda',ing:'buscando…',res:'resultados',none:'sin resultados.',for_:'para',more:'Más resultados',err:'No se pudo cargar la búsqueda.',home:'Inicio'},
    ru:{ph:'Поиск по сайту…',go:'Найти',h:'Результаты поиска',ing:'поиск…',res:'результатов',none:'ничего не найдено.',for_:'для',more:'Ещё результаты',err:'Не удалось загрузить поиск.',home:'Главная'},
    zh:{ph:'站内搜索…',go:'搜索',h:'搜索结果',ing:'正在搜索…',res:'条结果',none:'没有找到结果。',for_:'',more:'更多结果',err:'搜索无法加载。',home:'首页'},
    hi:{ph:'साइट में खोजें…',go:'खोजें',h:'खोज परिणाम',ing:'खोज रहे हैं…',res:'परिणाम',none:'कोई परिणाम नहीं मिला।',for_:'के लिए',more:'और परिणाम',err:'खोज लोड नहीं हो सकी।',home:'होम'}
  }[UI]||null; if(!T){ UI='en'; LANG='en'; }
  T=T||{ph:'Search the site…',go:'Search',h:'Search Results',ing:'searching…',res:'results',none:'no results found.',for_:'for',more:'More results',err:'Search could not load.',home:'Home'};
  var input=document.getElementById('kfd-input'), st=document.getElementById('kfd-status'), box=document.getElementById('kfd-results'),
      fl=document.getElementById('kfd-filters'), more=document.getElementById('kfd-more');
  input.placeholder=T.ph; document.querySelector('#kfd-form .kfd-go').textContent=T.go; more.textContent=T.more;
  if(UI!=='tr'){
    document.documentElement.lang=UI;
    var h1=document.querySelector('h1.page-title'); if(h1) h1.textContent=T.h;
    document.title=T.h+' | Klinik Farmakoloji Dosyası';
    var bc=document.querySelectorAll('.breadcrumb__items li'); if(bc.length){ var a=bc[0].querySelector('a'); if(a) a.textContent=T.home; var sp=bc[bc.length-1].querySelector('span'); if(sp) sp.textContent=T.h; }
  }
  var q=(P.get('q')||'').trim(); input.value=q;
  document.getElementById('kfd-form').onsubmit=function(ev){ev.preventDefault(); var u=new URL(location.href); u.searchParams.set('q',input.value.trim()); location.href=u.toString();};
  if(!q){ input.focus(); return; }
  function quote(x){return (UI==='zh'?'“'+x+'”':'"'+x+'"');}
  st.textContent=quote(q)+' '+T.ing;
  function gt(s,tl){ /* Google Translate (free web endpoint); on failure the text stays as it is */
    return fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl='+tl+'&dt=t&q='+encodeURIComponent(s))
      .then(function(r){return r.json();}).then(function(j){ return (j[0]||[]).map(function(x){return x[0];}).join('').trim()||s; })
      .catch(function(){ return s; });
  }
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
  function link(u){ if(LANG==='tr') return u;
    return 'https://'+encHost(h)+S+u+'?_x_tr_sl=auto&_x_tr_tl='+LANG+'&_x_tr_hl='+LANG; }
  import('/pagefind/pagefind.js').then(function(pf){
    return pf.options({excerptLength:30}).then(function(){
    return gt(q,'tr').then(function(tq){
      var terms=[q]; if(tq && tq.toLowerCase()!==q.toLowerCase()) terms.push(tq);
      return Promise.all(terms.map(function(x){return pf.search(x);})).then(function(rs){
        var seen={}, all=[];
        rs.forEach(function(r){ (r&&r.results||[]).forEach(function(x){ if(!seen[x.id]){seen[x.id]=x; all.push(x);} else { seen[x.id].score=Math.max(seen[x.id].score,x.score); } }); });
        all.sort(function(a,b){return b.score-a.score;});
        return {all:all, terms:terms};
      });
    });
    });
  }).then(function(R){
    var all=R.all, shown=0, filter='', data=[], secName={};
    var label=R.terms.map(quote).join(' / ');
    if(!all.length){ st.textContent=label+' '+T.none; return; }
    function secLabel(s){ return secName[s]||s; }
    function render(){
      var list=data.filter(function(d){return !filter || (d.filters && d.filters['Bölüm'] && d.filters['Bölüm'].indexOf(filter)>=0);});
      st.textContent=(UI==='tr'||UI==='hi'?label+' '+T.for_+' ':(T.for_?'':''))+(filter?list.length+' / ':'')+all.length+' '+T.res+(UI!=='tr'&&UI!=='hi'?(T.for_?' '+T.for_+' ':' ')+label:'');
      box.innerHTML=list.map(function(d){
        var img=d.meta&&d.meta.image?'<img src="'+d.meta.image+'" alt="" loading="lazy">':'';
        var sec=d.filters&&d.filters['Bölüm']?'<div class="sec">'+esc(d.filters['Bölüm'].map(secLabel).join(', '))+'</div>':'';
        return '<div class="kfd-res">'+img+'<div><a class="t" href="'+link(d.url)+'">'+esc(d.tTitle||d.meta&&d.meta.title||d.url)+'</a>'+sec+'<p>'+(d.tExcerpt?esc(d.tExcerpt):d.excerpt)+'</p></div></div>';
      }).join('');
      more.style.display=shown<all.length?'inline-block':'none';
    }
    function filters(){
      var secs={}; data.forEach(function(d){ (d.filters&&d.filters['Bölüm']||[]).forEach(function(s){secs[s]=(secs[s]||0)+1;}); });
      var keys=Object.keys(secs);
      fl.innerHTML=keys.length>1?keys.map(function(s){return '<button type="button" class="'+(s===filter?'on':'')+'" data-s="'+esc(s)+'">'+esc(secLabel(s))+' ('+secs[s]+')</button>';}).join(''):'';
      Array.prototype.forEach.call(fl.querySelectorAll('button'),function(b){ b.onclick=function(){ filter=(filter===b.getAttribute('data-s'))?'':b.getAttribute('data-s'); filters(); render(); }; });
      if(UI!=='tr') keys.forEach(function(s){ if(!secName[s]){ secName[s]=s; gt(s,LANG).then(function(x){ secName[s]=x; filters(); render(); }); } });
    }
    function load(n){
      var part=all.slice(shown,shown+n); shown+=part.length;
      return Promise.all(part.map(function(x){return x.data();})).then(function(ds){
        ds.forEach(function(d){ d.url=d.url.replace(/index\.html$/,''); data.push(d); });
        filters(); render();
        if(UI!=='tr') ds.forEach(function(d){
          var ex=d.excerpt.replace(/<[^>]+>/g,'');
          gt((d.meta&&d.meta.title||'')+'\n'+ex, LANG).then(function(x){ var i=x.indexOf('\n'); d.tTitle=i<0?x:x.slice(0,i); d.tExcerpt=i<0?'':x.slice(i+1); render(); });
        });
      });
    }
    more.onclick=function(){ load(20); };
    load(20);
  }).catch(function(e){ st.textContent=T.err; if(window.console) console.error(e); });
})();
</script>
</div>'''

TAG = re.compile(r'<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>')
def span_end(t, s):
    name = TAG.match(t, s).group(2).lower(); d = 0
    for m in TAG.finditer(t, s):
        if m.group(2).lower() != name or m.group(3): continue
        d += -1 if m.group(1) else 1
        if d == 0: return m.end()

def pages():
    for fp in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', 'pagefind/', '.git/')): continue
        yield fp, rel

def mark_article(t):
    a = t.find('<article data-history-node-id')
    if a < 0 or 'node--view-mode-full' not in t[a:a + 400]: return t
    head = t[a:t.find('>', a) + 1]
    if 'data-pagefind-body' not in head:
        t = t[:a] + head.replace('<article ', '<article data-pagefind-body ', 1) + t[a + len(head):]
    t = re.sub(r'<h1 class="title page-title"(?![^>]*data-pagefind-meta)', '<h1 class="title page-title" data-pagefind-meta="title"', t, count=1)
    t = re.sub(r'(<div class="field field--name-field-yazi-turu[^"]*")(?![^>]*data-pagefind-filter)', r'\1 data-pagefind-filter="Bölüm"', t, count=1)
    t = re.sub(r'(<div class="field field--name-field-one-cikan-gorsel[^>]*>\s*<img )(?!data-pagefind-meta)', r'\1data-pagefind-meta="image[src]" ', t, count=1)
    for cls in ('kfd-like', 'a2a_kit', 'node__side'):
        t = re.sub(r'(<(?:div|span) class="' + cls + r'[^"]*")(?![^>]*data-pagefind-ignore)', r'\1 data-pagefind-ignore', t)
    return t

def build_results_page():
    tpl = open(os.path.join(ROOT, 'iletisim', 'index.html'), encoding='utf-8').read()
    s = tpl.find('id="block-topplus-lite-content"'); s = tpl.rfind('<', 0, s); e = span_end(tpl, s)
    page = tpl[:s] + '<div id="block-topplus-lite-content" class="clearfix block block-system block-system-main-block"><div class="content">' + RESULTS + '</div></div>' + tpl[e:]
    page = re.sub(r'<title>.*?</title>', '<title>Arama Sonuçları | Klinik Farmakoloji Dosyası</title>', page, count=1, flags=re.S)
    page = re.sub(r'(<h1 class="title page-title"[^>]*>)(.*?)(</h1>)', r'\1Arama Sonuçları\3', page, count=1, flags=re.S)
    page = re.sub(r'(<ol class="breadcrumb__items">.*?<span>)İletişim(</span>)', r'\1Arama Sonuçları\2', page, count=1, flags=re.S)
    page = re.sub(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="/arama/" />', page, count=1)
    page = page.replace('<head>', '<head>\n<meta name="robots" content="noindex, follow" />', 1)
    page = re.sub(r'\s*<meta property="og:url"[^>]*>', '', page)
    os.makedirs(os.path.join(ROOT, 'arama'), exist_ok=True)
    open(os.path.join(ROOT, 'arama', 'index.html'), 'w', encoding='utf-8').write(page)

def main():
    n = m = 0
    for fp, rel in pages():
        if rel.startswith('arama/'): continue
        t = open(fp, encoding='utf-8').read()
        t2 = mark_article(t)
        if ANCHOR in t2:
            t2 = OLD_BOX.sub('', t2)
            li = t2.find('<div class="kfd-lang notranslate"')
            le = t2.find('</script>\n</div>', li) + len('</script>\n</div>') if li >= 0 else -1
            t2 = (t2[:le] + '\n' + BOX + t2[le:]) if li >= 0 else t2.replace(ANCHOR, ANCHOR + '\n' + BOX, 1)
        if t2 != t:
            open(fp, 'w', encoding='utf-8').write(t2); n += 1
        if 'data-pagefind-body' in t2: m += 1
    build_results_page()
    print(f'search box/markers updated on {n} pages; {m} article pages indexed')
    r = subprocess.run(['npx', '-y', 'pagefind@1', '--site', ROOT, '--glob', '**/index.html', '--force-language', 'tr'],
                       capture_output=True, text=True)
    print(r.stdout[-800:] or r.stderr[-800:])

if __name__ == '__main__':
    main()
