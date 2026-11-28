# Spec 248 manual evidence — a Go To on air must not show the service top pin.
# Usage: check_goto.py [base-url]
import json, sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8793'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 420, 'height': 860},
                            color_scheme='dark', device_scale_factor=1)
    page.goto(BASE + '/obs/dock', wait_until='networkidle')
    page.wait_for_selector('#pickBody .servicerow', timeout=20000)
    page.locator('#pickBody .servicerow').nth(0).click()
    page.wait_for_selector('#dockPanel[data-view="run"] .entryli', timeout=20000)
    page.wait_for_timeout(350)
    # Put a normal service entry on air first.
    page.evaluate("""() => document.querySelector('.entryli[data-index="2"] .entryrow').click()""")
    page.wait_for_timeout(300)
    # Open the Go To band (the operator's G gesture) and search a real song number.
    query = page.evaluate("""() => {
      const rows = [...document.querySelectorAll('.entryli .entryrow')];
      const hit = rows.map(r => r.textContent).map(t => (t.match(/\\d+/) || [])[0])
                      .find(n => n && Number(n) > 0);
      return hit || '1';
    }""")
    page.keyboard.press('g')
    page.wait_for_selector('.bandswap.is-find', timeout=5000)
    page.fill('#findInput', query)
    page.wait_for_timeout(500)
    page.keyboard.press('Enter')
    try:
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }", timeout=6000)
    except Exception:
        print(json.dumps({'query': query, 'goto_started': False,
                          'find_label': page.locator('#findLabel').inner_text()}))
        browser.close()
        sys.exit(1)
    page.evaluate("() => { const b = document.getElementById('runBody'); b.scrollTop = b.scrollHeight; }")
    page.wait_for_timeout(300)
    result = page.evaluate("""() => ({
      goto: !!(JSON.parse(localStorage.getItem('gkps-display') || 'null') || {}).goto,
      topPinHidden: document.querySelector('.topband-slot').hidden,
      offBlockShown: !document.getElementById('offBlock').hidden,
      offStripRows: document.querySelectorAll('#offBody .offrow').length,
      liveHeaderPins: document.querySelectorAll('.entryrow.is-covered').length,
      scrollTop: +document.getElementById('runBody').scrollTop.toFixed(1)
    })""")
    result['query'] = query
    print(json.dumps(result, indent=2))
    browser.close()
