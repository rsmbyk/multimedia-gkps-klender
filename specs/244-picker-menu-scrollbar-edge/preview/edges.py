"""Edge-state measurements for slice 244 against the live 8778 page."""
from playwright.sync_api import sync_playwright
import json

MEASURE = """() => {
  const box = (e) => { if(!e) return null; const r=e.getBoundingClientRect();
    return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),right:+r.right.toFixed(1),bottom:+r.bottom.toFixed(1),
      w:+r.width.toFixed(1),h:+r.height.toFixed(1),ch:e.clientHeight,sh:e.scrollHeight,
      gutter:e.offsetWidth-e.clientWidth}; };
  const menu = document.querySelector('.editor__picker-menu:not([hidden])');
  const opts = menu && menu.querySelector('.editor__picker-options');
  const first = opts && opts.querySelector('[role=option]');
  const filter = menu && menu.querySelector('input');
  return {menu:box(menu),options:box(opts),first:box(first),filter:box(filter),
    menuOverflow:getComputedStyle(menu).overflowX,theme:document.documentElement.dataset.theme||null};
}"""

def open_modal(page):
    page.goto("http://127.0.0.1:8778/", wait_until="domcontentloaded")
    page.locator(".rail__btn[href='/tatib/']").click(); page.wait_for_timeout(450)
    page.locator(".book").first.click(); page.wait_for_timeout(700)
    page.locator(".entry__start").hover(); page.wait_for_timeout(200)
    page.locator(".entry__start .entry__add-btn").filter(has_text="Passage").click(); page.wait_for_timeout(300)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    open_modal(pg)
    pg.locator("#entry-book-search").click(); pg.wait_for_timeout(200)
    pg.locator(".editor__picker-menu:not([hidden]) [role=option]").first.click()
    pg.wait_for_timeout(150)
    pg.locator("[data-picker-trigger]:not([disabled])").first.click(); pg.wait_for_timeout(200)
    print("chapter-open", json.dumps(pg.evaluate(MEASURE)))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(150)

    # A one-chapter book gives a non-overflowing menu: no bar, no reserved lane.
    pg.locator("#entry-book-search").click(); pg.wait_for_timeout(150)
    pg.locator("#entry-book-search").fill("Obaja"); pg.wait_for_timeout(200)
    pg.locator(".editor__picker-menu:not([hidden]) [role=option]:visible").first.click()
    pg.wait_for_timeout(150)
    pg.locator("[data-picker-trigger]:not([disabled])").first.click(); pg.wait_for_timeout(200)
    print("chapter-one-option", json.dumps(pg.evaluate(MEASURE)))
    b.close()
