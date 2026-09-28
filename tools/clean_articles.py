#!/usr/bin/env python3
"""Clean the body of article pages: remove pasted-in Word formatting and apply one journal style.

What changes (markup only; the words never change):
  * fonts, font sizes, line heights, margins and Word classes are removed from the article text
  * runs of spaces / non-breaking spaces become one space; empty paragraphs are removed
  * two or more line breaks inside a paragraph become separate paragraphs
  * bold/italic/underline set through styles become real <b>/<i>/<u>
  * headings are normalised (h3/h4); a leading title repeat, the byline and the reference list get classes
  * the page links /sites/default/files/kfd-makale.css, which holds the typography
Safety: the text of every article (all whitespace ignored), its links and its images are compared
before and after; an article that differs in any of these is left untouched and reported.

Usage:
  python3 tools/clean_articles.py --all              # clean every article in place
  python3 tools/clean_articles.py --preview a b ...  # write cleaned copies to /onizleme/<path>/
  python3 tools/clean_articles.py path/to/index.html # clean the given pages in place
"""
import os, re, sys, glob, html
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_HREF = '/sites/default/files/kfd-makale.css'
CSS_LINK = f'<link rel="stylesheet" media="all" href="{CSS_HREF}" />'
TAG = re.compile(r'<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>')
BLOCKS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'blockquote', 'figure', 'pre', 'hr'}
KEEP_ATTR = {'a': {'href', 'target', 'rel', 'title', 'name', 'id'}, 'img': {'src', 'alt', 'width', 'height', 'title'},
             'td': {'colspan', 'rowspan'}, 'th': {'colspan', 'rowspan'}, 'ol': {'start', 'type'},
             'iframe': {'src', 'width', 'height', 'allowfullscreen', 'frameborder', 'title'}, 'source': {'src', 'type'},
             'video': {'src', 'controls', 'width', 'height'}}
REF_HEAD = re.compile(r'^\s*(kaynaklar|kaynakça|kaynak|referanslar|references|literatür|sources)\s*:?\s*$', re.I)
MEDIA = ('img', 'iframe', 'video', 'table', 'hr', 'object', 'embed', 'audio')

def span_end(t, s):
    name = TAG.match(t, s).group(2).lower(); d = 0
    for m in TAG.finditer(t, s):
        if m.group(2).lower() != name or m.group(3): continue
        d += -1 if m.group(1) else 1
        if d == 0: return m.end()
    raise ValueError('unbalanced')

def body_span(t):
    a = t.find('<article data-history-node-id')
    if a < 0 or 'node--view-mode-full' not in t[a:a + 400]: return None
    b = t.find('property="schema:text"', a)
    if b < 0: return None
    s = t.rfind('<div', 0, b); e = span_end(t, s)
    inner_s = t.find('>', s) + 1; inner_e = e - len('</div>')
    return inner_s, inner_e

def plain(x): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', x)).replace('\xa0', ' '))
def links(x): return sorted(re.findall(r'<a\b[^>]*href="([^"]*)"', x))
def imgs(x): return sorted(re.findall(r'<img\b[^>]*src="([^"]*)"', x))

def has_content(el):
    if el.find(MEDIA): return True
    return bool(re.sub(r'[\s\xa0]+', '', el.get_text()))

def clean_style(el, soup):
    st = (el.get('style') or '').lower()
    wraps = []
    if re.search(r'font-weight\s*:\s*(bold|[6-9]00)', st) and el.name not in ('b', 'strong'): wraps.append('b')
    if re.search(r'font-style\s*:\s*italic', st) and el.name not in ('i', 'em'): wraps.append('i')
    if re.search(r'text-decoration[^;]*underline', st) and el.name != 'u' and el.name != 'a': wraps.append('u')
    center = re.search(r'text-align\s*:\s*center', st) or (el.get('align') or '').lower() == 'center'
    keep = KEEP_ATTR.get(el.name, set())
    for at in list(el.attrs):
        if at not in keep: del el[at]
    if center and el.name in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'td', 'th'):
        el['class'] = ['kfd-center']
    if wraps and el.name not in BLOCKS and el.name not in ('img', 'br'):
        inner = el
        for w in wraps:
            new = soup.new_tag(w)
            for c in list(inner.contents): new.append(c.extract())
            inner.append(new)
    elif wraps and el.name in ('p', 'div', 'li', 'td', 'th'):
        new = soup.new_tag(wraps[0])
        for c in list(el.contents): new.append(c.extract())
        el.append(new)

