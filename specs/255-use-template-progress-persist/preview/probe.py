"""Measure the three spec 255 indicator variants in both states."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parent / 'index.html').as_uri()


def read(page):
    return page.evaluate("""() => {
      const out = {};
      for (const v of ['a','b','c']) {
        const btn = document.querySelector('[data-example="' + v + '"] [data-generate-open]');
        const dot = btn.querySelector('.pv-dot');
        const b = btn.getBoundingClientRect();
        const d = dot.getBoundingClientRect();
        out[v] = {
          w: +b.width.toFixed(1), h: +b.height.toFixed(1),
          dotW: +d.width.toFixed(1), dotH: +d.height.toFixed(1),
          dotLeft: +(d.left - b.left).toFixed(1), dotTop: +(d.top - b.top).toFixed(1),
          dotVisible: d.width > 0 && getComputedStyle(dot).display !== 'none',
          name: (btn.getAttribute('aria-label') || btn.innerText.trim()).replace(/\\s+/g, ' '),
          text: btn.innerText.trim().replace(/\\s+/g, ' ')
        };
      }
      return out;
    }""")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1000, 'height': 900},
                                color_scheme='dark', device_scale_factor=2)
        errors = []
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(PAGE)
        page.wait_for_timeout(200)
        on = read(page)
        page.screenshot(path=str(Path(__file__).resolve().parent / 'shots' / 'indicators.png'),
                        full_page=True)
        page.click('#toggle')
        page.wait_for_timeout(200)
        off = read(page)
        browser.close()

    print('ON ', json.dumps(on, indent=2))
    print('OFF', json.dumps(off, indent=2))
    print('console errors:', errors)
    for v in 'abc':
        assert on[v]['h'] == 34, (v, 'height', on[v]['h'])
        if v in 'ac':
            assert on[v]['dotVisible'], (v, 'dot not visible when saved')
        else:
            assert not on[v]['dotVisible'], (v, 'B must not carry a dot')
        assert not off[v]['dotVisible'], (v, 'dot visible without a draft')
        assert 'draft saved' in on[v]['name'].lower(), (v, 'accessible name', on[v]['name'])
        assert 'draft saved' not in off[v]['name'].lower(), (v, 'stale name', off[v]['name'])
    assert on['a']['dotW'] == 7 and on['c']['dotW'] == 6
    assert abs(on['a']['w'] - off['a']['w']) < 0.2, 'A must not change width'
    assert on['c']['w'] > off['c']['w'], 'C widens the button by the dot and its gap'
    assert on['b']['w'] > off['b']['w'], 'B did not widen with the suffix'
    assert not errors, errors
    print('PASS all variants measured, both states')


if __name__ == '__main__':
    main()