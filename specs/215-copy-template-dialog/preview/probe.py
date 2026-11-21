"""Measures the preview: every number the spec's `## UI/UX` cites comes from here.

    .venv/bin/python specs/215-copy-template-dialog/preview/probe.py

Writes `shots/` (gitignored) and prints one JSON object per state.
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
URL = (HERE / 'index.html').as_uri()
SHOTS = HERE / 'shots'

MEASURE = """
() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return [+b.x.toFixed(1), +b.y.toFixed(1), +b.width.toFixed(1), +b.height.toFixed(1)]; };
  const s = (el, ...props) => { if (!el) return null; const cs = getComputedStyle(el);
    return Object.fromEntries(props.map(p => [p, cs.getPropertyValue(p)])); };
  const dialog = document.querySelector('.pv__dialog');
  const stage = document.querySelector('.pv__stage');
  const layer = document.querySelector('[data-copy-confirm]');
  const card = layer.querySelector('.confirm--dialog');
  const input = layer.querySelector('[data-copy-name]');
  const facts = [...layer.querySelectorAll('.confirm__facts li')];
  return {
    // the stage stands in for the window: `contain: layout` makes it the layer's
    // containing block, so "the layer is the window" is measurable on this page
    window: r(stage),
    dialog: r(dialog),
    layer: r(layer), layerStyle: s(layer, 'position', 'display', 'background-color', 'padding', 'border-top-left-radius'),
    card: r(card), cardStyle: s(card, 'width', 'padding', 'border-radius', 'background-color', 'box-shadow'),
    heading: r(card.querySelector('h3')), headingStyle: s(card.querySelector('h3'), 'font'),
    lead: r(card.querySelector('.confirm__lead')), leadStyle: s(card.querySelector('.confirm__lead'), 'font', 'color'),
    label: r(card.querySelector('.editor__field label')),
    input: r(input), inputStyle: s(input, 'font', 'background-color', 'border-top-color'),
    inputValue: input.value,
    facts: r(card.querySelector('.confirm__facts')),
    factRows: facts.map(r),
    factStyle: s(facts[0], 'font', 'color'),
    actions: r(card.querySelector('.editor__confirm-actions')),
    buttons: [...card.querySelectorAll('.editor__confirm-actions button')].map(b => ({
      label: b.textContent.trim(), box: r(b), right: +b.getBoundingClientRect().right.toFixed(1) })),
    acceptDisabled: layer.querySelector('[data-copy-accept]').disabled,
    focus: document.activeElement && document.activeElement.textContent.trim().slice(0, 24),
    // the Edit dialog must stay legible behind the layer, not be erased by it
    behindSample: (() => { const b = document.querySelector('[data-fragment]:not([hidden]) .editor__title');
      return b ? { title: b.textContent.trim(), box: r(b) } : null; })(),
  };
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 960, 'height': 780}, device_scale_factor=1)
    page.on('pageerror', lambda e: print('PAGEERROR', e))
    page.goto(URL)
    page.wait_for_timeout(400)
    SHOTS.mkdir(exist_ok=True)

    for scheme in ('dark', 'light'):
        if page.evaluate('() => document.documentElement.dataset.theme') != scheme:
            page.click('[data-theme-toggle]')
            page.wait_for_timeout(200)

        for size in ('service', 'template'):
            if size == 'template':
                page.click('[data-size-toggle]')
                page.wait_for_timeout(250)

            before = page.evaluate("() => document.querySelector('.pv__dialog').getBoundingClientRect().height")
            page.click(f'[data-fragment="{size}"] [data-copy-open]')
            page.wait_for_timeout(400)
            data = page.evaluate(MEASURE)
            data['state'] = f'{scheme}/{size}/open'
            data['dialogHeightBefore'] = round(before, 1)
            print(json.dumps(data))
            page.screenshot(path=str(SHOTS / f'{size}-{scheme}-open.png'))

            page.click('[data-copy-name]')
            page.wait_for_timeout(200)
            print(json.dumps({'state': f'{scheme}/{size}/clicked', 'selection': page.evaluate(
                "() => { const i = document.querySelector('[data-copy-name]');"
                " return [i.selectionStart, i.selectionEnd, i.value.length]; }")}))
            page.screenshot(path=str(SHOTS / f'{size}-{scheme}-selected.png'))

            page.fill('[data-copy-name]', '   ')
            page.wait_for_timeout(120)
            print(json.dumps({'state': f'{scheme}/{size}/blank', 'acceptDisabled': page.evaluate(
                "() => document.querySelector('[data-copy-accept]').disabled")}))
            page.fill('[data-copy-name]', '9 Agustus 2026 (Copy)')

            page.keyboard.press('Escape')
            page.wait_for_timeout(200)
            print(json.dumps({'state': f'{scheme}/{size}/closed', 'hidden': page.evaluate(
                "() => document.querySelector('[data-copy-confirm]').hidden"),
                'dialogHeight': round(page.evaluate(
                    "() => document.querySelector('.pv__dialog').getBoundingClientRect().height"), 1)}))

            if size == 'template':
                page.click('[data-size-toggle]')
                page.wait_for_timeout(250)
    browser.close()
