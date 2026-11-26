#!/usr/bin/env python3
"""Drive the three option previews and print measured pending-state values."""
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def probe(page, option, which):
    name = 'combined' if option == 'd' else 'option-' + option
    page.goto((HERE / f'{name}.html').as_uri())
    page.wait_for_load_state('load')
    page.get_by_role('button', name='Slow 1.2s').click()
    tile_id = '#railSearch' if which.startswith('search') else '#railMediaLibrary'
    if which == 'search-home':
        page.locator('[data-search-dest="home"]').click()
    page.locator('#pvMediaBtn' if which == 'media' else '#pvSearchBtn').click()
    page.wait_for_timeout(90)
    got = page.evaluate("""(which) => {
      const tile = document.getElementById(which.startsWith('search') ? 'railSearch' : 'railMediaLibrary');
      const stage = document.querySelector('.stage');
      const bars = ['pvStagebar', 'pvWindowBar'].map(id => {
        const el = document.getElementById(id);
        const r = el.getBoundingClientRect();
        return {id, hidden: el.hidden, height: getComputedStyle(el).height,
                topMinusStage: Math.round(r.top - stage.getBoundingClientRect().top)};
      });
      const ph = ['pvPh-search', 'pvPh-search-home', 'pvPh-media']
        .filter(id => !document.getElementById(id).hidden);
      return {
        option: document.documentElement.dataset.option,
        svgOpacity: getComputedStyle(tile.querySelector('svg')).opacity,
        ariaDisabled: tile.getAttribute('aria-disabled'),
        stageBusy: stage.getAttribute('aria-busy'),
        bars,
        placeholders: ph,
        readout: document.getElementById('pvReadout').textContent,
        status: document.getElementById('pvStatus').textContent
      };
    }""", which)
    print(option, which, got)
    page.screenshot(path=str(HERE / f'shots/option-{option}-{which}-pending.png'))
    page.wait_for_timeout(1400)
    landed = page.evaluate("""() => {
      const node = document.querySelector('#pvLanded .search-results__intro, #pvLanded .media-library__intro, #pvLanded .search-home__input');
      return {
        landedHidden: document.getElementById('pvLanded').hidden,
        heading: node ? (node.value || node.textContent) : '(none)',
        status: document.getElementById('pvStatus').textContent
      };
    }""")
    print(option, which, 'settled', landed)


def main():
    (HERE / 'shots').mkdir(exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome',
                                    args=['--no-sandbox', '--allow-file-access-from-files'])
        page = browser.new_page(viewport={'width': 1440, 'height': 900},
                                color_scheme='dark', device_scale_factor=1)
        page.on('pageerror', lambda e: errors.append(str(e)))
        for option in ['d', 'a', 'b', 'c']:
            for which in ['search', 'search-home', 'media']:
                probe(page, option, which)
        browser.close()
    print('page errors:', errors)


if __name__ == '__main__':
    main()
