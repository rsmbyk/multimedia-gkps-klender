"""Spec 138 prototype probe — the shell's own measurements, at four widths.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/138-sidebar-overlay-stack/preview/probe_prototype.py
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
PAGE = (HERE / 'prototype-tatib.html').as_uri()
SHOTS = HERE / 'shots'


def stage(page):
    return page.evaluate("() => Math.round(document.querySelector('.stage').getBoundingClientRect().width)")


def drawer(page, selector):
    return page.evaluate("""(selector) => {
      const el = document.querySelector(selector);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width),
              visible: r.right > 0 && r.left < innerWidth && cs.visibility !== 'hidden',
              shadow: cs.boxShadow !== 'none'};
    }""", selector)


def levels(page):
    return page.evaluate("""() => ({
      mode: document.documentElement.dataset.mode,
      phone: document.documentElement.dataset.phone,
      nav: document.documentElement.dataset.nav,
      ch: document.documentElement.dataset.ch,
      rail: document.documentElement.dataset.rail,
    })""")


def run(page, width, label):
    page.set_viewport_size({'width': width, 'height': 900})
    page.wait_for_timeout(150)
    page.reload(wait_until='networkidle')
    page.wait_for_timeout(150)
    if page.evaluate("() => document.querySelector('.proto-panel').hidden"):
        page.click('.proto-chip')
    mode = page.evaluate("() => document.documentElement.dataset.mode")
    closed = stage(page)
    print(f'\n### {label} ({width}px) — {levels(page)}')
    print(f'  stage closed: {closed}px')

    page.click('.proto-panel [data-do="l1"]')
    page.wait_for_timeout(260)
    open1 = stage(page)
    print(f'  after level 1: stage {open1}px  panel={drawer(page, "#panel")}  {levels(page)}')
    page.screenshot(path=str(SHOTS / f'{label}-l1.png'))

    page.click('.proto-panel [data-do="l2"]')
    page.wait_for_timeout(260)
    open2 = stage(page)
    print(f'  after level 2: stage {open2}px  panel={drawer(page, "#panel")}  chapters={drawer(page, "#chapters")}')
    page.screenshot(path=str(SHOTS / f'{label}-l2.png'))

    phone = page.evaluate("() => document.documentElement.dataset.phone") == 'yes'
    after = open2
    if mode == 'overlay' and not phone:
        page.mouse.click(int(width * 0.72), int(900 * 0.3))
        page.wait_for_timeout(260)
        after = stage(page)
        print(f'  after backdrop: stage {after}px  {levels(page)}')

        # the rail restores the last level
        page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        page.wait_for_timeout(260)
        print(f'  rail restores: {levels(page)}')
        page.screenshot(path=str(SHOTS / f'{label}-restored.png'))

    page.click('.proto-panel [data-do="close"]')
    page.wait_for_timeout(200)

    if phone:
        icon = "() => document.querySelector('.proto-toolbar__control').dataset.icon"
        page.click('.proto-toolbar__control')
        page.wait_for_timeout(260)
        labels = page.evaluate(
            "() => [...document.querySelectorAll('.rail__menu .rail__btn .proto-label')]"
            ".map((n) => n.textContent)")
        logo = page.evaluate("() => getComputedStyle(document.querySelector('.rail__logo')).display")
        foot = page.evaluate("() => document.querySelector('.rail__foot').parentElement.className")
        print(f'  menu open: {levels(page)} icon={page.evaluate(icon)} labels {labels}')
        print(f'  drawer logo display: {logo}  · rail foot lives in: {foot!r}')
        page.screenshot(path=str(SHOTS / f'{label}-rail.png'))

        page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        page.wait_for_timeout(260)
        print(f'  section chosen: {levels(page)} icon={page.evaluate(icon)}')
        print(f'  level 2 offered on a phone: {page.evaluate("() => !!document.querySelector('#chapters')")}'
              f' — chapters open: {page.evaluate("() => document.documentElement.dataset.ch")}')

        # level 2 is not offered for a service on a phone; the button must do nothing
        page.click('.proto-panel [data-do="l2"]')
        page.wait_for_timeout(200)
        print(f'  after asking for level 2: ch={page.evaluate("() => document.documentElement.dataset.ch")}')

        # the drawer's own back control returns to the menu, which stayed underneath
        page.click('#panelCollapse')
        page.wait_for_timeout(260)
        print(f'  drawer back: {levels(page)} icon={page.evaluate(icon)}')

        page.click('.proto-toolbar__control')
        page.wait_for_timeout(260)
        print(f'  close: {levels(page)} icon={page.evaluate(icon)}')
        print(f'  project button display on a phone: '
              f'{page.evaluate("() => getComputedStyle(document.querySelector('[data-project-open]') || document.body).display")}')
    return {'closed': closed, 'l1': open1, 'l2': open2, 'after': after}


with sync_playwright() as p:
    SHOTS.mkdir(exist_ok=True)
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(PAGE, wait_until='networkidle')
    page.click('.proto-chip')
    results = {}
    for width, label in ((1440, 'columns'), (1024, 'tablet'), (768, 'report'), (425, 'phone')):
        results[label] = run(page, width, label)
    print('\nstage width, closed → level 1 → level 2 → after backdrop')
    for label, r in results.items():
        print(f'  {label:<8} {r["closed"]:>5} → {r["l1"]:>5} → {r["l2"]:>5} → {r["after"]:>5}')
    browser.close()
