from pathlib import Path
from playwright.sync_api import sync_playwright

here = Path(__file__).resolve().parent
url = (here / 'index.html').as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(url)
    page.wait_for_timeout(120)
    page.click('.pv-bar button[data-lockstyle="label"]')
    page.click('.pv-bar button[data-scenario="rail-list"]')
    page.wait_for_timeout(420)
    print(page.evaluate("""() => {
      const e = document.querySelector('.pv-rail-busy');
      const spin = e.querySelector('.pv-lock-label') || e.querySelector('.pv-rail-spin');
      const s = spin && getComputedStyle(spin);
      const b = e.getBoundingClientRect();
      const sb = spin && spin.getBoundingClientRect();
      return {button:{x:b.x,y:b.y,w:b.width,h:b.height},
              svg:getComputedStyle(e.querySelector('svg')).display,
              spin: spin ? {x:sb.x,y:sb.y,w:sb.width,h:sb.height,
                            display:s.display,opacity:s.opacity,
                            color:s.borderTopColor,anim:s.animationName} : null};
    }"""))
    box = page.evaluate("""() => {const b=document.querySelector('.pv-rail-busy').getBoundingClientRect();
      return {x:b.x,y:b.y,width:b.width,height:b.height};}""")
    page.screenshot(path=str(here / 'railcrop.png'),
                    clip={'x': box['x'] - 12, 'y': box['y'] - 12,
                          'width': box['width'] + 90, 'height': box['height'] + 24})
    browser.close()
