"""Spec 135 preview — every row the three-line cap can produce.

Builds `cases.html`: one list at the real panel width (415px) and one at the
narrow width (313px), each holding a row per case, using the project's own
stylesheets, class names and row markup. A caption above each row names the
case; the row itself is exactly what `_toc.html` would draw.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/135-tatib-sidebar-row-clamp/preview/build_cases.py
"""
import html
import pathlib

HERE = pathlib.Path(__file__).parent

PROPOSAL = """
/* --- spec 135: a contents row is three lines, ellipsized --- */
.songrow__t {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  overflow-wrap: anywhere;
  min-width: 0;
}
.songrow__t--lines, .songrow__t--song { display: -webkit-box; }
/* A song that has a Bait line spends at most two lines on its heading, so the
   Bait line is always drawn as the third. No <br> between them: the heading and
   the Bait line are the box's own items. */
.songrow__t--song:has(.songrow__verses) .songrow__heading {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}
"""

FURNITURE = """
/* preview-only: captions and the columns themselves; no product rule is restyled */
body { margin: 0; background: var(--canvas); color: var(--ink); }
.wrap { padding: 28px 32px 64px; }
.lede { max-width: 62rem; margin: 0 0 6px; font: 600 20px/1.35 ui-sans-serif, system-ui, sans-serif; }
.note { max-width: 62rem; margin: 0 0 18px; color: var(--head-ink);
        font: 400 13.5px/1.6 ui-sans-serif, system-ui, sans-serif; }
.bar { display: flex; gap: 10px; margin: 0 0 24px; }
.bar button { font: 600 12.5px/1 ui-sans-serif, system-ui, sans-serif; padding: 8px 12px;
              border: 1px solid var(--divider); border-radius: 8px; background: var(--surface);
              color: var(--ink); cursor: pointer; }
.cols { display: flex; align-items: flex-start; gap: 40px; flex-wrap: wrap; }
.col { width: 415px; }
.col--narrow { width: 313px; }
.col > h2 { margin: 0 0 10px; font: 650 13px/1 ui-sans-serif, system-ui, sans-serif;
            letter-spacing: .08em; text-transform: uppercase; color: var(--head-ink); }
.pane { border: 1px solid var(--divider); border-radius: 12px; background: var(--rail-bg); }
.cap { padding: 10px 10px 4px; color: var(--head-ink);
       font: 500 10.5px/1.4 ui-sans-serif, system-ui, sans-serif;
       letter-spacing: .06em; text-transform: uppercase; }
.cap b { color: var(--ink); font-weight: 650; letter-spacing: 0; text-transform: none; font-size: 11.5px; }
ul.cl { list-style: none; margin: 0; padding: 0 10px 10px; }
#chListN li { position: relative; }
#chListN li:hover > .songrow:not([aria-current="true"]) { background: var(--icon-hover-bg); }
:root[data-section="tatib"] #chListN .songrow__t { padding-right: 30px; }
:root[data-section="tatib"] #chListN .songrow__c { align-self: center; }
#chListN li:hover .toc__grip, #chListN .toc__grip:focus-visible { opacity: 1; }
"""

GRIP = ('<button type="button" class="toc__grip" aria-label="Reorder {n}: drag, or move it with '
        'the arrow keys" title="Drag to reorder"><svg viewBox="0 0 20 20" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">'
        '<path d="M7 5.5h.01M13 5.5h.01M7 10h.01M13 10h.01M7 14.5h.01M13 14.5h.01"/></svg></button>')


def row_plain(num, lines, current=False, untitled=True, grip=True):
    text = '<br>'.join(html.escape(line) if line else '&nbsp;' for line in lines)
    current_attr = ' aria-current="true"' if current else ''
    cont = ' songrow--cont' if untitled else ''
    grip_html = GRIP.format(n=num) if grip else ''
    return (f'<li data-move-row><a class="songrow{cont}" href="#"{current_attr}>'
            f'<span class="songrow__c">{num}</span><span class="songrow__t">{text}</span></a>'
            f'{grip_html}</li>')


