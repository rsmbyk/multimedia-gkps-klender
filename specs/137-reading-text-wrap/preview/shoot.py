"""Spec 137 — screenshot every before/after pair at two viewports.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/137-reading-text-wrap/preview/shoot.py
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
PAGES = ['tatib', 'songs', 'bible', 'search']
VIEWPORTS = [(1440, 900), (390, 844)]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height in VIEWPORTS:
        for name in PAGES:
            for flavour in ('before', 'after'):
                page = browser.new_page(viewport={'width': width, 'height': height})
                page.goto((HERE / f'{flavour}-{name}.html').as_uri())
                page.wait_for_timeout(250)
                out = HERE / f'{flavour}-{name}-{width}x{height}.png'
                page.screenshot(path=str(out), full_page=False)
                page.close()
                print(out.name)
    browser.close()
