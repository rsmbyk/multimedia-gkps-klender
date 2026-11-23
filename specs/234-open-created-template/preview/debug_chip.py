"""Debug the template chip in the live editor dialog (spec 234 preview)."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.on('pageerror', lambda e: print('PAGEERROR', str(e)))
    page.goto('http://127.0.0.1:8774/tatib/', wait_until='networkidle')
    page.click('#panelAdd')
    page.wait_for_selector('#editorContent .editor__form')
    print('before:', page.evaluate("""() => {
      const f = document.querySelector('#editorContent .editor__form');
      const g = f.querySelector('[data-tatib-kinds]');
      return {action: f.action, selected: g.dataset.selected,
              kind: f.querySelector('[name=kind]')?.value,
              hidden: f.querySelector('.editor__date-field')?.hidden,
              date: f.querySelector('[name=date]')?.value};
    }"""))
    page.click('#editorContent [data-tatib-kind="1"]')
    page.wait_for_timeout(200)
    print('after click:', page.evaluate("""() => {
      const f = document.querySelector('#editorContent .editor__form');
      const g = f.querySelector('[data-tatib-kinds]');
      return {selected: g.dataset.selected,
              kind: f.querySelector('[name=kind]')?.value,
              hidden: f.querySelector('.editor__date-field')?.hidden,
              date: f.querySelector('[name=date]')?.value,
              pressed: [...g.querySelectorAll('[data-tatib-kind]')].map(b => b.getAttribute('aria-pressed'))};
    }"""))
    browser.close()
