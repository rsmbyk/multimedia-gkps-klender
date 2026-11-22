"""Build the static preview for spec 214 from the project's real materials.

Reads the product's own tokens.css and the .songrow/.toc rules from components.css,
and clones the row markup from reading/_toc.html. The only new CSS is the mark column
itself, which is what the slice proposes. Run from anywhere:

    python specs/214-sidebar-entry-kind-marks/preview/build_preview.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
TOKENS = ROOT / 'static/styles/design/tokens.css'
COMPONENTS = ROOT / 'static/styles/design/components.css'


def tokens_css():
    return TOKENS.read_text(encoding='utf-8')


def row_css():
    """The live rules a contents row uses, verbatim from components.css."""
    text = COMPONENTS.read_text(encoding='utf-8')
    blocks = []
    for selector in (
        '#panelBody li, #chList li',
        '.songrow {',
        '.songrow:hover',
        '#chList li:hover > .songrow',
        '.songrow[aria-current="true"]',
        '.songrow__c {',
        '.songrow[aria-current="true"] .songrow__c',
        '.songrow__t {',
        '.songrow__t--song:has',
        '.songrow__t--song {',
        '.songrow__heading',
        '.songrow__reference',
        '.songrow__title',
        '.songrow__verses {',
        '.songrow[aria-current="true"] .songrow__verses',
        ':root[data-theme="dark"] .songrow__verses',
        ':root[data-section="tatib"]',
        '.toc__eos',
        '.toc__eosline',
    ):
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.strip().startswith(selector):
                # a rule ends at its own closing brace, on this line or a later one
                end = index
                while end < len(lines) and '}' not in lines[end]:
                    end += 1
                block = '\n'.join(lines[index:end + 1])
                if block not in blocks:
                    blocks.append(block)
                break
    return '\n\n'.join(blocks)


# The four corner-badge glyphs from reading/_slot_kind_badge.html (spec 213), on the
# same 12-unit grid the product uses. The badge names the kind the slot resolves to.
BADGES = {
    'scripture': '<path d="M6 4.8c-.8-.65-1.9-.95-3.45-.85v5.2c1.55-.1 2.65.2 3.45.85.8-.65 1.9-.95 3.45-.85V3.95c-1.55-.1-2.65.2-3.45.85z"/><path d="M6 4.8v5.2"/>',
    'song': '<path d="M4.5 8.7V2.8l5.1-1v5.8"/><circle cx="3.35" cy="8.7" r="1.2"/><circle cx="8.45" cy="7.6" r="1.2"/>',
    'media': '<rect x="1.6" y="2.6" width="8.8" height="6.8" rx="1.2"/><path d="M5.1 4.7v2.6l2.2-1.3z"/>',
    'text': '<path d="M2.4 3.4h7.2M2.4 6h7.2M2.4 8.6h4.3"/>',
}


def badge(kind):
    return (f'<span class="slot__badge" aria-hidden="true" data-kind-badge="{kind}">'
            f'<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{BADGES[kind]}</svg></span>')


GLYPHS = {
    'text': '<path d="M3 4.5h14M3 8h14M3 11.5h9"/>',
    'scripture': ('<path d="M12 9.6c-1.6-1.3-3.8-1.9-6.9-1.7v10.4c3.1-.2 5.3.4 6.9 1.7 1.6-1.3 3.8-1.9 6.9-1.7V7.9c-3.1-.2-5.3.4-6.9 1.7z"/>'
                  '<path d="M12 9.6v10.4"/><path d="M12 2.6v4.6M10.1 4.5h3.8"/>'),
    'song': ('<path d="M9 17.4V5.6l10.2-2v11.6"/><circle cx="6.7" cy="17.4" r="2.4"/>'
             '<circle cx="16.9" cy="15.2" r="2.4"/>'),
    'media': '<rect x="3" y="4.5" width="18" height="15" rx="2.4"/><path d="M10 9v6l5-3z"/>',
    'fill_in': '<rect x="2.6" y="2.6" width="14.8" height="14.8" rx="3.6" stroke-dasharray="2.8 2.4"/><path d="M10 6.8v6.4M6.8 10h6.4"/>',
    'choice': '<rect x="2.6" y="2.6" width="14.8" height="14.8" rx="3.6" stroke-dasharray="2.8 2.4"/><circle cx="10" cy="10" r="3.6"/><circle cx="10" cy="10" r="1.5" fill="currentColor" stroke="none"/>',
    'break': '<path d="M12 4l8 8-8 8-8-8z"/>',
}


def mark(kind, badge_kind=None):
    slot = kind in ('fill_in', 'choice')
    viewbox = '0 0 20 20' if slot else '0 0 24 24'
    cls = 'songrow__mark songrow__mark--slot' if slot else 'songrow__mark'
    return (f'<span class="{cls}" aria-hidden="true" data-mark="{kind}">'
            f'<svg viewBox="{viewbox}" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{GLYPHS[kind]}</svg>'
            f'{badge(badge_kind) if slot and badge_kind else ""}'
            f'</span>')


ROWS = [
    ('text', '1', 'L : Marilah kita bangkit berdiri! Di dalam nama Allah Bapa, dan Tuhan Yesus Kristus, serta Roh Kudus, yang bersama kita semua. Amin.'),
    ('scripture', '2', 'Kisah Para Rasul 1:1'),
    ('song', '3', 'HAL 7 — Porini Dong Marribu Hali', 'Bait 1-7'),
    ('media', '4', 'Image · Beauty of the Lord'),
    ('fill_in', '5', 'Fill-in · Song', None, 'song'),
    ('choice', '6', 'Choice · Passage', None, 'scripture'),
    ('break', '7', None),
]


def column(candidate):
    out = []
    for row in ROWS:
        kind, number, label = row[0], row[1], row[2]
        verse = row[3] if len(row) > 3 else None
        badge_kind = row[4] if len(row) > 4 else None
        if kind == 'break':
            out.append(f'<li class="toc__eos" data-num="{number}"><span class="toc__eosline"></span></li>')
            continue
        song = (f'<span class="songrow__t songrow__t--song"><span class="songrow__heading">'
                f'{label}</span><span class="songrow__verses">{verse}</span></span>'
                if verse else f'<span class="songrow__t">{label}</span>')
        out.append(
            f'<li data-num="{number}"><a class="songrow" href="#ti-{number}" data-i="{number}" '
            f'data-num="{number}" data-txt="{label.lower()}">'
            f'<span class="songrow__c">{number}</span>'
            f'{"" if candidate == "0" else mark(kind, badge_kind)}{song}</a></li>')
    return '\n'.join(out)


CSS = """
/* Preview-only scaffolding: a 404px contents pane, like a 1440px window with both
   sidebars open (the width the binding tests measure). */
