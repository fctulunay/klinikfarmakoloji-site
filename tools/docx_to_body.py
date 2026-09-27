#!/usr/bin/env python3
"""Convert an article .docx into body HTML styled like existing klinikfarmakoloji.com articles.

Usage: python3 tools/docx_to_body.py article.docx out.body.html
Needs pandoc and beautifulsoup4.
Conventions (matching the Word drafts):
  * first paragraph = title, a paragraph with the author's name = byline
  * short bold paragraphs, or paragraphs like "2. Başlık" / "Sonuç", are section headings
  * paragraphs starting with "•" are bullet points
  * "Kaynakça"/"Kaynaklar" starts the numbered reference list
  * a last italic paragraph mentioning "AI desteği" becomes the grey note
"""
import re, sys, html, subprocess
from bs4 import BeautifulSoup, NavigableString

F = 'font-family:Georgia,serif'
def wrap_text(inner, size='12.0pt', color='black'):
    return f'<span style="font-size:11pt"><span style="text-autospace:none"><span style="{F}"><span style="font-size:{size}"><span style="color:{color}">{inner}</span></span></span></span></span>'

def P_title(x): return f'<p style="margin-bottom:11px"><span style="font-size:11pt"><span style="text-autospace:none"><span style="{F}"><b><span style="font-size:18.0pt"><span style="color:#651320">{x}</span></span></b></span></span></span></p>'
def P_author(x): return f'<p style="margin-bottom:25px"><span style="font-size:11pt"><span style="text-autospace:none"><span style="{F}"><b><span style="font-size:16.0pt"><span style="color:black">{x}</span></span></b></span></span></span></p>'
def P_head(x): return f'<p style="margin-top:21px; margin-bottom:14px"><span style="font-size:11pt"><span style="text-autospace:none"><span style="{F}"><b><span style="font-size:13.0pt"><span style="color:#651320">{x}</span></span></b></span></span></span></p>'
def P_sub(x): return f'<p style="margin-top:14px; margin-bottom:10px"><span style="font-size:11pt"><span style="text-autospace:none"><span style="{F}"><b><span style="font-size:12.0pt"><span style="color:#651320">{x}</span></span></b></span></span></span></p>'
def P_text(x): return f'<p style="margin-bottom:14px; text-align:justify"><span style="font-size:11pt"><span style="line-height:19.5pt"><span style="text-autospace:none"><span style="{F}"><span style="font-size:12.0pt"><span style="color:black">{x}</span></span></span></span></span></span></p>'
def P_formula(x): return f'<p style="margin:10px 0 16px; text-align:center">{wrap_text("<i>" + x + "</i>", "13.0pt")}</p>'
def P_caption(x): return f'<p style="margin-top:6px; margin-bottom:18px">{wrap_text("<i>" + x + "</i>", "10.0pt", "#555555")}</p>'
def P_bullet(x): return f'<p style="margin-bottom:7px; margin-left:50px; text-indent:-18.9pt"><span style="font-size:11pt"><span style="line-height:18.3pt"><span style="text-autospace:none"><span style="{F}"><span style="font-size:12.0pt"><span style="color:black">•</span></span>&nbsp;&nbsp;&nbsp;&nbsp; <span style="font-size:12.0pt"><span style="color:black">{x}</span></span></span></span></span></span></p>'
def H_refs(x): return f'<h1 style="margin-top:21px; margin-bottom:11px"><span style="font-size:14pt"><span style="{F}"><span style="color:#7a1f2b"><span style="font-size:12.0pt">{x}</span></span></span></span></h1>'
def LI_ref(x): return f'\t<li style="margin-bottom:4px"><span style="font-size:11pt"><span style="{F}"><i><span style="font-size:10.0pt">{x}</span></i></span></span></li>'
def P_note(x): return f'<p style="margin-top:16px"><span style="font-size:11pt"><span style="{F}"><i><span style="font-size:10.0pt"><span style="color:#555555">{x}</span></span></i></span></span></p>'

SUBSCRIPTS = [(r'μtest', 'μ<sub>test</sub>'), (r'μreferans', 'μ<sub>referans</sub>'), (r'σWR', 'σ<sub>WR</sub>')]

