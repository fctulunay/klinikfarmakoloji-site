#!/usr/bin/env python3
"""Add a new article to the static klinikfarmakoloji.com site.

Usage:  python3 tools/publish_article.py article.json

article.json:
{
  "section": "aci-ilac",                 # URL prefix of the section
  "slug": "biyobenzer-urunlerde-...",
  "title": "BİYOBENZER ÜRÜNLERDE ...",
  "date": "2026-09-27",                  # publication date (YYYY-MM-DD)
  "image": "/sites/default/files/yazi-gorselleri/2026-09/x.png",   # original image (already in place)
  "image_750x400": "/sites/default/files/styles/manset_resim_stili_750x400/public/yazi-gorselleri/2026-09/x.png",
  "body_file": "tools/articles/x.body.html",   # body HTML (inner HTML of the body field)
  "summary": "…"                          # optional plain-text teaser for the taxonomy list
}

What it does
  1. writes <section>/<slug>/index.html from the newest article page of that section
  2. puts the article on top of the section list (/<section>/ …/page/N/) and the taxonomy list
     (/<section>-0/ …), re-paginating 10 per page and regenerating the pagers
  3. adds it as the first slide of the homepage slider (keeps 5 slides)
  4. puts it first in the section's sidebar box on every page (keeps 5)
  5. adds /index.php/… and /node/N redirects and a sitemap entry
  6. refreshes the social-media preview tags (tools/social_meta.py) and the like buttons (tools/like_button.py)
"""
import os, re, sys, json, html, glob, math, datetime, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = re.compile(r'<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>')
MONTHS = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
SECTION_NAMES = {'aci-ilac': 'Acı İlaç', 'editorden': 'Editörden', 'bilimsel-yazilar': 'Bilimsel Yazılar',
                 'konuk-yazar': 'Konuk Yazar', 'sektoru-taniyalim': 'Sektörü Tanıyalım', 'haber': 'Haber'}
PER_PAGE = 10


# ---------------------------------------------------------------- html helpers
def span_end(t, s):
    name = TAG.match(t, s).group(2).lower(); d = 0
    for m in TAG.finditer(t, s):
        if m.group(2).lower() != name or m.group(3): continue
        d += -1 if m.group(1) else 1
        if d == 0: return m.end()
    raise ValueError('unbalanced ' + name)

def block(t, marker, start=0, end=None):
    i = t.find(marker, start, end if end is not None else len(t))
    if i < 0: return None
    s = i if t.startswith('<', i) else t.rfind('<', 0, i)
    return s, span_end(t, s)

def rows_in(t, s, e):
    out = []; i = s
    while True:
        j = t.find('<div class="views-row">', i, e)
        if j < 0: return out
        k = span_end(t, j); out.append(t[j:k]); i = k

def read(p): return open(os.path.join(ROOT, p.lstrip('/')), encoding='utf-8').read()
def write(p, s):
    fp = os.path.join(ROOT, p.lstrip('/')); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(s)

def listing_pages(prefix):
    pages = [f'{prefix}/index.html']; n = 1
    while os.path.exists(os.path.join(ROOT, f'{prefix}/page/{n}/index.html')):
        pages.append(f'{prefix}/page/{n}/index.html'); n += 1
    return pages

def page_url(prefix, n): return f'/{prefix}/' if n == 0 else f'/{prefix}/page/{n}/'


