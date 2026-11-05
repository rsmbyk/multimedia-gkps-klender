"""Measure and drive the keyboard-parity preview (spec 187).

Run from anywhere with the project's own virtualenv:

    ~/Projects/multimedia-gkps-klender/.venv/bin/python specs/187-keyboard-parity/preview/probe.py

It prints the numbers the spec's `## UI/UX` quotes and writes the shots its README
names to `preview/shots/` (gitignored). Every state is reached through the page's
own harness, and the interactions go through the page's own handlers.
"""

import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build as preview  # the sheet's own source of truth, beside this file

PAGE = (HERE / "index.html").as_uri()
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)

STATES = ["rest", "pick", "find", "nomatch", "loading", "song", "passage", "hidden",
          "alone", "fetching", "keys", "pickkeys"]

# The Find group's order is set by FR-013 (Prev, Next, Open, Close When Empty, Close),
# not inherited from the projector's template — whose *While Finding* group still lists
# Close When Empty before Open Match until the implementation lands.
FIND_ORDER_FIXED = {"Previous Match", "Next Match", "Open Match", "Close When Empty", "Close Find"}

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
              f"head {frame_box(page, '#viewRun .dock__head')['h']} px, "
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
        head_h = frame_box(page, "#viewRun .dock__head")["h"]
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

        print("\n== a go to with no service")
        state(page, "alone")
        head_title = page.inner_text("#runService")
        date_display = page.eval_on_selector("#runDate", "n => getComputedStyle(n).display")
        print(f"  head: '{head_title}', date display {date_display}")
        check("the head names the mode, not the go to twice", head_title == "Go To", head_title)
        check("the date line is not drawn with no service", date_display == "none", date_display)
        check("the go to block is the runner's only list",
              page.eval_on_selector("#entryList", "n => n.hidden")
              and not page.eval_on_selector("#offBlock", "n => n.hidden"))
        check("a service-less go to keeps the switch control usable",
              not page.eval_on_selector("#switchBtn", "n => n.disabled"))
        check("the service-less go to's block draws its rows",
              page.eval_on_selector_all("#offBody [data-pos]", "n => n.length") == 8)
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "alone.png"))

        state(page, "fetching")
        print(f"  fetching: header '{page.inner_text('#offLabel')}', rows "
              f"{page.eval_on_selector_all('#offBody [data-pos]', 'n => n.length')}, "
              f"arrows disabled "
              f"{page.eval_on_selector('#nextBtn', 'n => n.disabled')}/"
              f"{page.eval_on_selector('#prevBtn', 'n => n.disabled')}")
        check("a fetch in flight keeps the header and draws no rows",
              page.inner_text("#offLabel") == "Loading…"
              and page.eval_on_selector_all("#offBody [data-pos]", "n => n.length") == 0)
        check("a fetch in flight disables both transport arrows",
              page.eval_on_selector("#nextBtn", "n => n.disabled")
              and page.eval_on_selector("#prevBtn", "n => n.disabled"))
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "fetching.png"))

        print("\n== the shortcut sheet")
        state(page, "keys")
        sheet = frame_box(page, ".keysheet__panel")
        body = box(page, "#keysBody")
        rows = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .krow')]"
            " .filter(n => n.getClientRects().length).length")
        groups = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .ksgroup')]"
            " .filter(n => n.getClientRects().length).length")
        first_row = page.evaluate(
            "() => { const n = [...document.querySelectorAll('#keysBody .krow')]"
            " .find(r => r.getClientRects().length); const r = n.getBoundingClientRect();"
            " const f = getComputedStyle(n);"
            " return {w:+r.width.toFixed(1), h:+r.height.toFixed(1),"
            " font: f.fontSize+'/'+f.fontWeight, color: f.color}; }")
        label_font = box(page, "#keysBody .kfn")
        labels = page.eval_on_selector_all("#keysBody .kfn", "n => n.map(x => x.textContent)")
        print(f"  panel {sheet}, body {body}, {groups} groups, {rows} rows, "
              f"first row {first_row}, label {label_font}")
        check("the sheet is inset 8px inside the dock",
              abs(sheet["x"] - 8) < 1 and abs(sheet["y"] - 8) < 1, sheet)
        check("on the runner the sheet lists five groups, 32 rows — one row per direction, in the projector's own order",
              rows == 32 and groups == 5, f"{rows} rows, {groups} groups")
        check("the picker's own group is not drawn on the runner",
              page.eval_on_selector("[data-keys='pick']", "n => n.hidden"))
        check("the sheet's first row is the dock's 30px row",
              abs(first_row["h"] - 30) < 1, first_row)
        check("the row's label is 12.5px/400", label_font["font"] == "12.5px/400", label_font)
        print(f"  body scroll {page.eval_on_selector('#keysBody', 'n => n.scrollHeight')} "
              f"of {page.eval_on_selector('#keysBody', 'n => n.clientHeight')}")
        page.eval_on_selector("#pvFrame", "n => { n.style.height = '520px'; }")
        page.wait_for_timeout(120)
        short = page.evaluate(
            "() => { const b = document.getElementById('keysBody');"
            " return {client: b.clientHeight, scroll: b.scrollHeight,"
            " panel: +document.querySelector('.keysheet__panel').getBoundingClientRect().height.toFixed(1)}; }")
        print(f"  short dock (520): {short}")
        check("a short dock scrolls the sheet instead of clipping it",
              short["scroll"] > short["client"] and short["panel"] >= 503, short)
        page.eval_on_selector("#pvFrame", "n => { n.style.height = ''; }")
        page.wait_for_timeout(120)
        print(f"  title {box(page, '.keysheet__title')['font']}, row {first_row['font']}, "
              f"keycap {box(page, '.keysheet__body .k')}")
        check("the sheet names Esc's hold and K itself",
              "Back to Services (hold)" in labels and "Keyboard Shortcuts" in labels)
        check("no row wraps its chords at 400",
              page.evaluate(
                  "() => [...document.querySelectorAll('#keysBody .krow')]"
                  " .filter(n => n.getBoundingClientRect().height > 31).length") == 0)
        overflow = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .krow')]"
            " .filter(n => n.scrollWidth > n.clientWidth + 1).length")
        check("no row overflows the sheet at 400", overflow == 0, overflow)
        cut = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .kfn')]"
            " .filter(n => n.getClientRects().length && n.scrollWidth > n.clientWidth + 1)"
            " .map(n => n.textContent)")
        check("no label is ellipsized at 400", not cut, cut)
        glyph_boxes = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody svg')]"
            " .filter(n => n.getClientRects().length)"
            " .map(n => { const r = n.getBoundingClientRect();"
            "   return [+r.width.toFixed(1), +r.height.toFixed(1)]; })")
        wrong_glyphs = [box for box in glyph_boxes if box != [11, 11]]
        check("every symbol keycap draws its glyph at 11 × 11", not wrong_glyphs, str(wrong_glyphs))
        projector_rows = set(re.findall(
            r'<span class="fn">([^<]+)</span>',
            (preview.ROOT / "multimedia/web/templates/reading/projector_controls.html")
            .read_text(encoding="utf-8")))
        visible_labels = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .kfn')]"
            " .filter(n => n.getClientRects().length).map(n => n.textContent)")
        foreign = [label for label in visible_labels
                   if label not in projector_rows and label not in preview.DOCK_ONLY_LABELS]
        print(f"  labels: {len(visible_labels)} visible, {len(foreign)} not the projector's")
        check("every shared row wears the projector's own wording, verbatim",
              not foreign, str(foreign))
        projector_order = re.findall(
            r'<span class="fn">([^<]+)</span>',
            (preview.ROOT / "multimedia/web/templates/reading/projector_controls.html")
            .read_text(encoding="utf-8"))
        first_at = {}
        for index, label in enumerate(projector_order):
            first_at.setdefault(label, index)
        shared = [label for label in visible_labels
                  if label in first_at and label not in FIND_ORDER_FIXED]
        places = [first_at[label] for label in shared]
        out_of_order = [shared[i] for i in range(1, len(places)) if places[i] < places[i - 1]]
        print(f"  order: {len(shared)} shared rows, {len(out_of_order)} out of the projector's")
        check("the shared rows keep the projector's own order",
              not out_of_order, str(out_of_order))
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "keys.png"))

        print("\n== the sheet over the picker")
        state(page, "pickkeys")
        pick_rows = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .krow')]"
            " .filter(n => n.getClientRects().length).length")
        pick_groups = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .ksgroup')]"
            " .filter(n => n.getClientRects().length).length")
        pick_first = page.eval_on_selector("#keysBody .ksgroup h4", "n => n.textContent")
        pick_services = page.eval_on_selector_all("#viewPick .servicerow", "n => n.length")
        checked_group = page.eval_on_selector(
            "[data-keys='pick']", "n => ({hidden: n.hidden, rows: n.querySelectorAll('.krow').length})")
        print(f"  picker: {pick_rows} rows in {pick_groups} groups, first group "
              f"{pick_first!r}, {pick_services} services behind")
        check("on the picker the same sheet adds the picker's group: 34 rows in six",
              pick_rows == 34 and pick_groups == 6 and not checked_group["hidden"],
              f"{pick_rows} rows, {pick_groups} groups, {checked_group}")
        check("the picker's group leads the sheet, above Service",
              pick_first == "Pick a service", pick_first)
        check("the picker's group is its two keys", checked_group["rows"] == 2, checked_group)
        check("the picker behind the sheet is the captured one",
              pick_services == 116, pick_services)
        pick_labels = page.evaluate(
            "() => [...document.querySelectorAll('#keysBody .kfn')]"
            " .filter(n => n.getClientRects().length).map(n => n.textContent)")
        own = [label for label in pick_labels if label not in projector_rows]
        check("the dock-only rows are exactly the declared set",
              set(own) == set(preview.DOCK_ONLY_LABELS), str(sorted(own)))
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "pickkeys.png"))
        state(page, "keys")
        check("returning to the runner drops the picker's group again",
              page.eval_on_selector("[data-keys='pick']", "n => n.hidden"))

        page.keyboard.press("Escape")
        page.wait_for_timeout(240)
        check("Escape closes the sheet", page.eval_on_selector("#keysheet", "n => n.hidden"))
        page.keyboard.press("k")
        page.wait_for_timeout(240)
        check("K opens the sheet", not page.eval_on_selector("#keysheet", "n => n.hidden"))
        page.keyboard.press("k")
        page.wait_for_timeout(240)
        check("K closes the sheet", page.eval_on_selector("#keysheet", "n => n.hidden"))
        page.keyboard.press("k")
        page.wait_for_timeout(240)
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(80)
        check("no other key acts while the sheet is open",
              not page.eval_on_selector("#keysheet", "n => n.hidden"))
        origin = page.eval_on_selector("#pvFrame", "n => n.getBoundingClientRect().toJSON()")
        page.mouse.click(origin["x"] + 4, origin["y"] + 4)   # the sheet's 8px frame
        page.wait_for_timeout(240)
        check("a click on the sheet's frame closes it",
              page.eval_on_selector("#keysheet", "n => n.hidden"))

        for width in (320, 520):
            page.click(f'[data-width="{width}"]')
            state(page, "keys")
            overflow = page.evaluate(
                "() => [...document.querySelectorAll('#keysBody .krow')]"
                " .filter(n => n.scrollWidth > n.clientWidth + 1).length")
            page.locator("#pvFrame").screenshot(path=str(SHOTS / f"keys-{width}.png"))
            print(f"  sheet at {width}: {frame_box(page, '.keysheet__panel')} overflow {overflow}")
            check(f"the sheet fits {width}px", overflow == 0, overflow)
        page.click('[data-width="400"]')

        page.click('[data-theme="light"]')
        state(page, "keys")
        panel_bg = page.eval_on_selector(".keysheet__panel", "n => getComputedStyle(n).backgroundColor")
        cap_bg = page.eval_on_selector("#keysBody .k", "n => getComputedStyle(n).backgroundColor")
        print(f"  light: panel {panel_bg}, keycap {cap_bg}")
        check("the sheet wears the light rail and a distinct keycap",
              panel_bg == "rgb(237, 234, 227)" and cap_bg != panel_bg, f"{panel_bg} / {cap_bg}")
        page.locator("#pvFrame").screenshot(path=str(SHOTS / "keys-light.png"))
        page.click('[data-theme="dark"]')

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
