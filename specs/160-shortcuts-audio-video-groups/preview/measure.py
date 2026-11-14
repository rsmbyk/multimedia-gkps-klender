"""Measure the spec-160 preview: today vs after, at two window sizes.

    ../multimedia-gkps-klender/.venv/bin/python specs/160-shortcuts-audio-video-groups/preview/measure.py

Prints the sheet's box, its columns' heights, its groups and their rows for both variants at
1920×1080 and 1280×720. The numbers this prints are the ones `spec.md` and `plan.md` quote.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parent / "preview.html").as_uri()

PROBE = """(variant) => {
  const sheet = document.getElementById('sheet-' + variant);
  const box = el => { const r = el.getBoundingClientRect();
    return { h: Math.round(r.height * 10) / 10, w: Math.round(r.width * 10) / 10,
             top: Math.round(r.top * 10) / 10, bottom: Math.round(r.bottom * 10) / 10 }; };
  const groups = [...sheet.querySelectorAll('.group')].map(g => ({
    name: g.querySelector('h3').textContent,
    rows: [...g.querySelectorAll('.row .fn')].map(r => r.textContent),
    h: Math.round(g.getBoundingClientRect().height * 10) / 10,
    col: [...sheet.querySelectorAll('.stack')].findIndex(s => s.contains(g)) + 1,
  }));
  return { viewport: [innerWidth, innerHeight],
           sheet: box(sheet), scrollH: sheet.scrollHeight, fitLimit: innerHeight - 32,
           stacks: [...sheet.querySelectorAll('.stack')].map(s => Math.round(s.getBoundingClientRect().height * 10) / 10),
           groups };
}"""


def main() -> dict:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in ((1920, 1080), (1280, 720)):
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(URL, wait_until="networkidle")
            page.wait_for_timeout(250)
            result = {}
            for variant in ("today", "after"):
                page.click(f'.preview-bar button[data-variant="{variant}"]')
                page.wait_for_timeout(120)
                result[variant] = page.evaluate(PROBE, variant)
            out[f"{w}x{h}"] = result
            page.close()
        browser.close()
    return out


if __name__ == "__main__":
    data = main()
    for vp, variants in data.items():
        for variant, sheet in variants.items():
            print(f"{vp:>9} {variant:<5} sheet {sheet['sheet']['w']} × {sheet['sheet']['h']}px"
                  f" · limit {sheet['fitLimit']}px · scrollHeight {sheet['scrollH']}"
                  f" · columns {sheet['stacks']}")
            for group in sheet["groups"]:
                print(f"            col {group['col']}  {group['name']:<16} {group['h']:>6}px  "
                      f"{group['rows']}")
    print(json.dumps(data))
