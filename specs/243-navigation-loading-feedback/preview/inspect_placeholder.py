from pathlib import Path
from playwright.sync_api import sync_playwright

here = Path(__file__).resolve().parent
url = (here / 'index.html').as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(url)
    page.wait_for_timeout(120)
    page.click('.pv-bar button[data-scenario="verse-page"]')
    page.wait_for_timeout(420)
    print(page.evaluate("""() => {
      const stage = document.querySelector('.stage');
      const real = stage.querySelector(':scope > .read');
      const ph = document.querySelector('#pvPh-bible');
      const pra = ph.querySelector('.read');
      const head = real.querySelector('.read__head');
      const phead = pra.querySelector('.read__head');
      const box = (e) => { if (!e) return null; const b=e.getBoundingClientRect();
        return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1)}; };
      const cs = (e, p) => e ? getComputedStyle(e)[p] : null;
      return {stage:box(stage), stagePad:[cs(stage,'paddingLeft'),cs(stage,'paddingTop')],
              realRead:box(real), placeholder:box(ph), phRead:box(pra),
              realHead:box(head), phHead:box(phead),
              realMargin:[cs(real,'marginLeft'),cs(real,'marginTop')],
              phMargin:[cs(pra,'marginLeft'),cs(pra,'marginTop')]};
    }"""))
    browser.close()
