"""Before/after readouts for spec 240 from the live slice server.

Run with the repository's Python (Playwright installed):
  ~/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/240-entry-modal-title/preview/probe.py

The served worktree keeps the fix. The "before" column is read after injecting a
local override into the browser only; no served file is reverted.
"""
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8790'
SERVICE = '/tatib/149/'

MEASURE = """() => {
  const d = document.getElementById('editorModal');
  const t = d.querySelector('#editorTitle');
  if (!t) return null;
  const r = document.createRange(); r.selectNodeContents(t);
  const tr = r.getBoundingClientRect(), dr = d.getBoundingClientRect();
  const br = t.getBoundingClientRect(), s = getComputedStyle(t);
  return {
    title: t.textContent.trim(),
    frame: [Math.round(dr.width), Math.round(dr.height)],
    textX: +(tr.x - dr.x).toFixed(1), textY: +(tr.y - dr.y).toFixed(1),
    band: +br.height.toFixed(1), padding: s.padding,
    border: s.borderBottomWidth, font: s.fontSize,
    fieldY: +(d.querySelector('.editor__form > .editor__field').getBoundingClientRect().y - dr.y).toFixed(1),
  };
}"""

BROKEN = ('.editor:has([data-editor-size="large"]):not(:has(.editor__head)) '
          '.editor__title { padding: 0 !important; border: 0 !important; }')

CASES = (
    ('New text', '[data-entry-open="text"]'),
    ('New media', '[data-entry-open="media"]'),
    ('Edit text', '[data-entry-edit="21"]'),
)


def read(page, selector):
    page.goto(BASE + SERVICE)
    page.wait_for_load_state('networkidle')
    page.locator(selector).first.evaluate('el => el.click()')
    page.wait_for_function(
        "() => { const t = document.querySelector('#editorTitle');"
        " return t && t.textContent.trim().length > 0"
        " && document.querySelector('#editorContent [data-editor-size=\"large\"]'); }")
    page.wait_for_timeout(350)  # the media dialog's 190ms entrance settles
    after = page.evaluate(MEASURE)
    page.add_style_tag(content=BROKEN)
    before = page.evaluate(MEASURE)
    return before, after


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in ((1440, 900), (390, 844)):
            page = browser.new_page(
                viewport={'width': width, 'height': height},
                color_scheme='dark', device_scale_factor=1)
            print(f'== {width}x{height}, dark ==')
            for label, selector in CASES:
                before, after = read(page, selector)
                print(f'{label:10} before {before}')
                print(f'{"":10} after  {after}')
            page.close()
        browser.close()


if __name__ == '__main__':
    main()
