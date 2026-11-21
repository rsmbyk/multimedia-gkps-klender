"""Measure the Copy as template confirmation in the static preview (spec 212).

Run with the repo's own Playwright so a number quoted here and the number an E2E
test asserts come from the same Chromium:

    .venv/bin/python specs/212-copy-confirm-layer/preview/probe.py

Writes shots/ (gitignored) and prints one JSON object with both states: the
candidate CSS on (the proposal) and off (what production serves today).
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / 'shots'

MEASURE = """
() => {
  const box = el => { const b = el.getBoundingClientRect();
    return {x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1)}; };
  const style = (el, props) => { const s = getComputedStyle(el); const out = {};
    props.forEach(p => out[p] = s.getPropertyValue(p)); return out; };
  const modal = document.getElementById('editorModal');
  const layer = modal.querySelector('.editor__confirm-layer');
  const card = modal.querySelector('.editor__confirm');
  const h3 = card.querySelector('h3');
  const p = card.querySelector('p');
  const actions = card.querySelector('.editor__confirm-actions');
  const save = modal.querySelector('.editor__actions .editor__save');
  const saveBox = box(save);
  // What actually paints at the form's Save button, once the confirmation is up.
  const hit = document.elementFromPoint(saveBox.x + saveBox.w / 2, saveBox.y + saveBox.h / 2);
  const buttons = [...actions.querySelectorAll('button')].map(b => ({
    label: b.textContent.trim(), box: box(b), height: getComputedStyle(b).height,
  }));
  return {
    modal: {box: box(modal), radius: getComputedStyle(modal).borderTopLeftRadius},
    layer: {box: box(layer), ...style(layer, ['position', 'display', 'padding', 'background-color',
                                             'z-index', 'border-top-left-radius'])},
    card: {box: box(card), ...style(card, ['width', 'padding', 'border-radius', 'background-color',
                                          'box-shadow', 'display'])},
    heading: {...style(h3, ['font-family', 'font-size', 'font-weight', 'line-height', 'margin']), box: box(h3)},
    body: {...style(p, ['font-family', 'font-size', 'line-height', 'margin']), box: box(p)},
    actions: {box: box(actions), ...style(actions, ['display', 'justify-content', 'gap'])},
    buttons,
    coversForm: hit ? (hit.closest('.editor__confirm-layer') !== null) : null,
    hitElement: hit ? hit.className : null,
    formSaveBox: saveBox,
  };
}
"""


def main():
    SHOTS.mkdir(exist_ok=True)
    url = (HERE / 'index.html').as_uri()
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for state, disabled in (('proposed', False), ('current', True)):
            page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                    device_scale_factor=1, color_scheme='light')
            page.goto(url)
            page.wait_for_load_state('load')
            if disabled:
                page.eval_on_selector('#candidate', 'el => { el.disabled = true; }')
            page.wait_for_timeout(250)   # the dialog's own open animation, if any
            out[state] = page.evaluate(MEASURE)
            page.screenshot(path=str(SHOTS / f'{state}.png'))
            page.close()
        browser.close()
    print(json.dumps(out, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