def split_brs(soup):
    """<p>a<br><br>b</p>  ->  <p>a</p><p>b</p>"""
    for p in list(soup.find_all(['p', 'div'])):
        if p.find(BLOCKS - {'p'}): continue
        h = p.decode_contents()
        parts = re.split(r'(?:\s*<br\s*/?>\s*(?:&nbsp;|\xa0|\s)*){2,}', h)
        if len(parts) < 2: continue
        frag = ''.join(f'<p>{x}</p>' for x in parts)
        new = BeautifulSoup(frag, 'html.parser')
        p.replace_with(new)

def normalise_text(soup):
    for s in list(soup.find_all(string=True)):
        if isinstance(s, Comment): s.extract(); continue
        if s.parent and s.parent.name in ('pre', 'script', 'style'): continue
        t = str(s).replace('\xa0', ' ')
        t = re.sub(r'[ \t\r\n\f   ]+', ' ', t)
        if t != str(s): s.replace_with(t)

def strip_edges(soup):
    """Trim leading/trailing spaces inside blocks and drop spaces around <br>."""
    for b in soup.find_all(['p', 'li', 'h3', 'h4', 'td', 'th', 'div']):
        first = next((c for c in b.descendants if isinstance(c, NavigableString)), None)
        if first is not None: first.replace_with(str(first).lstrip())
        last = None
        for c in b.descendants:
            if isinstance(c, NavigableString): last = c
        if last is not None: last.replace_with(str(last).rstrip())
    for br in soup.find_all('br'):
        # remove a <br> that ends a block
        nxt = br.next_sibling
        while isinstance(nxt, NavigableString) and not nxt.strip(): nxt = nxt.next_sibling
        if nxt is None and br.parent and br.parent.name in ('p', 'li', 'td', 'th', 'h3', 'h4', 'div'): br.extract()

def clean_body(inner, title):
    soup = BeautifulSoup(inner, 'html.parser')
    for bad in soup.find_all(['style', 'script', 'meta', 'link', 'xml', 'o:p', 'font']):
        if bad.name == 'font': bad.unwrap()
        elif bad.name == 'o:p': bad.unwrap()
        else: bad.decompose()
    for c in soup.find_all(string=lambda x: isinstance(x, Comment)): c.extract()
    for el in list(soup.find_all(True)): clean_style(el, soup)
    # headings
    for h in soup.find_all(['h1', 'h2']): h.name = 'h3'
    for h in soup.find_all(['h5', 'h6']): h.name = 'h4'
    # spans without attributes are noise
    for sp in list(soup.find_all('span')):
        if not sp.attrs: sp.unwrap()
    # divs that only hold inline content act as paragraphs
    for d in list(soup.find_all('div')):
        if not d.find(BLOCKS): d.name = 'p'
        else: d.unwrap()
    # merge nested identical inline tags (<b><b>x</b></b>)
    for tag in ('b', 'strong', 'i', 'em', 'u'):
        for el in list(soup.find_all(tag)):
            if el.parent is not None and el.parent.name == tag: el.unwrap()
    normalise_text(soup)
    split_brs(soup)
    soup = BeautifulSoup(str(soup), 'html.parser')
    normalise_text(soup)
    strip_edges(soup)
    # empty blocks and empty inline wrappers
    for _ in range(3):
        for el in list(soup.find_all(['p', 'h3', 'h4', 'li', 'b', 'strong', 'i', 'em', 'u', 'span', 'blockquote'])):
            if not has_content(el) and not el.find('br'):
                if el.name == 'li' and el.parent and len(el.parent.find_all('li', recursive=False)) == 1: el.parent.decompose(); continue
                el.decompose()
        for p in list(soup.find_all('p')):   # a paragraph holding only <br>s
            if not has_content(p): p.decompose()
    for ul in soup.find_all(['ul', 'ol']):
        if not ul.find('li'): ul.decompose()
    # roles: title repeat, byline, sub-headings, references
    blocks = [b for b in soup.find_all(['p', 'h3', 'h4', 'ul', 'ol', 'table', 'blockquote'], recursive=False)]
    tnorm = re.sub(r'\W+', '', title.lower())
    for i, b in enumerate(blocks[:4]):
        txt = b.get_text(' ', strip=True)
        if b.name in ('p', 'h3', 'h4') and tnorm and re.sub(r'\W+', '', txt.lower()) == tnorm:
            b.name = 'p'; b['class'] = ['kfd-title']
        elif b.name == 'p' and len(txt) < 80 and re.search(r'Tulunay|Prof\.?\s*Dr', txt) and not re.search(r'[.!?]$', txt.replace('Dr.', 'Dr')):
            b['class'] = ['kfd-byline']
    # a first bold line directly followed by the byline is the article's own title
    if len(blocks) > 1 and blocks[0].name in ('p','h3','h4') and 'kfd-byline' in (blocks[1].get('class') or []) and not blocks[0].get('class'):
        blocks[0].name = 'p'; blocks[0]['class'] = ['kfd-title']
    in_refs = False
    for b in blocks:
        txt = b.get_text(' ', strip=True)
        if REF_HEAD.match(txt):
            b.name = 'p'; b['class'] = ['kfd-refs-head']; in_refs = True; continue
        if in_refs:
            if b.name in ('h3', 'h4'): in_refs = False; continue
            if b.name in ('ol', 'ul'): b['class'] = ['kfd-refs']
            elif b.name == 'p': b['class'] = (b.get('class') or []) + ['kfd-ref']
            continue
        if b.name == 'p' and not b.get('class') and re.match(r'^[•·▪●◦■□►▸\-–]\s', txt):
            b['class'] = ['kfd-bullet']; continue
        if b.name == 'p' and not b.get('class'):
            kids = [c for c in b.contents if not (isinstance(c, NavigableString) and not c.strip())]
            if (len(kids) == 1 and getattr(kids[0], 'name', None) in ('b', 'strong') and 3 <= len(txt) <= 120
                    and not re.search(r'[.:,;]$', txt)):
                b['class'] = ['kfd-sub']
    out = str(soup)
    out = re.sub(r'\n{3,}', '\n\n', out).strip()
    return out

