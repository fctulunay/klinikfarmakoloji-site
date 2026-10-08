# Article pictures in 7 languages

Visitors who read the site through the language flags (en, de, es, ru, zh, hi, ja) get the
article text translated by Google, but words inside a picture can not be translated. So every
article picture gets seven companion files next to it:

    sites/default/files/yazi-gorselleri/2026-10/abc.png        Turkish original
    sites/default/files/yazi-gorselleri/2026-10/abc.en.png     English   (also .de .es .ru .zh .hi .ja)

`tools/image_lang.py` finds these files and makes the page swap them in.

## Doing it for a new article

1. `python3 tools/gorsel-kaynak/pending.py` lists pictures (the `cms/` upload folder, and month folders from 2026-10) without language versions.
2. Look at each picture and read its article (`content/yazilar/*.md`).
   - No words in it, a logo, already English or bilingual: add its name to `skip.txt`.
   - The article has an English twin article with its own picture: copy that picture as `<name>.en.png`
     and make cards for the other six languages only.
3. Add a new `batchN.py` (copy the shape of `batch12.py`) and `mapN.json` (card id -> picture path
   without extension). A card is a condensed version: kicker, title, subtitle, optional key numbers,
   3-6 labelled points, one closing message, optional sources. Only title + subtitle gives a poster.
   Use only what the picture and article say; keep numbers exactly; no em dashes.
   The pictures carry no "Prepared with AI support" note (dropped 2026-10-08 at the author's request).
   Card ids must be new (check `grep -l "'<id>'" batch*.py`).
4. Render and place:

       cd tools/gorsel-kaynak
       python3 cards.py batchN        # writes out/<id>.<lang>.png, prints OVERFLOW if text does not fit
       python3 publish.py mapN.json   # copies them next to the originals
       cd ../.. && python3 tools/image_lang.py

   Open a few of the PNGs (always the Hindi, Chinese and Japanese ones) to check nothing is cut off.
5. Commit everything except `tools/gorsel-kaynak/out/` and push to `main`; the site redeploys.

Needs Python `playwright` with Chromium, and the Noto Sans CJK system fonts. The Hindi font is in `fonts/`.
