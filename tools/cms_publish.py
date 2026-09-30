#!/usr/bin/env python3
"""Publish articles written in the Pages CMS editor (content/yazilar/*.md).

Runs automatically on GitHub (.github/workflows/yayinla.yml) whenever an article
is saved. For every new or changed article it:
  * gives it a permanent address  /<bölüm>/<başlıktan-türetilen-ad>
  * makes the 750x400 list picture from the main image
  * takes the text from the editor (or, if the editor is empty, from the Word file)
  * adds the attached documents at the end ("Ekler")
  * runs tools/publish_article.py (article page, lists, homepage, sidebar,
    search, translation flags, share previews, like button, reader counter, SEO)
  * if the title or picture of an already published article changed, updates
    them everywhere they are listed
State (which file became which address) is kept in content/.yayinlanan.json.
Usage: python3 tools/cms_publish.py            (only changed articles)
       python3 tools/cms_publish.py --all      (re-publish every article)
"""
import os, re, sys, json, html, glob, hashlib, datetime, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
STATE = os.path.join(ROOT, 'content', '.yayinlanan.json')
SECTIONS = {'aci-ilac', 'haber', 'editorden', 'bilimsel-yazilar', 'konuk-yazar', 'sektoru-taniyalim'}
TR = str.maketrans({'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u', 'â': 'a', 'î': 'i', 'û': 'u',
                    'Ç': 'c', 'Ğ': 'g', 'I': 'i', 'İ': 'i', 'Ö': 'o', 'Ş': 's', 'Ü': 'u', 'Â': 'a', 'Î': 'i', 'Û': 'u'})


def slugify(s):
    s = s.translate(TR).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    if len(s) > 80: s = s[:80].rsplit('-', 1)[0]
    return s or 'yazi'


