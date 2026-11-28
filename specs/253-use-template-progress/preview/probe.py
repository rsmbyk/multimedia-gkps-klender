"""Playwright probe for the spec 253 static preview. Run with the repo venv python."""
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = Path(__file__).resolve().parent / 'index.html'


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000},
                                color_scheme='dark', device_scale_factor=1)
        errors = []
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(150)

        def slots():
            return page.locator('.g-row--slot[data-set="true"]').count()

        def storage():
            return page.evaluate("""() => {
                const o = {};
                for (let i = 0; i < sessionStorage.length; i++) {
                    const k = sessionStorage.key(i);
                    if (k.startsWith('gkps:generate:')) o[k] = JSON.parse(sessionStorage.getItem(k));
                }
                return o;
            }""")

        results = []
        results.append(('A opens empty', slots() == 0))
        page.locator('[data-slot-action]').first.click()
        results.append(('Set settles one slot', slots() == 1))
        results.append(('continuous save wrote a keyed record',
                        'gkps:generate:101' in storage()))
        page.locator('[data-generate-close]').click()
        layer = page.locator('[data-generate-leave]')
        results.append(('dirty Cancel shows the confirm', layer.is_visible()))
        text = layer.inner_text()
        results.append(('confirm says saved + resumed',
                        'saved in this browser session' in text and 'pick up where you left off' in text))
        box = layer.locator('.editor__confirm').bounding_box()
        page.locator('[data-leave-stay]').click()
        results.append(('Stay keeps the modal and the slot',
                        page.locator('#generateModal').is_visible() and slots() == 1))
        page.locator('[data-generate-close]').click()
        page.locator('[data-leave-accept]').click()
        results.append(('Leave closes without discarding',
                        not page.locator('#generateModal').is_visible()
                        and slots() == 1 and 'gkps:generate:101' in storage()))
        page.reload()
        page.wait_for_timeout(150)
        results.append(('reload restores template A', slots() == 1))
        page.locator('[data-open="202"]').click()
        results.append(('template B is independent', slots() == 0))
        page.locator('[data-open="101"]').click()
        page.locator('[data-slot-action]').first.click()
        page.keyboard.press('Escape')
        results.append(('Esc on a dirty modal shows the confirm', layer.is_visible()))

        for name, ok in results:
            print(('PASS  ' if ok else 'FAIL  ') + name)
        print(f'confirm card box: {box}')
        print('console errors:', errors)
        browser.close()
        assert all(ok for _, ok in results), 'probe failed'
        assert not errors, 'console errors'


if __name__ == '__main__':
    main()
