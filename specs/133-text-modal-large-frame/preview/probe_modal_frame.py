"""Spec 133 preview probe — the frame each create modal is drawn in.

Opens one Tata Ibadah service and measures, for `+ Text`, `+ Media` and (when a
selector is given) an existing text entry's `Edit`:

  * the dialog's own box and computed width/height/max-height,
  * the content padding, the title band (box, padding, font-size, divider),
  * the form's display/flex, every top-level field with its margin,
  * the textarea's box and flex, the actions row and the Save/Cancel buttons.

Two JSON blocks are printed — the modals at three viewports and the same two
create modals in both themes — plus one screenshot per modal per theme.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/133-text-modal-large-frame/preview/probe_modal_frame.py \
        [base-url] [out-prefix] [service-path] [edit-selector]

Defaults: base `http://127.0.0.1:8768` (this worktree's runserver), prefix
`/tmp/tatib-133`, the first service on `/tatib/`, and no edit measurement.
"""
import json
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8768').rstrip('/')
OUT = sys.argv[2] if len(sys.argv) > 2 else '/tmp/tatib-133'
SERVICE = sys.argv[3] if len(sys.argv) > 3 else None
EDIT = sys.argv[4] if len(sys.argv) > 4 else None
EDIT_SERVICE = sys.argv[5] if len(sys.argv) > 5 else None

LINK = """() => {
  const link = [...document.querySelectorAll('a[href^="/tatib/"]')]
    .find(a => /^\\/tatib\\/\\d+\\/$/.test(a.getAttribute('href') || ''));
  return link ? link.getAttribute('href') : null;
}"""

READ = """(label) => {
  const dialog = document.querySelector('#editorModal');
  const box = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1),
            bottom: +(r.bottom).toFixed(1)};
  };
  const cs = (el, ...props) => {
    if (!el) return null;
    const s = getComputedStyle(el);
    return Object.fromEntries(props.map((p) => [p, s.getPropertyValue(p)]));
  };
  const fields = [...dialog.querySelectorAll('.editor__form > .editor__field, .editor__form > .editor__row')];
  return {
    label,
    title: (dialog.querySelector('#editorTitle') || {}).textContent,
    dialog: box(dialog),
    dialogStyle: cs(dialog, 'width', 'height', 'max-height', 'padding'),
    content: box(dialog.querySelector('#editorContent')),
    contentStyle: cs(dialog.querySelector('#editorContent'), 'padding', 'overflow-y'),
    titleBox: box(dialog.querySelector('.editor__title')),
    titleStyle: cs(dialog.querySelector('.editor__title'), 'padding', 'font-size',
                    'border-bottom-width', 'margin'),
    form: box(dialog.querySelector('.editor__form')),
    formStyle: cs(dialog.querySelector('.editor__form'), 'display', 'flex-direction', 'flex'),
    screenMode: box(dialog.querySelector('.editor__screen-mode-wrap')),
    fields: fields.map((el) => ({box: box(el), margin: cs(el, 'margin').margin,
                                 flex: cs(el, 'flex', 'display', 'flex-direction')})),
    textarea: box(dialog.querySelector('textarea')),
    textareaStyle: cs(dialog.querySelector('textarea'), 'height', 'flex', 'min-height'),
    actions: box(dialog.querySelector('.editor__actions')),
    actionsStyle: cs(dialog.querySelector('.editor__actions'), 'margin', 'border-top-width', 'padding'),
    save: box(dialog.querySelector('.editor__save')),
    cancel: box(dialog.querySelector('.editor__cancel')),
    viewport: {w: window.innerWidth, h: window.innerHeight},
    pageScroll: {document: document.documentElement.scrollHeight, viewport: window.innerHeight},
  };
}"""


def open_modals(page, kind):
    """Click the tile, and click again if the page had not wired its handler yet."""
    selector = f'[data-entry-open="{kind}"]'
    for attempt in range(4):
        page.wait_for_timeout(400)
        try:
            if attempt % 2 == 0:
                page.locator(selector).first.click(force=True)
            else:
                # narrow viewports keep the stage tile off-canvas; a DOM click still
                # reaches the delegated handler and is what the layout is measured on
                page.eval_on_selector(selector, 'el => el.click()')
        except Exception:                              # noqa: BLE001
            pass
        try:
            page.wait_for_selector('#editorModal[open]', state='visible', timeout=3000)
            break
        except Exception:                              # noqa: BLE001
            continue
    page.wait_for_selector('#editorModal[open]', state='visible')
    page.wait_for_function(
        "() => { const t = document.querySelector('#editorTitle');"
        " return t && t.textContent.trim().toLowerCase().startsWith('new '); }")
    page.wait_for_timeout(350)          # the open animation settles
    return page.evaluate(READ, f'new-{kind}')


