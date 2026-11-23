"""Measure the state a manually opened songbook/song reaches."""
import json, time
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:8768'

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(BASE + '/songs/')
    page.wait_for_load_state('networkidle')

    def state():
        return page.evaluate("""() => ({
          path: location.pathname,
          history: (history.state && history.state.url) || null,
          title: document.getElementById('readName')?.textContent || '',
          currentBook: document.querySelector('#panelBody a.book[aria-current="true"]')
            ?.getAttribute('data-name') || null,
          currentSong: document.querySelector('#chList a.songrow[aria-current="true"]')?.textContent || null,
          nav: document.documentElement.dataset.nav,
          ch: document.documentElement.dataset.ch,
          read: document.documentElement.dataset.read,
          bookPageCurrent: document.querySelector('.book[aria-current="true"]')?.getAttribute('href') || null
        })""")

    books = page.locator('#panelBody a.book').filter(has_text='Probe Book')
    print('probe books:', books.count())
    books.first.click()
    page.wait_for_timeout(700)
    print('book opened by hand:', json.dumps(state()))
    songs = page.locator('#chList a.songrow').filter(has_text='Probe Song')
    print('probe songs:', songs.count())
    if songs.count():
        songs.first.click()
        page.wait_for_timeout(700)
        print('song opened by hand:', json.dumps(state()))
    b.close()
