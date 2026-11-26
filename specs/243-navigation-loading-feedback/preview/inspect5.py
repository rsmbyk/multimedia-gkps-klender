from pathlib import Path
from playwright.sync_api import sync_playwright

url = (Path(__file__).resolve().parent / 'index.html').as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(url)
    page.wait_for_timeout(120)
    page.click('.pv-bar button[data-rowstyle="a"]')
    page.wait_for_timeout(420)
    print(page.evaluate("""() => {
      const e = document.querySelector('.pv-row-busy');
      const s = getComputedStyle(e, '::after');
      const r = e.getBoundingClientRect();
      return {rect:{x:r.x,y:r.y,w:r.width,h:r.height},
              overflow:getComputedStyle(e).overflow,
              after:{content:s.content,display:s.display,width:s.width,height:s.height,
                     border:s.borderTopWidth,color:s.borderTopColor,position:s.position,
                     right:s.right,top:s.top}};
    }"""))
    box = page.evaluate("""() => {const b=document.querySelector('.pv-row-busy').getBoundingClientRect();
      return {x:b.x,y:b.y,width:b.width,height:b.height};}""")
    page.screenshot(path=str(Path(__file__).resolve().parent / 'rowcrop.png'),
                    clip={'x': box['x'] - 10, 'y': box['y'] - 10,
                          'width': box['width'] + 80, 'height': box['height'] + 20})
    browser.close()
