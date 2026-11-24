"""Measure the shipped media-library pill hover rule against its baseline.

The live page at http://127.0.0.1:8767/media-library/ carries the change. The probe
only deletes the rule from a second page's CSSOM to obtain the before numbers.
"""
import json

from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8767/media-library/"
FIND_RULE = """() => {
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (e) { continue; }
    for (let i = 0; i < rules.length; i++) {
      const r = rules[i];
      if (r.selectorText && r.selectorText.includes('media-library__chips button:not')) {
        return {sheet: sheet.href, index: i, selector: r.selectorText, cssText: r.cssText};
      }
    }
  }
  return null;
}"""
SNAP = """el => {
  const s = getComputedStyle(el), b = el.getBoundingClientRect();
  return {background: s.backgroundColor, border: s.borderColor, color: s.color,
          width: +b.width.toFixed(2), height: +b.height.toFixed(2)};
}"""


def measure(page, dark, disable_rule):
    page.emulate_media(color_scheme="dark" if dark else "light")
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    rule = page.evaluate(FIND_RULE)
    if disable_rule:
        page.evaluate(
            """() => {
              for (const sheet of document.styleSheets) {
                let rules;
                try { rules = sheet.cssRules; } catch (e) { continue; }
                for (let i = 0; i < rules.length; i++) {
                  if (rules[i].selectorText && rules[i].selectorText.includes(
                      'media-library__chips button:not')) { sheet.deleteRule(i); return true; }
                }
              }
              return false;
            }"""
        )
    chip = page.locator('[data-media-type="image"]')
    page.mouse.move(1400, 850)
    rest = chip.evaluate(SNAP)
    chip.hover()
    page.wait_for_timeout(80)
    hover = chip.evaluate(SNAP)
    return {"rule": rule, "rest": rest, "hover": hover}


def main():
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for dark in (False, True):
            for shipped in (False, True):
                page = browser.new_page()
                key = ("dark" if dark else "light") + ("_after" if shipped else "_before")
                out[key] = measure(page, dark, disable_rule=not shipped)
                page.close()
        # selected pill: click Images, then hover it — the active fill must survive.
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle")
        chip = page.locator('[data-media-type="image"]')
        chip.click()
        page.mouse.move(1400, 850)
        selected_rest = chip.evaluate(SNAP)
        chip.hover()
        page.wait_for_timeout(80)
        out["selected_hover"] = {"rest": selected_rest, "hover": chip.evaluate(SNAP)}
        page.close()
        browser.close()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