# ---------------------------------------------------------------- pagers (Drupal markup)
def full_pager(prefix, cur, total, quantity=9):
    L = ['<nav class="pager" role="navigation" aria-labelledby="pagination-heading">',
         '    <h4 id="pagination-heading" class="visually-hidden">Pagination</h4>',
         '    <ul class="pager__items js-pager__items">']
    def link(n): return page_url(prefix, n)
    if cur > 0:
        L += [f'''        <li class="pager__item pager__item--first">
          <a href="{link(0)}" title="İlk sayfaya git">
            <span class="visually-hidden">İlk sayfa</span>
            <span aria-hidden="true">« ilk</span>
          </a>
        </li>''', f'''        <li class="pager__item pager__item--previous">
          <a href="{link(cur - 1)}" title="Önceki sayfaya dön" rel="prev">
            <span class="visually-hidden">Önceki sayfa</span>
            <span aria-hidden="true">‹ Önceki</span>
          </a>
        </li>''']
    middle = math.ceil(quantity / 2); pc = cur + 1
    first = pc - middle + 1; last = pc + quantity - middle
    if last > total: first += total - last; last = total
    if first <= 0: last += 1 - first; first = 1
    last = min(last, total)
    if first > 1: L.append('        <li class="pager__item pager__item--ellipsis" role="presentation">&hellip;</li>')
    for i in range(first, last + 1):
        if i == pc:
            L.append(f'''        <li class="pager__item is-active">
          <a href="{link(i - 1)}" title="Şu an kullanılan sayfa">
            <span class="visually-hidden">
              Şu an kullanılan sayfa
            </span>{i}</a>
        </li>''')
        else:
            L.append(f'''        <li class="pager__item">
          <a href="{link(i - 1)}" title="Go to page {i}">
            <span class="visually-hidden">
              Page
            </span>{i}</a>
        </li>''')
    if last < total: L.append('        <li class="pager__item pager__item--ellipsis" role="presentation">&hellip;</li>')
    if cur < total - 1:
        L += [f'''        <li class="pager__item pager__item--next">
          <a href="{link(cur + 1)}" title="Sonraki sayfaya git" rel="next">
            <span class="visually-hidden">Sonraki sayfa</span>
            <span aria-hidden="true">Sonraki ›</span>
          </a>
        </li>''', f'''        <li class="pager__item pager__item--last">
          <a href="{link(total - 1)}" title="Son sayfaya git">
            <span class="visually-hidden">Last page</span>
            <span aria-hidden="true">Son »</span>
          </a>
        </li>''']
    L += ['    </ul>', '  </nav>']
    return '\n'.join(L)

def mini_pager(prefix, cur, total):
    L = ['<nav class="pager" role="navigation" aria-labelledby="pagination-heading">',
         '    <h4 class="pager__heading visually-hidden">Pagination</h4>',
         '    <ul class="pager__items js-pager__items">']
    if cur > 0:
        L.append(f'''        <li class="pager__item pager__item--previous">
          <a href="{page_url(prefix, cur - 1)}" title="Önceki sayfaya dön" rel="prev">
            <span class="visually-hidden">Önceki sayfa</span>
            <span aria-hidden="true">‹‹</span>
          </a>
        </li>''')
    L.append(f'''        <li class="pager__item is-active">
          Sayfa {cur + 1}         </li>''')
    if cur < total - 1:
        L.append(f'''        <li class="pager__item pager__item--next">
          <a href="{page_url(prefix, cur + 1)}" title="Sonraki sayfaya git" rel="next">
            <span class="visually-hidden">Sonraki sayfa</span>
            <span aria-hidden="true">››</span>
          </a>
        </li>''')
    L += ['    </ul>', '  </nav>']
    return '\n'.join(L)


# ---------------------------------------------------------------- listings
def relist(prefix, new_row, pager_kind):
    """Prepend new_row to the paginated listing at /prefix/, re-chunk, rewrite pagers."""
    pages = listing_pages(prefix)
    docs = [read(p) for p in pages]
    allrows = []; spans = []
    for t in docs:
        s, e = block(t, 'id="block-topplus-lite-content"')
        vs, ve = block(t, '<div class="view-content">', s, e)
        rs = rows_in(t, vs, ve); allrows += rs; spans.append((vs, ve))
    href = re.search(r'href="([^"]+)"', new_row).group(1)
    if any(href in r for r in allrows[:PER_PAGE]):
        print(f'  {prefix}: already listed, skipped'); return
    allrows.insert(0, new_row)
    total = math.ceil(len(allrows) / PER_PAGE)
    while len(docs) < total:                       # new last page: clone the previous last page
        docs.append(docs[-1]); pages.append(f'{prefix}/page/{len(pages)}/index.html'); spans.append(spans[-1])
    for n, (t, p) in enumerate(zip(docs, pages)):
        s, e = block(t, 'id="block-topplus-lite-content"')
        vs, ve = block(t, '<div class="view-content">', s, e)
        chunk = allrows[n * PER_PAGE:(n + 1) * PER_PAGE]
        inner = '<div class="view-content">\n' + '\n'.join('    ' + r for r in chunk) + '\n\n    </div>'
        t = t[:vs] + inner + t[ve:]
        s, e = block(t, 'id="block-topplus-lite-content"')
        pg = block(t, '<nav class="pager"', s, e)
        if pg:
            new_pg = full_pager(prefix, n, total) if pager_kind == 'full' else mini_pager(prefix, n, total)
            t = t[:pg[0]] + new_pg + t[pg[1]:]
        write(p, t)
    print(f'  {prefix}: {len(allrows)} items on {total} pages')


