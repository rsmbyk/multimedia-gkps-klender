#!/usr/bin/env python3
"""Probe the spec-200 preview: geometry of the new control, which events move the list,
and the six conditions on the idle centring.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py

Writes shots/*.png (gitignored) and prints the numbers `spec.md`'s UI/UX and Success
Criteria sections cite. `?idle=<ms>` shortens the idle clock so the matrix runs in
seconds; the page itself defaults to 15 s.
"""

from __future__ import annotations

import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
IDLE_MS = 800

MEASURE = """
() => {
  const q = (s) => document.querySelector(s);
  const box = (el) => { const r = el.getBoundingClientRect();
    return {x: Math.round(r.x), y: Math.round(r.y), w: +r.width.toFixed(2), h: +r.height.toFixed(2)}; };
  const cs = (el, p) => getComputedStyle(el)[p];
  const pair = q('.navpair');
  const centre = q('#centreBtn');
  const svg = centre.querySelector('svg');
  const body = q('#runBody');
  const row = q('.screenerow[aria-current="true"]');
  const bb = body.getBoundingClientRect(), rr = row.getBoundingClientRect();
  return {
    pairGap: cs(pair, 'gap'),
    navpair: [...pair.children].map((b) => ({id: b.id, ...box(b)})),
    centreBox: box(centre),
    centreRadius: cs(centre, 'border-radius'),
    centreStrokeWidth: cs(centre, 'border-color'),
    svgBox: box(svg),
    svgStroke: cs(svg, 'stroke-width'),
    svgWidth: cs(svg, 'width'),
    scroller: {clientH: body.clientHeight, scrollH: body.scrollHeight},
    liveRowHeight: rr.height,
    liveRowOffCentre: Math.round(((rr.top + rr.bottom) / 2) - ((bb.top + bb.bottom) / 2)),
    liveRowFullyOffScreen: rr.bottom <= bb.top || rr.top >= bb.bottom,
  };
}
"""

SAMPLE = """
() => new Promise((done) => {
  const body = document.querySelector('#runBody');
  const frames = [];
  const t0 = performance.now();
  (function tick() {
    frames.push(Math.round(body.scrollTop));
    if (performance.now() - t0 < 420) requestAnimationFrame(tick);
    else done(frames);
  })();
})
"""

OFFSCREEN = """
() => { const b = document.querySelector('#runBody');
  const r = document.querySelector('.screenerow[aria-current="true"]').getBoundingClientRect();
  const bb = b.getBoundingClientRect();
  return Math.round(b.scrollTop) + '|' + (r.bottom <= bb.top || r.top >= bb.bottom); }
"""


def state(page) -> dict:
    return page.evaluate(MEASURE)


def scroll_away(page) -> None:
    page.evaluate("document.querySelector('#scrollAway').click()")
    page.wait_for_timeout(80)


def blockers(page, *, display_off=False, layer=False, other=False, browsed_other=False,
             picker=False, on_screen=False) -> None:
    page.evaluate(
        """(o) => {
            document.querySelector('#cLive').checked = !o.display_off;
            document.querySelector('#cLayer').checked = o.layer;
            document.querySelector('#cOther').checked = o.other;
            document.querySelector('#cBrowsed').checked = !o.browsed_other;
            document.querySelector('#dockPanel').dataset.view = o.picker ? 'pick' : 'run';
            document.querySelector('#idleOn').checked = true;
        }""",
        {"display_off": display_off, "layer": layer, "other": other,
         "browsed_other": browsed_other, "picker": picker},
    )
    if on_screen:
        page.evaluate("document.querySelector('#scrollBack').click()")
    page.wait_for_timeout(80)


