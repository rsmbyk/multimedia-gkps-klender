"""Gate-1 probe: compare the base app with the slice's live preview.

Both servers are opened through the home page and the rail, never a deep link.
Reads the DOM after each click, so a missing fetch shows as a number, not a timeout.
"""
import json
from playwright.sync_api import sync_playwright

SURFACES = {'base': 'http://127.0.0.1:63404', 'preview': 'http://127.0.0.1:8769'}


def snapshot(page, requests):
    return page.evaluate("""() => ({
      section: document.documentElement.dataset.section,
      stageKind: (document.querySelector('#read') || {}).dataset?.kind || null,
      books: document.querySelectorAll('#panelBody .book').length,
      emptyHidden: document.querySelector('#panelEmpty')?.hidden === true,
      emptyTitle: document.querySelector('#panelEmpty .listempty__title')?.textContent.trim() || ''
    })""") | {'bibleRequests': sum(1 for url in requests if url.endswith('/bible/'))}


def run(playwright, url):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 900},
                                  color_scheme='dark', device_scale_factor=1)
    page = context.new_page()
    requests = []
    page.on('request', lambda request: requests.append(request.url))
    page.goto(url + '/')
    page.locator('#railMediaLibrary').click()
    page.wait_for_function(
        "() => (document.querySelector('#read') || {}).dataset?.kind === 'media-library'")
    media = snapshot(page, requests)
    page.locator('.rail [data-panel="alkitab"]').click()
    page.wait_for_timeout(600)
    first = snapshot(page, requests)
    page.locator('.rail [data-panel="kidung"]').click()
    page.wait_for_timeout(400)
    page.locator('.rail [data-panel="alkitab"]').click()
    page.wait_for_timeout(400)
    second = snapshot(page, requests)
    browser.close()
    return {'media': media, 'firstBibleClick': first, 'afterOtherSection': second}


if __name__ == '__main__':
    with sync_playwright() as playwright:
        print(json.dumps({name: run(playwright, url) for name, url in SURFACES.items()}, indent=2))