def open_edit(page, selector):
    """The Edit control on a filled stage sits behind a hover, so reveal it first."""
    control = page.locator(selector).first
    control.hover()
    try:
        control.click(timeout=4000)
    except Exception:                                  # noqa: BLE001
        page.eval_on_selector(selector, 'el => el.click()')
    page.wait_for_selector('#editorModal[open]', state='visible')
    page.wait_for_function(
        "() => { const t = document.querySelector('#editorTitle');"
        " return t && t.textContent.trim().toLowerCase().startsWith('edit '); }")
    page.wait_for_timeout(350)
    return page.evaluate(READ, 'edit-text')


def close(page):
    page.keyboard.press('Escape')
    page.wait_for_selector('#editorModal[open]', state='detached')
    page.wait_for_timeout(120)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        result = {'base': BASE, 'sizes': {}, 'themes': {}, 'edit': None}

        # ---- three viewports, light theme ------------------------------------
        for width, height in ((1440, 900), (1280, 800), (390, 844)):
            page = browser.new_page(viewport={'width': width, 'height': height})
            page.goto(f'{BASE}/tatib/')
            service = SERVICE or page.evaluate(LINK)
            page.goto(f'{BASE}{service}')
            page.wait_for_selector('[data-entry-open="text"]', state='attached')
            result['service'] = service
            key = f'{width}x{height}'
            result['sizes'][key] = {}
            for kind in ('text', 'media'):
                print(f'... {key} {kind}', file=sys.stderr, flush=True)
                result['sizes'][key][kind] = open_modals(page, kind)
                if width == 1440:
                    page.screenshot(path=f'{OUT}-{kind}-light.png')
                close(page)
            page.close()

        # ---- both themes at 1440x900 ----------------------------------------
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'{BASE}{result["service"]}')
        page.wait_for_selector('[data-entry-open="text"]', state='attached')
        for theme in ('dark',):
            page.evaluate("(t) => document.documentElement.dataset.theme = t", theme)
            page.wait_for_timeout(120)
            for kind in ('text', 'media'):
                result['themes'][f'{kind}-{theme}'] = open_modals(page, kind)
                page.screenshot(path=f'{OUT}-{kind}-{theme}.png')
                close(page)

        # ---- the form still works: mode switch, Save guard, no page scroll ----
        page.goto(f'{BASE}{result["service"]}')
        page.wait_for_selector('[data-entry-open="text"]', state='attached')
        open_modals(page, 'text')
        result['behaviour'] = page.evaluate("""() => {
          const d = document.querySelector('#editorModal');
          const read = () => ({
            mode: d.querySelector('[name="default_screen_mode"]').value,
            selected: d.querySelector('[data-create-screen-mode]').dataset.selected,
            help: d.querySelector('[data-create-mode-help]').textContent.trim(),
            saveDisabled: d.querySelector('.editor__save').disabled,
          });
          const before = read();
          d.querySelector('[data-create-mode="single_screen"]').click();
          const afterMode = read();
          const area = d.querySelector('textarea');
          area.value = 'Salam sejahtera bagi kita semua';
          area.dispatchEvent(new Event('input', {bubbles: true}));
          const afterType = read();
          area.value = '';
          area.dispatchEvent(new Event('input', {bubbles: true}));
          return {before, afterMode, afterType, afterClear: read(),
                  scrolls: document.documentElement.scrollHeight > window.innerHeight,
                  dialogScroll: d.scrollHeight > d.clientHeight};
        }""")
        page.screenshot(path=f'{OUT}-text-mode-single.png')
        close(page)

        # ---- a short viewport keeps the frame inside the window --------------
        page.set_viewport_size({'width': 1280, 'height': 600})
        page.goto(f'{BASE}{result["service"]}')
        page.wait_for_selector('[data-entry-open="text"]', state='attached')
        result['short'] = open_modals(page, 'text')
        page.screenshot(path=f'{OUT}-text-1280x600.png')
        close(page)

        # ---- a narrow viewport, for the presentation -------------------------
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(f'{BASE}{result["service"]}')
        page.wait_for_selector('[data-entry-open="text"]', state='attached')
        open_modals(page, 'text')
        page.screenshot(path=f'{OUT}-text-390x844.png')
        close(page)

        # ---- the edit form stays as it was ----------------------------------
        if EDIT:
            page.set_viewport_size({'width': 1440, 'height': 900})
            page.goto(f'{BASE}{EDIT_SERVICE or result["service"]}')
            page.wait_for_selector(EDIT, state='attached')
            page.evaluate("() => document.documentElement.dataset.theme = 'light'")
            result['edit'] = open_edit(page, EDIT)
            page.screenshot(path=f'{OUT}-edit-text-light.png')
            close(page)
        browser.close()

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