def main() -> int:
    SHOTS.mkdir(exist_ok=True)
    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 940, "height": 880}, device_scale_factor=1)
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto((HERE / "index.html").as_uri() + f"?idle={IDLE_MS}", wait_until="domcontentloaded")
        page.wait_for_selector("#entryList .entryli")
        page.wait_for_timeout(150)

        print("== geometry ==")
        geo = state(page)
        for key in ("pairGap", "navpair", "centreBox", "centreRadius", "svgBox", "svgStroke",
                    "svgWidth", "scroller", "liveRowHeight"):
            print(f"  {key}: {geo[key]}")

        print("== trigger 1: the control ==")
        before = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        page.evaluate("document.querySelector('#centreBtn').click()")
        frames = page.evaluate(SAMPLE)
        page.wait_for_timeout(60)
        after = state(page)
        reversals = sum(
            1 for i in range(2, len(frames))
            if (frames[i] - frames[i - 1]) * (frames[i - 1] - frames[i - 2]) < 0
        )
        print(f"  scrollTop {before} -> {frames[-1]} · live row off centre {after['liveRowOffCentre']} px")
        print(f"  frames: {len(frames)} · reversals: {reversals} · first move at {frames}"[:160])
        page.screenshot(path=str(SHOTS / "01-centred-by-the-control.png"))

        print("== trigger 2: an item click ==")
        page.evaluate("document.querySelector('#runBody').scrollTop = 0")
        page.wait_for_timeout(60)
        page.evaluate(
            "(() => { document.querySelector('.entryli[data-index=\"3\"] .screenerow').click(); })()"
        )
        page.wait_for_timeout(400)
        print("  live entry/row:", page.evaluate(
            "(() => { const li = document.querySelector('.entryli[data-live=\"true\"]');"
            " const r = li.querySelector('.screenerow[aria-current=\"true\"]');"
            " return li.dataset.index + ' / ' + (r ? r.textContent.trim() : 'none'); })()"))
        print("  ", page.evaluate(OFFSCREEN), "(scrollTop|live row fully off screen)")
        page.screenshot(path=str(SHOTS / "02-centred-by-an-item-click.png"))

        print("== follow mode ==")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("#entryList .entryli")
        page.wait_for_timeout(120)

        def mode():
            return page.evaluate("document.querySelector('#pvMode').textContent")

        def off_centre():
            return page.evaluate(
                "(() => { const b = document.querySelector('#runBody');"
                " const r = document.querySelector('.screenerow[aria-current=\"true\"]');"
                " const bb = b.getBoundingClientRect(), rr = r.getBoundingClientRect();"
                " return Math.round(((rr.top + rr.bottom) / 2) - ((bb.top + bb.bottom) / 2)); })()")

        page.evaluate("document.querySelector('#runBody').scrollTop = 0")
        for _ in range(3):
            page.evaluate("document.querySelector('#nextBtn').click()")
            page.wait_for_timeout(240)
        print("  three advances while following:", mode(), "· live row off centre", off_centre(), "px")
        page.screenshot(path=str(SHOTS / "01b-following-advance.png"))

        page.evaluate("document.querySelector('#scrollAway').click()")
        page.wait_for_timeout(100)
        start = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        page.evaluate("document.querySelector('#nextBtn').click()")
        page.wait_for_timeout(240)
        print("  after a scroll:", mode(), "· Next left scrollTop at",
              start, "->", page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)"))

        start = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        page.evaluate("document.querySelector('#prevBtn').click()")
        page.wait_for_timeout(240)
        print("  Back from browsing:", mode(), "· scrollTop", start,
              "->", page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)"))

        before_live = page.evaluate(
            "Number(document.querySelector('.entryli[data-live=\"true\"]').dataset.index)")
        page.evaluate("document.querySelector('.nextband').click()")
        page.wait_for_timeout(240)
        after_live = page.evaluate(
            "Number(document.querySelector('.entryli[data-live=\"true\"]').dataset.index)")
        first_row = page.evaluate(
            "(() => { const li = document.querySelector('.entryli[data-live=\"true\"]');"
            " const r = li.querySelector('.screenerow[aria-current=\"true\"]');"
            " return Array.prototype.indexOf.call(li.querySelectorAll('.screenerow'), r); })()")
        print(f"  sticky Next band from browsing: {mode()} · live pointer {before_live} -> {after_live}"
              f" · first row {first_row} · off centre {off_centre()} px")

        page.evaluate("document.querySelector('#scrollAway').click()")
        page.wait_for_timeout(100)

        page.evaluate("document.querySelector('#centreBtn').click()")
        page.wait_for_timeout(240)
        page.evaluate("document.querySelector('#nextBtn').click()")
        page.wait_for_timeout(240)
        print("  after the centre control:", mode(), "· live row off centre", off_centre(), "px")

        page.evaluate("document.querySelector('.entryli[data-index=\"2\"] .entryrow').click()")
        page.wait_for_timeout(100)
        start = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        page.evaluate("document.querySelector('#prevBtn').click()")
        page.wait_for_timeout(240)
        print("  after expanding another entry:", mode(), "· Previous left scrollTop at",
              start, "->", page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)"))

        print(f"== trigger 3: the idle elapse ({IDLE_MS} ms stand-in for 15 s) ==")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("#entryList .entryli")
        page.wait_for_timeout(120)
        held = [
            ("everything clear", {}),
            ("the words are hidden", {"display_off": True}),
            ("a layer is open", {"layer": True}),
            ("another entry's header is open", {"other": True}),
            ("another service is open in the dock", {"browsed_other": True}),
            ("the picker is the view", {"picker": True}),
            ("the live row is still on screen", {"on_screen": True}),
        ]
        for label, flags in held:
            blockers(page, **flags)
            if not flags.get("on_screen"):
                scroll_away(page)
            start = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
            page.wait_for_timeout(int(IDLE_MS * 1.5))
            end = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
            verdict = "moved" if end != start else "still"
            print(f"  {label:38s} {start:>5} -> {end:<5} {verdict}")
            if flags == {}:
                page.screenshot(path=str(SHOTS / "03-centred-by-idle.png"))
                print("   mode after that idle re-centre:", page.evaluate(
                    "document.querySelector('#pvMode').textContent"))
        print("  idle clock on the page:", page.evaluate(
            "document.querySelector('#pvRead').textContent.replace('\\n', ' · ')"))

        blockers(page, layer=True)
        scroll_away(page)
        page.screenshot(path=str(SHOTS / "04-idle-held-by-a-layer.png"))

        print("== the clock's own events ==")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("#entryList .entryli")
        page.wait_for_timeout(120)

        def clock():
            return page.evaluate("document.querySelector('#idleClock').textContent")

        print("-- a moving pointer does NOT restart it --")
        blockers(page)
        scroll_away(page)
        page.wait_for_timeout(int(IDLE_MS * 0.7))
        before_move = clock()
        start = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        for step in range(1, 5):
            page.mouse.move(600 + step * 9, 620 + step * 7)
            page.wait_for_timeout(25)
        after_move = clock()
        page.wait_for_timeout(int(IDLE_MS * 0.5))
        end = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        print(f"  clock {before_move} -> {after_move} across a pointer move; "
              f"scrollTop {start} -> {end} (still centred by the elapse: {end != start})")

        print("-- a click restarts it --")
        blockers(page)
        scroll_away(page)
        page.wait_for_timeout(int(IDLE_MS * 0.7))
        before_click = clock()
        page.mouse.click(300, 80)                 # the head's text, not a control
        page.wait_for_timeout(160)
        after_click = clock()
        print(f"  clock {before_click} -> {after_click} on a click (restarted: "
              f"{float(after_click.split()[0]) > float(before_click.split()[0])})")

        print("-- a press held down suspends it --")
        page.mouse.move(300, 80)
        page.mouse.down()
        page.wait_for_timeout(int(IDLE_MS * 1.4))
        held_clock = clock()
        held_scroll = page.evaluate("Math.round(document.querySelector('#runBody').scrollTop)")
        page.mouse.up()
        page.wait_for_timeout(160)
        released_clock = clock()
        print(f"  clock while held: {held_clock}; scrollTop {held_scroll}; "
              f"on release: {released_clock}")

        print("== console ==", errors or "clean")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