def row_song(num, reference, title, bait, current=False):
    ref = f'<span class="songrow__reference">{html.escape(reference)}</span> ' if reference else ''
    bait_html = f'<span class="songrow__verses">{html.escape(bait)}</span>' if bait else ''
    current_attr = ' aria-current="true"' if current else ''
    return (f'<li data-move-row><a class="songrow" href="#"{current_attr}>'
            f'<span class="songrow__c">{num}</span>'
            f'<span class="songrow__t songrow__t--song"><span class="songrow__heading">{ref}'
            f'<span class="songrow__title">{html.escape(title)}</span></span>{bait_html}</span></a>'
            f'{GRIP.format(n=num)}</li>')


def row_eos():
    return ('<li class="toc__eos" aria-hidden="true"><span class="toc__eosline"></span></li>')


COLS = [
    ('Reading sidebar · 415px', 'col', 'chList', [
        ('Song · hymn, one heading line', row_song(1, 'KJ 152', 'Ada Kuasa dalam DarahNya', 'Bait 1-3')),
        ('Song · hymn, heading on two lines', row_song(2, 'HAL 7', 'Porini Dong Marribu Hali Ma Daging', 'Bait 1-9')),
        ('Song · 64-character title, no verse line',
         row_song(3, 'PJ 606', 'Saudara, Mari Kita Menyanyikan Pujian bagi Tuhan yang Setia', '')),
        ('Passage · one line', row_plain(4, ['Kisah Para Rasul 1:1'], untitled=False)),
        ('Passage · longest reference', row_plain(5, ['Kisah Para Rasul 12:1-3'], untitled=False)),
        ('Media · short filename', row_plain(6, ['images.jpeg'], untitled=False)),
        ('Media · long filename',
         row_plain(7, ['Sujud & Terima Kasih - JCC Worship [Official Music Video] - Impact Music Indonesia.mp3'],
                   untitled=False)),
        ('Media · 64-character entry title',
         row_plain(8, ['Perekaman Ibadah Minggu Kedua Setelah Paskah dari Ruang Ibadah Utama'], untitled=False)),
        ('Text · untitled, one body line', row_plain(9, ['Salam sejahtera bagi kita semua'])),
        ('Text · untitled, two body lines',
         row_plain(10, ['L. Di dalam nama Allah Bapa, dan Tuhan Yesus Kristus,', 'serta Roh Kudus.'])),
        ('Text · untitled, three body lines',
         row_plain(11, ['Jemaat menyanyikan bait pertama', 'Liturgis membacakan ayat kedua',
                        'Doa pembuka dipimpin liturgis'])),
        ('Text · untitled, six body lines → three and …',
         row_plain(12, ['Nyanyian Pembuka', 'Jemaat menyanyikan bait pertama bersama-sama',
                        'Liturgis membacakan ayat kedua sebelum doa pembuka\u2026'])),
        ('Text · untitled, blank second line', row_plain(13, ['Keep this', '', 'Skip this'])),
        ('Text · untitled, one unbroken run',
         row_plain(14, ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'])),
        ('Legacy text · untitled, one unbroken link (the 11 Oktober 2026 service, 81 characters)',
         row_plain(20, ['https://drive.google.com/drive/folders/18A0dI3cwJxzSGTxim3ENlj4GwrB2Yatd'])),
        # the same unbroken run in every other kind: the rule is on the label box,
        # so a song heading, a text title, a media title and a legacy title all wrap
        ('Song · 64-character title with no spaces, plus its Bait line',
         row_song(21, 'PJ 606',
                  'SaudaraMariKitaMenyanyikanPujianBagiTuhanYangSetiaDanPenuhKasih',
                  'Bait 1-3')),
        ('Text · titled, 64 characters with no spaces',
         row_plain(22, ['PengakuanImanRasuliDanDoaSyafaatBagiJemaatDanPelayananGereja'],
                   untitled=False)),
        ('Media · 64-character filename with no spaces',
         row_plain(23, ['SujudTerimaKasihJCCWorshipOfficialMusicVideoImpactMusicIndonesia.mp3'],
                   untitled=False)),
        ('Legacy text · titled, 64 characters with no spaces',
         row_plain(24, ['PengakuanImanRasuliDanDoaSyafaatBagiJemaatDanPelayananGereja'],
                   untitled=False)),
        ('Text · untitled, 120 characters with no spaces',
         row_plain(25, ['a' * 120])),
        ('Text · titled, short', row_plain(15, ['VOTUM, INTROITUS, DOA'], untitled=False)),
        ('Text · titled, 64 characters',
         row_plain(16, ['Pengakuan Iman Rasuli dan Doa Syafaat bagi Jemaat dan Pelayanan Gereja'],
                   untitled=False)),
        ('Section break', row_eos()),
        ('Legacy text · untitled, four lines → three and …',
         row_plain(17, ['L. Di dalam nama Allah Bapa, dan Tuhan Yesus Kristus,', 'serta Roh Kudus,',
                        'Pencipta langit dan bumi\u2026'])),
        ('Legacy text · titled', row_plain(18, ['PAMUNGKAHNI'], untitled=False)),
        ('Selected state · three-line row', row_plain(19, ['Nyanyian Pembuka',
                                                          'Jemaat menyanyikan bait pertama bersama-sama',
                                                          'Liturgis membacakan ayat kedua\u2026'], current=True)),
    ]),
    ('Narrow sidebar · 313px', 'col col--narrow', 'chListN', [
        ('Song · heading capped at two lines, Bait line third',
         row_song(1, 'PJ 606', 'Saudara, Mari Kita Menyanyikan Pujian bagi Tuhan yang Setia', 'Bait 1-3')),
        ('Text · 64-character title, three lines',
         row_plain(2, ['Pengakuan Iman Rasuli dan Doa Syafaat bagi Jemaat dan Pelayanan Gereja'],
                   untitled=False)),
        ('Media · long filename wraps to three',
         row_plain(3, ['Sujud & Terima Kasih - JCC Worship [Official Music Video] - Impact Music Indonesia.mp3'],
                   untitled=False)),
        ('Passage · unchanged', row_plain(4, ['Kisah Para Rasul 1:1'], untitled=False)),
        ('Song · unbroken heading, capped at two lines',
         row_song(5, 'PJ 606',
                  'SaudaraMariKitaMenyanyikanPujianBagiTuhanYangSetiaDanPenuhKasih', 'Bait 1-3')),
        ('Media · unbroken filename', row_plain(6, [
            'SujudTerimaKasihJCCWorshipOfficialMusicVideoImpactMusicIndonesia.mp3'], untitled=False)),
        ('Legacy text · unbroken link',
         row_plain(7, ['https://drive.google.com/drive/folders/18A0dI3cwJxzSGTxim3ENlj4GwrB2Yatd'])),
    ]),
]


def build_col(title, cls, list_id, rows):
    body = []
    for caption, markup in rows:
        body.append(f'<li class="cap"><b>{html.escape(caption)}</b></li>')
        body.append(markup)
    return (f'<section class="{cls}"><h2>{html.escape(title)}</h2>'
            f'<div class="pane"><ul class="cl" id="{list_id}">{"".join(body)}</ul></div></section>')


def main():
    cols = '\n'.join(build_col(*col) for col in COLS)
    page = f"""<!doctype html>
<html lang="en" data-theme="light" data-theme-mode="light" data-nav="open" data-ch="open"
      data-read="on" data-home="landing" data-section="tatib" data-ch-mode="chapter">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spec 135 — every row the three-line cap can produce</title>
<link rel="stylesheet" href="../../../static/styles/design/tokens.css">
<link rel="stylesheet" href="../../../static/styles/design/components.css">
<style>{PROPOSAL}{FURNITURE}</style>
</head>
<body>
<div class="wrap">
  <p class="lede">Every row the three-line cap can produce</p>
  <p class="note">The rows below are the project's own: the same classes, the same stylesheets, the
  same markup <code>_toc.html</code> draws. Only the clamp rule is new. Hover a row to see its
  drag handle; the last row is selected. The right column is the same list at the width a 390px
  window gives the panel.</p>
  <div class="bar">
    <button type="button" onclick="document.documentElement.dataset.theme='light'">Light</button>
    <button type="button" onclick="document.documentElement.dataset.theme='dark'">Dark</button>
  </div>
  <div class="cols">
{cols}
  </div>
</div>
</body>
</html>
"""
    (HERE / 'cases.html').write_text(page, encoding='utf-8')
    print(f'wrote {HERE / "cases.html"}')


if __name__ == '__main__':
    main()