def fix_relative_pagers(prefix):
    """Old pages kept Drupal's relative '?page=N' links; point them at the static pages."""
    for p in listing_pages(prefix):
        t = read(p)
        t2 = re.sub(r'href="\?page=(\d+)"', lambda m: f'href="{page_url(prefix, int(m.group(1)))}"', t)
        if t2 != t: write(p, t2)


# ---------------------------------------------------------------- main
def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    sec, slug, title = cfg['section'], cfg['slug'], cfg['title']
    url = f'/{sec}/{slug}'
    d = datetime.date.fromisoformat(cfg['date'])
    dmy = d.strftime('%d.%m.%Y'); iso = cfg['date'] + 'T09:00:00+00:00'
    t_esc = html.escape(title, quote=True)
    body = open(os.path.join(ROOT, cfg['body_file']), encoding='utf-8').read()
    img, img750 = cfg['image'], cfg['image_750x400']
    from PIL import Image
    iw, ih = Image.open(os.path.join(ROOT, img.lstrip('/'))).size
    nid = 1 + max(int(os.path.basename(x)) for x in glob.glob(os.path.join(ROOT, 'node', '*')) if os.path.basename(x).isdigit())
    if os.path.exists(os.path.join(ROOT, url.lstrip('/'), 'index.html')):
        nid = int(re.search(r'data-history-node-id="(\d+)"', read(url + '/index.html')).group(1))

    # 1. article page, cloned from the newest article in this section
    sidebar_src = read('index.html')
    first_link = re.search(r'id="block-views-block-yazi-kategorileri-block-1".*?href="(/' + sec + r'/[^"]+)"', sidebar_src, re.S)
    tpl_path = first_link.group(1).rstrip('/') + '/index.html'
    if tpl_path == url + '/index.html':    # re-running: newest is this article; use the second
        tpl_path = re.findall(r'<div id="yazi-blok-baslik"><a href="(/' + sec + r'/[^"]+)"', sidebar_src)[1].rstrip('/') + '/index.html'
    tpl = read(tpl_path)
    old_url = tpl_path[:-len('/index.html')]
    old_title = html.unescape(re.search(r'<meta name="title" content="(.*?) \| Klinik', tpl).group(1))
    s = tpl.find('<article data-history-node-id'); e = span_end(tpl, s)
    art = tpl[s:e]
    art = re.sub(r'data-history-node-id="\d+"', f'data-history-node-id="{nid}"', art, count=1)
    art = art.replace(f'about="/index.php{old_url}"', f'about="/index.php{url}"').replace(f'about="{old_url}"', f'about="{url}"')
    art = re.sub(r'(<span property="schema:dateCreated" content=")[^"]+', r'\g<1>' + iso, art, count=1)
    art = re.sub(r'<div class="month">.*?</div>', f'<div class="month">{MONTHS[d.month - 1]}</div>', art, count=1)
    art = re.sub(r'<div class="day">.*?</div>', f'<div class="day">{d.day}</div>', art, count=1)
    art = re.sub(r'<div class="year">.*?</div>', f'<div class="year">{d.year}</div>', art, count=1)
    art = re.sub(r'(<span property="schema:name" content=")[^"]*', r'\g<1>' + t_esc, art, count=1)
    art = re.sub(r'(<div class="field field--name-field-one-cikan-gorsel[^>]*>\s*<img src=")[^"]+(" width=")\d+(" height=")\d+',
                 lambda m: f'{m.group(1)}{img}{m.group(2)}{iw}{m.group(3)}{ih}', art, count=1)
    share = urllib.parse.quote(f'https://klinikfarmakoloji.com{url}', safe='')
    art = re.sub(r'<span class="a2a_kit.*?</span>',
                 f'<span class="a2a_kit a2a_kit_size_32 addtoany_list" data-a2a-url="https://klinikfarmakoloji.com{url}" data-a2a-title="{t_esc}">'
                 f'<a class="a2a_dd addtoany_share" href="https://www.addtoany.com/share#url={share}&amp;title={urllib.parse.quote(title)}"></a>'
                 '<a class="a2a_button_facebook"></a><a class="a2a_button_twitter"></a><a class="a2a_button_whatsapp"></a></span>', art, count=1, flags=re.S)
    bs = art.find('<div property="schema:text"'); be = span_end(art, bs)
    art = art[:bs] + art[bs:art.find('>', bs) + 1] + body + '</div>' + art[be:]
    page = tpl[:s] + art + tpl[e:]
    oe = html.escape(old_title, quote=True)
    page = page.replace(f'<meta name="title" content="{oe} | Klinik Farmakoloji Dosyası" />', f'<meta name="title" content="{t_esc} | Klinik Farmakoloji Dosyası" />')
    page = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{html.escape(cfg.get("summary") or title, quote=True)}" />', page, count=1)
    page = re.sub(r'<title>.*?</title>', f'<title>{t_esc} | Klinik Farmakoloji Dosyası</title>', page, count=1, flags=re.S)
    page = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />', page, count=1)
    page = re.sub(r'(<h1 class="title page-title"><span[^>]*>).*?(</span>)', lambda m: m.group(1) + t_esc + m.group(2), page, count=1, flags=re.S)
    page = re.sub(r'(<li class="breadcrumb__item">(?:(?!</li>).)*?<span>)' + re.escape(oe) + r'(</span>)',
                  lambda m: m.group(1) + t_esc + m.group(2), page, count=1, flags=re.S)
    write(url + '/index.html', page)
    print('article page:', url, 'node', nid, '(template', old_url + ')')

    # 2a. section list (/aci-ilac/) – image cards
    card = f'''<div class="views-row"><div class="views-field views-field-nid"><span class="field-content"><div id="yazi-sayfa">
<div id="yazi-sayfa-gorsel">  <a href="{url}" hreflang="tr"><img src="{img750}" width="750" height="400" alt="" title="{t_esc}" typeof="Image" class="image-style-manset-resim-stili-750x400" />
</a>
</div>
<div id="yazi-sayfa-yazi">
<div id="yazi-sayfa-tarih">{dmy}</div>
<div id="yazi-sayfa-baslik"><a href="{url}" hreflang="tr">{t_esc}</a></div>
</div>
</div></span></div></div>'''
    fix_relative_pagers(sec)
    relist(sec, card, 'full')

    # 2b. taxonomy list (/aci-ilac-0/) – teaser articles
    tax = f'{sec}-0'
    if os.path.exists(os.path.join(ROOT, tax, 'index.html')):
        t = read(f'{tax}/index.html')
        s, e = block(t, 'id="block-topplus-lite-content"')
        vs, ve = block(t, '<div class="view-content">', s, e)
        teaser = rows_in(t, vs, ve)[0]
        o_url = re.search(r'<h2 class="node__title">\s*<a href="([^"]+)"', teaser).group(1)
        o_title = re.search(r'<span property="schema:name" content="([^"]*)"', teaser).group(1)
        tz = teaser.replace(o_url, url).replace(o_title, t_esc)
        tz = re.sub(r'data-history-node-id="\d+"', f'data-history-node-id="{nid}"', tz, count=1)
        tz = re.sub(r'(<span property="schema:dateCreated" content=")[^"]+', r'\g<1>' + iso, tz, count=1)
        tz = re.sub(r'<div class="month">.*?</div>', f'<div class="month">{MONTHS[d.month - 1]}</div>', tz, count=1)
        tz = re.sub(r'<div class="day">.*?</div>', f'<div class="day">{d.day}</div>', tz, count=1)
        tz = re.sub(r'<div class="year">.*?</div>', f'<div class="year">{d.year}</div>', tz, count=1)
        bs = tz.find('<div property="schema:text"'); be = span_end(tz, bs)
        summ = html.escape(cfg.get('summary') or title)
        tz = tz[:bs] + tz[bs:tz.find('>', bs) + 1] + f'<p>{summ}</p>' + '</div>' + tz[be:]
        tz = re.sub(r'<span class="a2a_kit.*?</span>',
                    f'<span class="a2a_kit a2a_kit_size_32 addtoany_list" data-a2a-url="https://klinikfarmakoloji.com{url}" data-a2a-title="{t_esc}">'
                    f'<a class="a2a_dd addtoany_share" href="https://www.addtoany.com/share#url={share}&amp;title={urllib.parse.quote(title)}"></a>'
                    '<a class="a2a_button_facebook"></a><a class="a2a_button_twitter"></a><a class="a2a_button_whatsapp"></a></span>', tz, count=1, flags=re.S)
        relist(tax, tz, 'mini')

    # 3. homepage slider: new first slide, keep 5
    t = read('index.html')
    s, e = block(t, 'id="block-views-block-manset-block-1"')
    sl = block(t, '<div id="slick-views-manset-block-1-1-slider"', s, e)
    inner_s = t.find('>', sl[0]) + 1; inner_e = sl[1] - len('</div>')
    slides = []; i = inner_s
    while True:
        j = t.find('<div class="slick__slide slide slide--', i, inner_e)
        if j < 0: break
        k = span_end(t, j); slides.append(t[j:k]); i = k
    if url not in slides[0]:
        new = slides[0]
        o_href = re.search(r'<div id="manset-gorsel"><a href="([^"]+)"', new).group(1)
        new = new.replace(o_href, url)
        new = re.sub(r'<img src="[^"]+"', f'<img src="{img750}"', new, count=1)
        new = re.sub(r'(<div id="manset-terim"><a href=")[^"]*(">)[^<]*', lambda m: f'{m.group(1)}/{tax}{m.group(2)}{SECTION_NAMES.get(sec, sec)}', new, count=1)
        new = re.sub(r'(<div id="manset-baslik"><a href="[^"]*" hreflang="tr">)[^<]*', lambda m: m.group(1) + t_esc, new, count=1)
        slides = [new] + slides[:4]
        slides = [re.sub(r'^<div class="slick__slide slide slide--\d+"', f'<div class="slick__slide slide slide--{n}"', x) for n, x in enumerate(slides)]
        t = t[:inner_s] + ''.join(slides) + t[inner_e:]
        write('index.html', t); print('  homepage slider updated')

    # 4. sidebar box for this section on every page
    box_ids = {'aci-ilac': 'block-views-block-yazi-kategorileri-block-1'}
    box_id = box_ids.get(sec)
    newrow = f'''<div class="views-row"><div class="views-field views-field-nid"><span class="field-content"><div id="yazi-blok-yazi">
<div id="yazi-blok-tarih">{dmy}</div>
<div id="yazi-blok-baslik"><a href="{url}" hreflang="tr">{t_esc}</a></div>
</div></span></div></div>'''
    changed = 0
    if box_id is None:
        # find the sidebar box whose "Tümünü gör" link points to this section
        m = re.search(r'id="(block-views-block-yazi-kategorileri-block-\d+)"(?:(?!id="block-).)*?<div class="more-link"><a href="/' + sec + '">', sidebar_src, re.S)
        box_id = m.group(1) if m else None
    if box_id:
        for fp in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
            rel = os.path.relpath(fp, ROOT)
            if rel.startswith(('index.php/', 'node/')): continue
            t = open(fp, encoding='utf-8').read()
            b = block(t, f'id="{box_id}"')
            if not b: continue
            vc = block(t, '<div class="view-content">', b[0], b[1])
            if not vc: continue
            rs = rows_in(t, *vc)
            if rs and url in rs[0]: continue
            rs = [newrow] + [r for r in rs if url not in r][:4]
            t = t[:vc[0]] + '<div class="view-content">\n          ' + '\n    '.join(rs) + '\n    </div>' + t[vc[1]:]
            open(fp, 'w', encoding='utf-8').write(t); changed += 1
    print(f'  sidebar box updated on {changed} pages')

    # 5. redirects + sitemap
    def redirect(target):
        te = html.escape(target, quote=True)
        return (f'<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><title>Yönlendiriliyor…</title>'
                f'<link rel="canonical" href="{te}"><meta http-equiv="refresh" content="0; url={te}"></head>'
                f'<body><p><a href="{te}">{te}</a></p></body></html>')
    write(f'/index.php{url}/index.html', redirect(url + '/'))
    write(f'/node/{nid}/index.html', redirect(url + '/'))
    sm = read('sitemap.xml'); loc = f'<url><loc>https://klinikfarmakoloji.com{urllib.parse.quote(url + "/")}</loc></url>'
    if loc not in sm: write('sitemap.xml', sm.replace('</urlset>', loc + '\n</urlset>'))
    # 6. link-preview tags (Facebook / X / LinkedIn / WhatsApp) for the new and updated pages
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import clean_articles; clean_articles.main([url.lstrip('/') + '/index.html'])
    import social_meta; social_meta.main()
    import like_button; like_button.main()
    import analytics; analytics.main()
    import language_switch; language_switch.main()
    import search; search.main()
    print('done')


if __name__ == '__main__':
    main(sys.argv[1])
