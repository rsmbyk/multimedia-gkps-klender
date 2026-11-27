"""Manual-step record for gate 2: own-tile toggle, cross-section switch, direct load."""
import json
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8769'


def state(page):
    return page.evaluate("""() => ({
      section: document.documentElement.dataset.section,
      nav: document.documentElement.dataset.nav,
      read: document.documentElement.dataset.read,
      stage: (document.querySelector('#read') || {}).dataset?.kind || null,
      books: document.querySelectorAll('#panelBody .book').length
    })""")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900}, color_scheme='dark')
    requests = []
    page.on('request', lambda r: requests.append(r.url))
    page.goto(BASE + '/media-library/')
    direct = state(page)
    page.locator('.rail [data-panel="alkitab"]').click()
    page.wait_for_timeout(400)
    opened = state(page)
    page.locator('.rail [data-panel="alkitab"]').click()
    page.wait_for_timeout(400)
    toggled = state(page)
    page.locator('.rail [data-panel="tatib"]').click()
    page.wait_for_timeout(400)
    tatib = state(page)
    print(json.dumps({'directLoad': direct, 'alkitabOpened': opened,
                      'ownTileToggled': toggled, 'tatibSwitch': tatib,
                      'fetched': [u for u in requests if u.endswith(('/bible/', '/tatib/'))]},
                     indent=2))
    browser.close()
