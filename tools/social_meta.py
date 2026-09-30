#!/usr/bin/env python3
"""Add Open Graph / Twitter card tags (link previews on Facebook, X, LinkedIn, WhatsApp) to every page.

For each article page: title, a short description from the article text, and a 1200x630 share image
(the article's own image fitted on a cream background, so square infographics are not cropped).
Other pages get the site-wide default image. Safe to re-run: existing tags are replaced, and share
images are only generated when missing (use --force to rebuild them).

Usage: python3 tools/social_meta.py [--force]
"""
import os, re, sys, html, glob, hashlib
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://klinikfarmakoloji.com'
SITE_NAME = 'Klinik Farmakoloji Dosyası'
SHARE_DIR = 'sites/default/files/paylasim'
BG = (245, 238, 224)            # cream, as in the site's tables
DEFAULT_IMG = '/sites/default/files/default_images/kfd-default-img.jpg'
FORCE = '--force' in sys.argv

def share_image(src_rel):
    """Return site path of a 1200x630 JPEG built from src_rel (site path)."""
    src = os.path.join(ROOT, src_rel.lstrip('/'))
    if not os.path.isfile(src): return None
    name = re.sub(r'[^a-z0-9.-]+', '-', os.path.splitext(os.path.basename(src_rel))[0].lower())[:80]
    name += '-' + hashlib.md5(src_rel.encode()).hexdigest()[:6] + '.jpg'
    out_rel = f'/{SHARE_DIR}/{name}'; out = os.path.join(ROOT, out_rel.lstrip('/'))
    if os.path.exists(out) and not FORCE: return out_rel
    try:
        im = Image.open(src); im.load()
    except Exception:
        return None
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bgim = Image.new('RGB', im.size, BG); bgim.paste(im, mask=im.split()[-1]); im = bgim
    else:
        im = im.convert('RGB')
    W, H = 1200, 630
    canvas = Image.new('RGB', (W, H), BG)
    s = min((W - 40) / im.width, (H - 30) / im.height)
    if im.width / im.height > 1.6:          # already wide: fill the frame instead
        s = max(W / im.width, H / im.height)
    r = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    canvas.paste(r, ((W - r.width) // 2, (H - r.height) // 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, 'JPEG', quality=85, optimize=True, progressive=True)
    return out_rel

def text_of(fragment):
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', fragment, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

def description(body_html, title):
    for p in re.findall(r'<p\b[^>]*>(.*?)</p>', body_html, re.S):
        t = text_of(p)
        if len(t) < 80 or t.upper() == title.upper() or 'Tulunay' in t[:60]: continue
        if len(t) > 200: t = t[:200].rsplit(' ', 1)[0].rstrip(',;:') + '…'
        return t
    return title

def page_url(rel):
    p = '/' + rel[:-len('index.html')] if rel.endswith('index.html') else '/' + rel
    return SITE + p

def main():
    TAGS = re.compile(r'\n?<meta (?:property="(?:og|article):[^"]+"|name="twitter:[^"]+")[^>]*>')
    n_art = n_other = 0
    for fp in sorted(glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('index.php/', 'node/', 'tools/', '.git/')): continue
        t = open(fp, encoding='utf-8').read()
        if 'http-equiv="refresh"' in t[:600] or '<head>' not in t: continue
        t = TAGS.sub('', t)
        m = re.search(r'<title>(.*?)</title>', t, re.S)
        full_title = html.unescape(m.group(1).strip()) if m else SITE_NAME
        title = re.sub(r'\s*\|\s*Klinik Farmakoloji Dosyası.*$', '', full_title) or SITE_NAME
        art_s = (lambda _m: _m.start() if _m else -1)(re.search(r'<article[^>]*data-history-node-id', t))
        is_article = art_s >= 0 and 'node--view-mode-full' in t[art_s:art_s + 400]
        img = None; desc = SITE_NAME + ': Türkiye Akılcı İlaç Kullanım Platformu'; published = None
        if is_article:
            im = re.search(r'field--name-field-one-cikan-gorsel[^>]*>\s*<img (?:data-pagefind-meta="[^"]*" )?src="([^"]+)"', t[art_s:])
            img = share_image(im.group(1) if im else DEFAULT_IMG)
            b = t.find('property="schema:text"', art_s)
            if b > 0: desc = description(t[b:t.find('</article>', b)], title)
            pd = re.search(r'property="schema:dateCreated" content="([^"]+)"', t[art_s:])
            published = pd.group(1) if pd else None
            n_art += 1
        else:
            img = share_image(DEFAULT_IMG); n_other += 1
        e = lambda s: html.escape(s, quote=True)
        tags = [f'<meta property="og:site_name" content="{SITE_NAME}" />',
                f'<meta property="og:locale" content="tr_TR" />',
                f'<meta property="og:type" content="{"article" if is_article else "website"}" />',
                f'<meta property="og:title" content="{e(title)}" />',
                f'<meta property="og:description" content="{e(desc)}" />',
                f'<meta property="og:url" content="{e(page_url(rel))}" />']
        if img:
            tags += [f'<meta property="og:image" content="{SITE}{img}" />',
                     '<meta property="og:image:width" content="1200" />',
                     '<meta property="og:image:height" content="630" />',
                     f'<meta property="og:image:alt" content="{e(title)}" />']
        if published: tags.append(f'<meta property="article:published_time" content="{published}" />')
        tags += ['<meta name="twitter:card" content="summary_large_image" />',
                 f'<meta name="twitter:title" content="{e(title)}" />',
                 f'<meta name="twitter:description" content="{e(desc)}" />']
        if img: tags.append(f'<meta name="twitter:image" content="{SITE}{img}" />')
        anchor = re.search(r'<meta name="description"[^>]*>|<meta charset="utf-8" />', t)
        pos = anchor.end() if anchor else t.find('<head>') + len('<head>')
        t = t[:pos] + '\n' + '\n'.join(tags) + t[pos:]
        open(fp, 'w', encoding='utf-8').write(t)
    print(f'social tags: {n_art} articles, {n_other} other pages')

if __name__ == '__main__':
    main()