def parse(path):
    import yaml
    t = open(path, encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', t, re.S)
    if not m: return None, t
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def local(p):
    p = urllib.parse.unquote(str(p or '').strip())
    p = re.sub(r'^https?://[^/]+', '', p)
    return os.path.join(ROOT, p.lstrip('/')), '/' + p.lstrip('/')


def human_size(n):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB': return (f'{n:.0f} {unit}' if unit == 'B' else f'{n:.1f} {unit}').replace('.', ',')
        n /= 1024


def make_750(src_web):
    """750x400 centre-cropped copy in Drupal's image-style folder (used by lists and the slider)."""
    from PIL import Image
    src, web = local(src_web)
    rel = web.split('/sites/default/files/', 1)[1]
    out_web = '/sites/default/files/styles/manset_resim_stili_750x400/public/' + rel
    out = os.path.join(ROOT, out_web.lstrip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = Image.open(src)
    if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
    w, h = im.size; target = 750 / 400
    if w / h > target:
        nw = int(h * target); box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = int(w / target); box = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
    im.crop(box).resize((750, 400), Image.LANCZOS).save(out)
    return web, out_web


def body_html(meta, body):
    text = re.sub(r'<[^>]+>|&nbsp;|\s', '', body or '')
    if not text and meta.get('word_dosyasi'):
        import docx_to_body
        path, _ = local(meta['word_dosyasi'])
        return docx_to_body.convert(path)
    return body or ''


def attachments(meta):
    files = meta.get('ekler') or []
    if isinstance(files, str): files = [files]
    items = []
    for f in files:
        path, web = local(f)
        if not os.path.exists(path): continue
        name = os.path.basename(web)
        items.append(f'<li><a href="{html.escape(urllib.parse.quote(web), quote=True)}" target="_blank" rel="noopener">{html.escape(name)}</a> '
                     f'<span class="kfd-ek-boyut">({human_size(os.path.getsize(path))})</span></li>')
    if not items: return ''
    return ('<div class="kfd-ekler" style="margin:1.5em 0 0;padding:.8em 1em;border:1px solid #d0c5b3;background:#faf6ee">'
            '<p style="margin:0 0 .4em;font-weight:bold;color:#651320">Ekler</p>'
            '<ul style="margin:0 0 0 1.2em;padding:0">' + ''.join(items) + '</ul></div>')


def summary_of(meta, body):
    if meta.get('ozet'): return re.sub(r'\s+', ' ', str(meta['ozet'])).strip()
    t = html.unescape(re.sub(r'<[^>]+>', ' ', body)); t = re.sub(r'\s+', ' ', t).strip()
    return (t[:197].rsplit(' ', 1)[0] + '…') if len(t) > 200 else t


def replace_everywhere(pairs):
    """After a title or picture change: update every page that lists the article."""
    pairs = [(a, b) for a, b in pairs if a and b and a != b]
    if not pairs: return
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', '.git/', 'pagefind/')): continue
        t = open(fp, encoding='utf-8').read(); t2 = t
        for a, b in pairs: t2 = t2.replace(a, b)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
    print(f'  updated title/picture on {n} pages')


def main(all_=False):
    state = json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}
    todo = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'content', 'yazilar', '*.md'))):
        key = os.path.basename(path)
        digest = hashlib.sha1(open(path, 'rb').read()).hexdigest()
        if not all_ and state.get(key, {}).get('hash') == digest: continue
        todo.append((key, path, digest))
    if not todo:
        print('nothing to publish'); return
    import publish_article
    for key, path, digest in todo:
        meta, body = parse(path)
        if not meta or not meta.get('baslik'):
            print(f'{key}: no title, skipped'); continue
        prev = state.get(key, {})
        title = re.sub(r'\s+', ' ', str(meta['baslik'])).strip()
        sec = prev.get('section') or str(meta.get('bolum') or '').strip()
        if sec not in SECTIONS:
            print(f'{key}: unknown section {sec!r}, skipped'); continue
        if prev.get('section') and meta.get('bolum') and meta['bolum'] != prev['section']:
            print(f'{key}: section can not change after publishing; kept {prev["section"]}')
        slug = prev.get('slug')
        if not slug:
            base = slugify(title); slug = base; i = 2
            while os.path.exists(os.path.join(ROOT, sec, slug, 'index.html')):
                slug = f'{base}-{i}'; i += 1
        date = str(meta.get('tarih') or datetime.date.today().isoformat())[:10]
        if not meta.get('gorsel'):
            print(f'{key}: no main picture, skipped'); continue
        img, img750 = make_750(meta['gorsel'])
        body = body_html(meta, body) + attachments(meta)
        os.makedirs(os.path.join(ROOT, 'tools', 'articles'), exist_ok=True)
        bf = f'tools/articles/{slug}.body.html'
        open(os.path.join(ROOT, bf), 'w', encoding='utf-8').write(body)
        cfg = {'section': sec, 'slug': slug, 'title': title, 'date': date, 'image': img, 'image_750x400': img750,
               'body_file': bf, 'summary': summary_of(meta, body), 'source': f'content/yazilar/{key}'}
        cp = os.path.join(ROOT, 'tools', 'articles', f'{slug}.json')
        json.dump(cfg, open(cp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'== {key} -> /{sec}/{slug}')
        publish_article.main(cp)
        if prev.get('title') or prev.get('image_750x400'):
            oe, ne = html.escape(prev.get('title', ''), quote=True), html.escape(title, quote=True)
            replace_everywhere([(f'>{oe}</a>', f'>{ne}</a>') if prev.get('title') else ('', ''),
                                (f'title="{oe}"', f'title="{ne}"') if prev.get('title') else ('', ''),
                                (prev.get('image_750x400', ''), img750)])
        state[key] = {'hash': digest, 'section': sec, 'slug': slug, 'title': title, 'image_750x400': img750,
                      'url': f'/{sec}/{slug}'}
        json.dump(state, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('done')


if __name__ == '__main__':
    main('--all' in sys.argv)