html, body { height: auto; }
body { display: block; margin: 0; padding: 16px; background: var(--canvas); color: var(--ink);
       font: 16px/1.5 var(--font-sans); }
.preview { display: flex; gap: 28px; align-items: flex-start; }
.pane { width: 404px; }
.pane h2 { font: 600 13px/1.4 var(--font-sans); color: var(--head-ink); margin: 0 0 8px; }
#chList { list-style: none; margin: 0; padding: 0; width: 404px; border: 1px solid var(--divider);
          border-radius: 12px; background: var(--canvas); }
.songrow { align-items: center; }

/* The proposed column. A: the number's own box is untouched; the mark is a new
   16px column after it with the row's existing 10px gap. B: the number's box is
   reduced to 24px and the mark follows at 8px, so the label keeps the old x. */
.songrow__mark { flex: none; width: 16px; height: 16px; display: block; color: var(--head-ink); }
.songrow__mark svg { width: 100%; height: 100%; display: block; }
/* The slot's kind modifier, scaled from spec 213's 13px disc at a 20px mark to
   11px at this 16px mark. The disc paints the row's own face so it does not read
   as a hole on the hover fill. */
.songrow__mark--slot { position: relative; }
.slot__badge { position: absolute; right: -3px; bottom: -2px; width: 11px; height: 11px;
               border-radius: 50%; background: var(--canvas); color: var(--head-ink);
               display: grid; place-items: center; }
.slot__badge svg { width: 8px; height: 8px; }
.songrow:hover .slot__badge { background: var(--icon-hover-bg); }
.pane--A .songrow__mark { margin-left: 0; }
.pane--B .songrow__c { min-width: 24px; }
.pane--B .songrow { gap: 8px; }
.toc__eos { display: flex; align-items: center; padding: 6px 18px; }
.toc__eos .songrow__mark { width: 12px; height: 12px; margin-right: 10px; }
.toc__eosline { flex: 1; border-top: 1px solid var(--divider); }
"""


def page():
    return f"""<!doctype html>
<html lang="id" data-theme="light" data-section="tatib">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Contents kind column — spec 214 preview</title>
<style>{tokens_css()}</style>
<style>{row_css()}</style>
<style>{CSS}</style>
</head>
<body>
<div class="preview">
  <section class="pane pane--0"><h2>0 · today, no column</h2>
    <ul id="chList">{column('0')}</ul></section>
  <section class="pane pane--A"><h2>A · number box unchanged</h2>
    <ul id="chList">{column('A')}</ul></section>
  <section class="pane pane--B"><h2>B · compact number box</h2>
    <ul id="chList">{column('B')}</ul></section>
</div>
</body>
</html>
"""


if __name__ == '__main__':
    (HERE / 'index.html').write_text(page(), encoding='utf-8')
    print(f'wrote {HERE / "index.html"}')
