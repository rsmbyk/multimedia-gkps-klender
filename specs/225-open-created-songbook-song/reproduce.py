"""Measure what happens right now after a songbook/song is created."""
import json, time
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8768'
stamp = str(int(time.time()))[-6:]


def state(page):
    return page.evaluate("""() => ({
      path: location.pathname,
      title: document.getElementById('readName')?.textContent || '',
      currentBook: document.querySelector('#panelBody a.book[aria-current="true"]')
        ?.getAttribute('data-name') || null,
      currentSong: document.querySelector('#chList a.songrow[aria-current="true"]')
        ?.getAttribute('href') || document.querySelector('#chList [aria-current="true"]')
        ?.getAttribute('href') || null,
      nav: document.documentElement.dataset.nav,
      ch: document.documentElement.dataset.ch,
      read: document.documentElement.dataset.read,
      marker: window.__gkps225 || null
    })""")


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(BASE + '/songs/')
    page.wait_for_load_state('networkidle')
    page.evaluate("() => { window.__gkps225 = 'alive'; }")
    print('before:', json.dumps(state(page)))

    # --- create a songbook from the panel Add button
    page.click('#panelAdd')
    page.wait_for_selector('#editorContent input[name="name"]')
    book_name = 'Probe Book ' + stamp
    page.fill('#editorContent input[name="name"]', book_name)
    page.click('#editorContent .editor__save')
    page.wait_for_function("!document.querySelector('dialog[open]')")
    page.wait_for_timeout(1000)
    print('after songbook:', json.dumps(state(page)))
    print('book rows:', page.locator('#panelBody a.book').filter(has_text=book_name).count())

    # find the created book's row and open it if needed
    row = page.locator('#panelBody a.book').filter(has_text=book_name).first
    print('book href:', row.get_attribute('href') if row.count() else None)
    if row.count():
        row.click()
        page.wait_for_timeout(600)
    print('after opening book by hand:', json.dumps(state(page)))

    # --- create a song in that book
    page.click('#songAdd')
    page.wait_for_selector('#editorContent input[name="title"]')
    song_title = 'Probe Song ' + stamp
    page.fill('#editorContent input[name="title"]', song_title)
    page.click('#editorContent .editor__save')
    page.wait_for_function("!document.querySelector('dialog[open]')")
    page.wait_for_timeout(1000)
    print('after song:', json.dumps(state(page)))
    print('song rows:', page.locator('#chList a.songrow').filter(has_text=song_title).count())
    browser.close()
