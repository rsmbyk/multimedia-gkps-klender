"""Before/after geometry probe for the entry-modal picker popouts.

Walks the real home -> Tata Ibadah -> service -> add-passage path and measures
each open menu's scrollport against the menu border box.
"""
from playwright.sync_api import sync_playwright
import json
import sys

PORT = sys.argv[1] if len(sys.argv) > 1 else "8778"
TAG = sys.argv[2] if len(sys.argv) > 2 else "base"

MEASURE = """() => {
  const box = (e) => { const r=e.getBoundingClientRect(),s=getComputedStyle(e);
    return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),right:+r.right.toFixed(1),bottom:+r.bottom.toFixed(1),
      w:+r.width.toFixed(1),h:+r.height.toFixed(1),ch:e.clientHeight,sh:e.scrollHeight,
      overflow:s.overflowY,pad:s.padding,margin:s.margin,radius:s.borderRadius,clip:s.overflow}; };
  return [...document.querySelectorAll('.editor__picker-menu:not([hidden])')].map(menu => ({
    menu: box(menu),
    children: [...menu.children].map(c => ({cls:c.className.toString().slice(0,60),tag:c.tagName,box:box(c),ph:c.placeholder||null}))
  }));
}"""

def dump(pg, label):
    data = pg.evaluate(MEASURE)
    print(TAG, label, json.dumps(data), flush=True)
    return data

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    pg.goto(f"http://127.0.0.1:{PORT}/", wait_until="domcontentloaded")
    pg.locator(".rail__btn[href='/tatib/']").click(); pg.wait_for_timeout(500)
    pg.locator(".book").first.click(); pg.wait_for_timeout(800)
    pg.locator(".entry__start").hover(); pg.wait_for_timeout(250)
    pg.locator(".entry__start .entry__add-btn").filter(has_text="Passage").click(); pg.wait_for_timeout(350)

    pg.locator("#entry-book-search").click(); pg.wait_for_timeout(200)
    dump(pg, "BOOK")
    pg.screenshot(path=f"/home/rsmbyk/.hermes/cache/scratch/gkps-popout-probe/{TAG}-book.png")
    pg.locator(".editor__picker-menu:not([hidden]) [role=option]:visible").first.click()
    pg.wait_for_timeout(200)

    triggers = pg.locator("[data-picker-trigger]:not([disabled])")
    print(TAG, "enabled triggers", triggers.count(), flush=True)
    for idx in range(min(2, triggers.count())):
        triggers.nth(idx).click(); pg.wait_for_timeout(200)
        dump(pg, f"MENU{idx}")
        pg.screenshot(path=f"/home/rsmbyk/.hermes/cache/scratch/gkps-popout-probe/{TAG}-menu{idx}.png")
        opts = pg.locator(".editor__picker-menu:not([hidden]) [role=option]:visible")
        print(TAG, "visible options", opts.count(), flush=True)
        if opts.count():
            opts.first.click(); pg.wait_for_timeout(150)
        else:
            pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    b.close()