def clean_page(t):
    sp = body_span(t)
    if not sp: return t, 'no-body'
    s, e = sp
    inner = t[s:e]
    m = re.search(r'<h1 class="title page-title">(?:<span[^>]*>)?(.*?)(?:</span>)?\s*</h1>', t, re.S)
    title = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    new = clean_body(inner, title)
    if plain(new) != plain(inner): return t, 'text-mismatch'
    if links(new) != links(inner): return t, 'link-mismatch'
    if imgs(new) != imgs(inner): return t, 'image-mismatch'
    t2 = t[:s] + new + t[e:]
    if CSS_HREF not in t2:
        t2 = t2.replace('</head>', CSS_LINK + '\n</head>', 1)
    return t2, 'ok'

def article_pages():
    for fp in sorted(glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', 'onizleme/', '.git/')): continue
        yield fp

def main(argv):
    import collections
    res = collections.Counter(); problems = []
    if argv and argv[0] == '--preview':
        for rel in argv[1:]:
            rel = rel.strip('/'); fp = os.path.join(ROOT, rel, 'index.html')
            t = open(fp, encoding='utf-8').read()
            t2, r = clean_page(t)
            t2 = t2.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow" />', 1)
            banner = (f'<div style="background:#651320;color:#fff;font:15px/1.4 Georgia,serif;padding:10px 16px;text-align:center">'
                      f'Önizleme: temizlenmiş biçim. <a style="color:#fff;text-decoration:underline" href="/{rel}/">Şu anki hâli için tıklayın</a></div>')
            t2 = re.sub(r'(<body[^>]*>)', r'\1' + banner, t2, count=1)
            out = os.path.join(ROOT, 'onizleme', rel, 'index.html'); os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(t2); print(rel, r)
        return
    targets = list(article_pages()) if argv and argv[0] == '--all' else [os.path.join(ROOT, a) for a in argv]
    for fp in targets:
        t = open(fp, encoding='utf-8').read()
        t2, r = clean_page(t)
        res[r] += 1
        if r not in ('ok', 'no-body'): problems.append((os.path.relpath(fp, ROOT), r))
        if r == 'ok' and t2 != t: open(fp, 'w', encoding='utf-8').write(t2)
    print(dict(res))
    for p in problems: print('  left untouched:', *p)

if __name__ == '__main__':
    main(sys.argv[1:])
