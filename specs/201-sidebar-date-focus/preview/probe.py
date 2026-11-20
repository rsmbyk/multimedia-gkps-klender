from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parent / "index.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1000, "height": 900})
    page.goto(PAGE)
    page.wait_for_load_state("load")

    def state(which, name):
        page.evaluate("""([which, name]) => {
          const panel = document.querySelector('.panel--' + which);
          const btn = [...panel.querySelectorAll('.pvcontrols button')].find(b => b.dataset.state === name);
          btn.click();
        }""", [which, name])
        return page.evaluate("""(which) => {
          const li = document.querySelector('.panel--' + which + ' li[data-editor-kind]');
          const s = li.querySelector('.book__s');
          return {display: getComputedStyle(s).display, focusWithin: li.matches(':focus-within'),
                  active: document.activeElement && (document.activeElement.className || document.activeElement.tagName),
                  edit: getComputedStyle(li.querySelector('.row-edit')).opacity,
                  height: li.getBoundingClientRect().height,
                  fontSize: getComputedStyle(s).fontSize,
                  lineHeight: getComputedStyle(s).lineHeight};
        }""", which)

    for which in ("before", "after"):
        print("==", which)
        for name in ("rest", "hover", "clicked", "elsewhere"):
            print(f"  {name:10}", state(which, name))

    b = state("before", "clicked")
    a = state("after", "clicked")
    assert b["display"] == "none" and b["focusWithin"], b
    assert a["display"] == "block" and a["focusWithin"], a
    assert state("before", "hover")["display"] == "none"
    assert state("after", "hover")["display"] == "none"
    assert state("before", "elsewhere")["display"] == "block"
    assert state("after", "elsewhere")["display"] == "block"
    print("preview assertions: PASS")
    browser.close()