def inner(el):
    """Inner HTML of a pandoc element: keep b/strong/i/em/a/sub/sup, drop <u>, collapse whitespace."""
    out = []
    for c in el.children:
        if isinstance(c, NavigableString): out.append(html.escape(str(c), quote=False))
        elif c.name in ('strong', 'b'): out.append('<b>' + inner(c) + '</b>')
        elif c.name in ('em', 'i'): out.append('<i>' + inner(c) + '</i>')
        elif c.name in ('sub', 'sup'): out.append(f'<{c.name}>' + inner(c) + f'</{c.name}>')
        elif c.name == 'a': out.append(f'<a href="{html.escape(c.get("href", ""), quote=True)}" target="_blank" rel="noopener">' + inner(c) + '</a>')
        elif c.name == 'br': out.append('<br />')
        else: out.append(inner(c))
    return re.sub(r'\s+', ' ', ''.join(out)).strip()

def plain(el): return re.sub(r'\s+', ' ', el.get_text()).strip()

def is_heading(el, txt):
    only_bold = el.name == 'p' and len(el.contents) == 1 and getattr(el.contents[0], 'name', None) in ('strong', 'b')
    numbered = re.match(r'^\d+(\.\d+)*\.\s+\S', txt) and len(txt) < 110 and not txt.endswith('.')
    return (only_bold and len(txt) < 140) or numbered or txt in ('Sonuç', 'Giriş', 'Kaynakça', 'Kaynaklar')

def convert(docx):
    h = subprocess.run(['pandoc', docx, '-t', 'html', '--wrap=none'], capture_output=True, text=True, check=True).stdout
    soup = BeautifulSoup(h, 'html.parser')
    els = [e for e in soup.children if getattr(e, 'name', None)]
    out = []; refs = []; in_refs = False; first = True
    for el in els:
        if el.name == 'blockquote':
            for p in el.find_all('p'):
                x = re.sub(r'^•\s*', '', inner(p))
                out.append(P_bullet(x))
            continue
        if el.name == 'table':
            rows = []
            for n, tr in enumerate(el.find_all('tr')):
                tds = tr.find_all(['td', 'th']); cells = []
                for k, td in enumerate(tds):
                    bg = ' background:#efd9dc;' if k == 0 else (' background:#f5eee0;' if n % 2 else '')
                    txt = inner(td)
                    txt = f'<b><span style="color:#651320">{txt}</span></b>' if k == 0 else txt
                    cells.append(f'\t\t\t<td style="border:solid #d0c5b3 1.0pt;{bg} padding:4px 7px" valign="top"><p style="margin:0; text-align:left">{wrap_text(txt, "11.0pt")}</p></td>')
                rows.append('\t\t<tr>\n' + '\n'.join(cells) + '\n\t\t</tr>')
            out.append('<table class="Table" style="border-collapse:collapse; border:solid #d0c5b3 1.0pt; width:100%">\n\t<tbody>\n' + '\n'.join(rows) + '\n\t</tbody>\n</table>')
            continue
        if el.name in ('ol', 'ul'):
            for li in el.find_all('li'):
                (refs if in_refs else out).append(LI_ref(inner(li)) if in_refs else P_bullet(inner(li)))
            continue
        txt = plain(el)
        if not txt: continue
        x = inner(el)
        for a, b in SUBSCRIPTS: x = x.replace(a, b)
        if first:
            out.append(P_title(re.sub(r'</?b>', '', x))); first = False; continue
        if re.fullmatch(r'Prof\.? ?Dr\.?.*Tulunay', txt, re.I):
            out.append(P_author(re.sub(r'</?b>', '', x))); continue
        if txt in ('Kaynakça', 'Kaynaklar'):
            in_refs = True; out.append(H_refs(txt)); continue
        if in_refs:
            if 'AI desteği' in txt:
                out.append('<ol>\n' + '\n'.join(refs) + '\n</ol>'); refs = []
                out.append(P_note('Not: ' + re.sub(r'</?i>', '', x) if not txt.startswith('Not') else re.sub(r'</?i>', '', x))); in_refs = False
            else:
                refs.append(LI_ref(re.sub(r'^\s*(<i>)?\s*\d+\.\s*', r'\1', x).replace('<i>', '').replace('</i>', '')))
            continue
        if re.match(r'^Tablo \d+\.', txt): out.append(P_caption(x)); continue
        if re.match(r'^[^.]{1,40}\s(=|≈)\s', txt) and len(txt) < 80 and not txt.endswith('.'): out.append(P_formula(x)); continue
        if is_heading(el, txt):
            clean = re.sub(r'</?b>', '', x)
            out.append(P_sub(clean) if re.match(r'^\d+\.\d+\.', txt) else P_head(clean)); continue
        out.append(P_text(x))
    if refs: out.append('<ol>\n' + '\n'.join(refs) + '\n</ol>')
    return '\n'.join(out)

if __name__ == '__main__':
    open(sys.argv[2], 'w', encoding='utf-8').write(convert(sys.argv[1]))
    print('wrote', sys.argv[2])
