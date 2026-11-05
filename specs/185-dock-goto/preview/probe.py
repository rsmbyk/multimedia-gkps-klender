"""Measure and drive the Go To preview (spec 185).

Run from anywhere with the project's own virtualenv:

    ~/Projects/multimedia-gkps-klender/.venv/bin/python specs/185-dock-goto/preview/probe.py

It prints the numbers the spec's `## UI/UX` quotes and writes the shots its README
names to `preview/shots/` (gitignored). Every state is reached through the page's
own harness, and the interactions go through the page's own handlers.
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = (HERE / "index.html").as_uri()
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)

STATES = ["rest", "find", "nomatch", "loading", "song", "passage", "hidden"]

failures = []


def check(name, ok, detail=""):
    print(("  ok   " if ok else "  FAIL ") + name + ((" — " + str(detail)) if detail else ""))
    if not ok:
        failures.append(name)


def box(page, selector):
    return page.eval_on_selector(
        selector,
        "n => { if (!n || n.hidden) return null; const r = n.getBoundingClientRect();"
        " const f = getComputedStyle(n);"
        " return {w:+r.width.toFixed(1), h:+r.height.toFixed(1),"
        " font: f.fontSize+'/'+f.fontWeight, color: f.color}; }")


def frame_box(page, selector):
    return page.evaluate(
        "(sel) => { const n = document.querySelector(sel); const fr = document.getElementById('pvFrame');"
        " if (!n || n.hidden) return null; const r = n.getBoundingClientRect();"
        " const b = fr.getBoundingClientRect();"
        " return {x:+(r.x-b.x).toFixed(1), y:+(r.y-b.y).toFixed(1),"
        " w:+r.width.toFixed(1), h:+r.height.toFixed(1)}; }", selector)


def band_open(page):
    return page.eval_on_selector("#bandSwap", "n => n.classList.contains('is-find')")


def row_h(page, selector):
    return page.eval_on_selector(selector, "n => +n.getBoundingClientRect().height.toFixed(1)")


def state(page, name):
    page.click(f'[data-state="{name}"]')
    page.wait_for_timeout(240)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 980, "height": 940}, device_scale_factor=2)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(PAGE)
        page.wait_for_timeout(500)

        print("== the page")
        check("no script error", not errors, str(errors))
        check("the product's lookup module is ready",
              page.evaluate("window.GKPSProjectorLibrary.ready()"))

        print("\n== the states, by hand")
        for name in STATES:
            state(page, name)
            page.locator("#pvFrame").screenshot(path=str(SHOTS / f"{name}.png"))
            check(f"{name}: block and band are not both up",
                  not (not page.eval_on_selector("#offBlock", "n=>n.hidden") and band_open(page)))

        print("\n== numbers (400 × 800, dark)")
        state(page, "rest")
        entry_rows = page.eval_on_selector_all(".entryrow", "n => n.length")
        entry_label_x = frame_box(page, '.entryrow[aria-current="true"] .entryrow__t')["x"]
        entry_inner_x = frame_box(page, '.entryli[data-live="true"] .screenerow__line')["x"]
        one_line_row = page.evaluate(
            "() => [...document.querySelectorAll('.entryrow')]"
            "  .map(n => +n.getBoundingClientRect().height.toFixed(1)).sort((a,b)=>a-b)[0]")
        one_line_screen = page.evaluate(
            "() => { const rows = [...document.querySelectorAll('.entryli[data-live=\"true\"] .screenerow')]"
            "  .map(n => +n.getBoundingClientRect().height.toFixed(1)).sort((a,b)=>a-b);"
            "  return rows[0] || null; }")
        print(f"  runner: {entry_rows} entry rows, "
              f"head {frame_box(page, '.dock__head')['h']} px, "
              f"one-line entry row {one_line_row} px, one-line screenerow {one_line_screen} px")
        print(f"  transport: chip {box(page, '#transChip')} baits {box(page, '#baitStrip')} "
              f"arrows {box(page, '#nextBtn')}")

        state(page, "find")
        print(f"  band: {frame_box(page, '#findBand')} (field {box(page, '#findInput')}, "
              f"result {box(page, '#findResult')})")
        print(f"  field font {box(page, '#findInput')['font']}, "
              f"result font {box(page, '#findResult')['font']}, "
              f"count font {box(page, '#findCount')['font']}")
        check("field and suggestion share one width",
              box(page, "#findInput")["w"] == box(page, "#findResult")["w"])
        check("the field takes the focus", page.evaluate("document.activeElement.id") == "findInput")
        match_bg = page.eval_on_selector("#findResult", "n => getComputedStyle(n).backgroundColor")
        print(f"  match row background {match_bg}, border "
              f"{page.eval_on_selector('#findResult', 'n => getComputedStyle(n).borderTopColor')}")
        check("a row holding a match is highlighted",
              page.get_attribute("#findResult", "data-match") == "true"
              and match_bg != "rgba(0, 0, 0, 0)")
        state(page, "nomatch")
        page.wait_for_timeout(400)          # the row's own colour transition must settle
        empty_bg = page.eval_on_selector("#findResult", "n => getComputedStyle(n).backgroundColor")
        print(f"  empty row background {empty_bg}")
        check("a row with no match is not highlighted",
              page.get_attribute("#findResult", "data-match") == "false"
              and empty_bg != match_bg)

        state(page, "song")
        print(f"  header: {frame_box(page, '#offStrip')} label {box(page, '#offLabel')} "
              f"back {box(page, '#offBack')}")
        rows_x = frame_box(page, "#offBody .screenerow")["x"]
        line_x = frame_box(page, "#offBody .screenerow__line")["x"]
        head_x = frame_box(page, "#offBody .baithead")["x"]
        label_x = frame_box(page, "#offLabel")["x"]
        print(f"  columns: go to label {label_x}, row box {rows_x}, row text {line_x}, "
              f"bait head {head_x}; service entry label {entry_label_x}, inner row {entry_inner_x}")
        check("the header keeps the dock's own left edge", abs(label_x - 14) < 1, label_x)
        check("the go to's rows take the left space a service entry indents",
              abs(rows_x - 8) < 1 and abs(head_x - 8) < 1 and abs(line_x - 18) < 1
              and rows_x < entry_inner_x)
        strip_bg = page.eval_on_selector("#offStrip", "n => getComputedStyle(n).backgroundColor")
        back_bg = page.eval_on_selector("#offBack", "n => getComputedStyle(n).backgroundColor")
        print(f"  header fill {strip_bg}, Back fill {back_bg}")
        check("the Back control keeps its own fill on the tinted header",
              back_bg != strip_bg and back_bg == "rgb(35, 32, 25)", back_bg)
        check("the header carries no on-screen pill of its own",
              page.eval_on_selector_all("#offStrip .onscreen", "n => n.length") == 0)
        head_h = frame_box(page, ".dock__head")["h"]
        check("the header's rest position is its pinned one",
              abs(frame_box(page, "#offStrip")["y"] - head_h) < 0.6,
              frame_box(page, "#offStrip")["y"])
        state(page, "passage")
        page.wait_for_timeout(120)
        page.eval_on_selector("#runBody", "n => { n.scrollTop = 240; }")
        page.wait_for_timeout(120)
        pinned = frame_box(page, "#offStrip")["y"]
        check("the header pins to the top of the list while its verses scroll",
              pinned <= head_h + 0.6, pinned)
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "passage-pinned.png"))
        page.eval_on_selector("#runBody", "n => { n.scrollTop = 0; }")
        state(page, "song")
        check("the service's own rows are not drawn while a go to is up",
              page.eval_on_selector("#entryList", "n => n.hidden")
              and page.eval_on_selector_all(".entryrow", "n => n.length") == 27)
        print(f"  head: switch disabled {page.eval_on_selector('#switchBtn', 'n => n.disabled')}, "
              f"opacity {page.eval_on_selector('#switchBtn', 'n => getComputedStyle(n).opacity')}")
        check("the switch-service control is disabled while a go to is up",
              page.eval_on_selector("#switchBtn", "n => n.disabled")
              and page.eval_on_selector("#switchBtn", "n => getComputedStyle(n).opacity") == "0.45")
        check("the find and display controls stay usable",
              not page.eval_on_selector("#findBtn", "n => n.disabled")
              and not page.eval_on_selector("#blankBtn", "n => n.disabled"))
        check("no service row claims to be on air while a goto is up",
              page.eval_on_selector_all('.entryrow[aria-current="true"]', "n => n.length") == 0)
        print(f"  block: {frame_box(page, '#offBlock')} header {frame_box(page, '#offStrip')} "
              f"rows {page.eval_on_selector_all('#offBody [data-pos]', 'n => n.length')} "
              f"current {page.eval_on_selector_all('#offBody [aria-current=\"true\"]', 'n => n.length')}")
        check("the go to is drawn as the list's live block",
              page.eval_on_selector_all("#offBody [data-pos]", "n => n.length") == 8
              and page.eval_on_selector_all('#offBody [aria-current="true"]', "n => n.length") == 1)
        check("the block's live row is the one the strip names",
              page.evaluate("""() => { const r = document.querySelector('#offBody [aria-current="true"]');
                return !!r && r.textContent.trim().length > 0; }"""))

        state(page, "passage")
        print(f"  passage: chip {box(page, '#transChip')} baits hidden "
              f"{page.eval_on_selector('#baitStrip', 'n=>n.hidden')}")
        check("a passage goto shows the edition chip and no bait strip",
              not page.eval_on_selector("#transChip", "n=>n.hidden")
              and page.eval_on_selector("#baitStrip", "n=>n.hidden"))

        print("\n== light")
        page.click('[data-theme="light"]')
        state(page, "song")
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "song-light.png"))
        print(f"  strip label {box(page, '#offLabel')['color']}, "
              f"strip bg {page.eval_on_selector('#offStrip', 'n => getComputedStyle(n).backgroundColor')}")
        page.click('[data-theme="dark"]')

        print("\n== widths")
        for width in (320, 520):
            page.click(f'[data-width="{width}"]')
            state(page, "song")
            label = box(page, "#offLabel")
            clipped = page.eval_on_selector("#offLabel", "n => n.scrollWidth > n.clientWidth + 1")
            page.locator("#pvFrame").screenshot(path=str(SHOTS / f"width-{width}.png"))
            print(f"  {width}px: strip {frame_box(page, '#offStrip')} label {label} clipped={clipped}")
            check(f"at {width}px the strip keeps its height and Back", box(page, "#offBack") is not None)
        page.click('[data-width="400"]')

        print("\n== the go to layer")
        state(page, "find")
        page.wait_for_timeout(260)
        scrim = page.eval_on_selector(
            "#findScrim",
            "n => ({hidden: n.hidden, opacity: getComputedStyle(n).opacity,"
            " bg: getComputedStyle(n).backgroundColor,"
            " box: n.getBoundingClientRect().toJSON()})")
        print(f"  scrim {scrim}")
        check("the find band is a layer over the dock",
              not scrim["hidden"] and float(scrim["opacity"]) > 0.99)
        check("the layer is the product's backdrop",
              scrim["bg"] == "rgba(0, 0, 0, 0.68)", scrim["bg"])
        covers = page.evaluate(
            """() => { const body = document.getElementById('runBody').getBoundingClientRect();
                       const hit = document.elementFromPoint(body.x + body.width / 2,
                                                             body.y + body.height / 2);
                       return hit && hit.id; }""")
        check("the layer covers the list", covers == "findScrim", covers)
        band_hit = page.evaluate(
            """() => { const f = document.getElementById('findInput').getBoundingClientRect();
                       const hit = document.elementFromPoint(f.x + f.width / 2, f.y + f.height / 2);
                       return hit && (hit.id || hit.className); }""")
        check("the band stands above the layer", band_hit == "findInput", band_hit)
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "find-layer.png"))
        page.click("#findScrim")
        page.wait_for_timeout(260)
        check("a click on the layer closes the band",
              not band_open(page) and page.eval_on_selector("#findScrim", "n => n.hidden"))

        page.keyboard.press("g")
        page.wait_for_timeout(200)
        page.keyboard.press("Backspace")
        page.wait_for_timeout(260)
        check("Backspace on an empty field closes the band",
              not band_open(page) and page.eval_on_selector("#findScrim", "n => n.hidden"))
        page.keyboard.press("g")
        page.wait_for_timeout(200)
        page.keyboard.type("NKB")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(120)
        check("Backspace in a used field only deletes",
              page.input_value("#findInput") == "NK" and band_open(page),
              page.input_value("#findInput"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(240)

        print("\n== the transport bar")
        state(page, "song")
        bar = page.evaluate("""() => {
          const row = document.getElementById('transportRow');
          const baits = document.getElementById('baitStrip').getBoundingClientRect();
          const nav = row.querySelector('.navpair').getBoundingClientRect();
          const chips = [...document.querySelectorAll('#baitChips .bait')];
          return {display: getComputedStyle(row).display, client: row.clientHeight,
                  scroll: row.scrollHeight,
                  baitsMid: +(baits.top + baits.height / 2).toFixed(1),
                  navMid: +(nav.top + nav.height / 2).toFixed(1), chips: chips.length,
                  rowH: +row.getBoundingClientRect().height.toFixed(1)}; }""")
        print(f"  bar: {bar}")
        check("the transport bar is the normal service's row: flex, one line, nothing clipped",
              bar["display"] == "flex" and bar["scroll"] == bar["client"] == 40
              and abs(bar["baitsMid"] - bar["navMid"]) < 1)
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "bar-song.png"))
        state(page, "passage")
        bar = page.evaluate("""() => {
          const row = document.getElementById('transportRow');
          const chip = document.getElementById('transChip').getBoundingClientRect();
          const nav = row.querySelector('.navpair').getBoundingClientRect();
          return {display: getComputedStyle(row).display, scroll: row.scrollHeight,
                  client: row.clientHeight,
                  chipMid: +(chip.top + chip.height / 2).toFixed(1),
                  navMid: +(nav.top + nav.height / 2).toFixed(1)}; }""")
        print(f"  bar (passage): {bar}")
        check("a passage's bar is one line too", bar["scroll"] == bar["client"]
              and abs(bar["chipMid"] - bar["navMid"]) < 1)
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "bar-passage.png"))

        print("\n== the open/close morph")
        state(page, "rest")
        page.keyboard.press("g")
        page.wait_for_timeout(100)
        mid_transport = row_h(page, "#transportRow")
        mid_band = row_h(page, "#findBand")
        page.wait_for_timeout(220)
        print(f"  mid-flight transport {mid_transport} px, band {mid_band} px; "
              f"settled transport {row_h(page, '#transportRow')} px, band {row_h(page, '#findBand')} px")
        check("opening morphs both rows on one curve",
              0 < mid_transport < 40 and 0 < mid_band < 76)
        check("the settled band is the full band", abs(row_h(page, "#findBand") - 76) < 1)
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        closing_transport = row_h(page, "#transportRow")
        closing_band = row_h(page, "#findBand")
        page.wait_for_timeout(220)
        print(f"  closing: transport {closing_transport} → {row_h(page, '#transportRow')}, "
              f"band {closing_band} → {row_h(page, '#findBand')}")
        check("closing morphs them back the same way",
              0 < closing_transport < 40 and 0 < closing_band < 76
              and abs(row_h(page, "#findBand")) < 1
              and abs(row_h(page, "#transportRow") - 40) < 1)

        print("\n== the interactions")
        state(page, "rest")
        page.keyboard.press("g")
        page.wait_for_timeout(120)
        check("G opens the find band", band_open(page))
        page.keyboard.type("Matius 5")
        page.wait_for_timeout(120)
        check("a passage reference finds its chapter",
              page.inner_text("#findLabel").startswith("Matius 5"), page.inner_text("#findLabel"))
        page.keyboard.press("Enter")
        page.wait_for_timeout(140)
        check("Enter puts the passage on air",
              page.inner_text("#offLabel") == "Matius 5:1", page.inner_text("#offLabel"))
        check("the band returns the transport", not band_open(page))
        check("the first verse disables Previous", page.eval_on_selector("#prevBtn", "n=>n.disabled"))
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(80)
        check("an arrow steps the goto", page.inner_text("#offLabel") == "Matius 5:2")
        service_screen = page.evaluate(
            "() => document.querySelector('.screenerow[aria-current=\"true\"]')"
            " && document.querySelector('.screenerow[aria-current=\"true\"]').dataset.screen")
        check("the go to's own verses are in the list",
              page.eval_on_selector_all('#offBody [data-pos]', 'n => n.length') == 48)
        page.click('#offBody [data-pos="4"]')
        page.wait_for_timeout(120)
        check("clicking a verse row moves the passage there",
              page.inner_text("#offLabel") == "Matius 5:4", page.inner_text("#offLabel"))
        page.keyboard.press("t")
        page.wait_for_timeout(80)
        check("T flips the goto's edition", page.inner_text("#transChip") == "SIM")
        page.keyboard.press(" ")
        page.wait_for_timeout(80)
        check("Space hides the words", page.get_attribute("#blankBtn", "aria-pressed") == "true")
        check("the eye says Show words", page.get_attribute("#blankBtn", "title") == "Show words")
        page.click("#offBack")
        page.wait_for_timeout(140)
        check("Back drops the block", page.eval_on_selector("#offBlock", "n=>n.hidden"))
        check("Back brings the service's rows back",
              not page.eval_on_selector("#entryList", "n => n.hidden"))
        check("Back re-enables the switch-service control",
              not page.eval_on_selector("#switchBtn", "n => n.disabled"))
        current = page.evaluate(
            "() => document.querySelector('.screenerow[aria-current=\"true\"]')"
            " && document.querySelector('.screenerow[aria-current=\"true\"]').dataset.screen")
        check("Back returns the service to its own screen",
              current == "12" and service_screen is None, f"now {current}")
        check("the words stay hidden, as the operator blanked them",
              page.get_attribute("#blankBtn", "aria-pressed") == "true"
              and page.get_attribute("#blankBtn", "title") == "Display this service")

        page.keyboard.press("g")
        page.wait_for_timeout(100)
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        check("Escape closes the find band and leaves the service alone",
              not band_open(page) and page.eval_on_selector("#offBlock", "n=>n.hidden"))

        browser.close()

    print("\n== result")
    if failures:
        print("  FAILURES: " + ", ".join(failures))
        sys.exit(1)
    print("  all checks passed; shots in " + str(SHOTS))


if __name__ == "__main__":
    main()
