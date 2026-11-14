"""Measure the spec-189 preview and write its shots.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python specs/189-song-verse-editing/preview/probe.py

Every number `## UI/UX` quotes comes from here. Shots land in `shots/` (gitignored).
The page is opened over `file://`; it is self-contained, so nothing else is needed.
"""

import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = (HERE / "index.html").as_uri()
SHOTS = HERE / "shots"


def box(page, selector):
    handle = page.query_selector(selector)
    if handle is None:
        return None
    return page.evaluate(
        """el => { const r = el.getBoundingClientRect();
                   return {x: +r.x.toFixed(1), y: +r.y.toFixed(1),
                           w: +r.width.toFixed(1), h: +r.height.toFixed(1)}; }""",
        handle)


def style(page, selector, prop):
    return page.evaluate(
        """([sel, prop]) => { const el = document.querySelector(sel);
                              return el ? getComputedStyle(el)[prop] : null; }""",
        [selector, prop])


def start_frames(page):
    page.evaluate(
        "() => { window.__ft = []; window.__stop = false;"
        " (function tick() { window.__ft.push(performance.now());"
        " if (!window.__stop) requestAnimationFrame(tick); })(); }")


def frame_stats(page):
    page.evaluate("() => { window.__stop = true; }")
    return page.evaluate(
        "() => { const f = window.__ft || [];"
        " const gaps = [];"
        " for (let i = 1; i < f.length; i += 1) gaps.push(f[i] - f[i - 1]);"
        " gaps.sort((a, b) => a - b);"
        " return {frames: f.length,"
        "         max_gap: gaps.length ? +gaps[gaps.length - 1].toFixed(1) : null,"
        "         p95_gap: gaps.length ? +gaps[Math.floor(gaps.length * 0.95)].toFixed(1) : null}; }")


def settle(page):
    page.evaluate("""() => Promise.all(
        document.getAnimations().map(a => a.finished.catch(() => {})))""")
    page.wait_for_timeout(60)


def set_state(page, name):
    # A programmatic click: the state bar sits behind the editor dialog's backdrop
    # once a modal is open, and Playwright's pointer click would be intercepted.
    page.evaluate(
        """name => [...document.querySelectorAll('[data-state]')]
             .find(button => button.dataset.state === name).click()""", name)
    settle(page)


def measure(page, label, report):
    report[label] = {
        "verse": box(page, ".v"),
        "number": box(page, ".v .v__n"),
        "text": box(page, ".v .v__text"),
        "verse_font": style(page, ".v", "font"),
        "number_font": style(page, ".v__n", "font"),
        "number_colour": style(page, ".v__n", "color"),
        "add": box(page, ".verse-add__btn"),
        "add_wrap": box(page, ".verse-add"),
        "add_border": style(page, ".verse-add__btn", "border"),
        "add_colour": style(page, ".verse-add__btn", "color"),
        "acts_opacity": style(page, ".v .v__acts", "opacity"),
    }


def main():
    SHOTS.mkdir(exist_ok=True)
    report = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                color_scheme="dark", device_scale_factor=1)
        page.goto(PAGE)
        page.wait_for_load_state("load")

        # ---------- rest ----------
        set_state(page, "rest")
        measure(page, "rest_1440", report)
        page.screenshot(path=str(SHOTS / "01-rest-1440-dark.png"))

        # ---------- hover ----------
        set_state(page, "hover")
        settle(page)
        row = page.query_selector_all(".v")[1]
        report["hover_1440"] = {
            "acts": box(page, ".v:nth-of-type(2) .v__acts") or page.evaluate(
                """() => { const v = document.querySelectorAll('.v')[1];
                           const a = v.querySelector('.v__acts');
                           const r = a.getBoundingClientRect();
                           return {x: +r.x.toFixed(1), y: +r.y.toFixed(1),
                                   w: +r.width.toFixed(1), h: +r.height.toFixed(1)}; }"""),
            "acts_opacity": page.evaluate(
                """() => getComputedStyle(
                    document.querySelectorAll('.v')[1].querySelector('.v__acts')).opacity"""),
            "grip": page.evaluate(
                """() => { const b = document.querySelectorAll('.v')[1]
                        .querySelector('.v__grip').getBoundingClientRect();
                    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1)}; }"""),
            "edit": page.evaluate(
                """() => { const b = document.querySelectorAll('.v')[1]
                        .querySelector('.v__edit').getBoundingClientRect();
                    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1)}; }"""),
            "text": page.evaluate(
                """() => { const b = document.querySelectorAll('.v')[1]
                        .querySelector('.v__text').getBoundingClientRect();
                    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1)}; }"""),
            "hover_delay": page.evaluate(
                """() => { const a = document.querySelectorAll('.v')[1].querySelector('.v__acts');
                    return getComputedStyle(a).transitionDuration + ' / '
                         + getComputedStyle(a).transitionDelay; }"""),
        }
        page.screenshot(path=str(SHOTS / "02-hover-1440-dark.png"))

        # ---------- a one-line verse: the tools must still fit its gutter ----------
        set_state(page, "short")
        settle(page)
        report["short"] = page.evaluate(
            """() => { const row = document.querySelectorAll('.v')[3];
                       const r = row.getBoundingClientRect();
                       const a = row.querySelector('.v__acts').getBoundingClientRect();
                       return {row: {y: +r.y.toFixed(1), h: +r.height.toFixed(1)},
                               acts: {y: +a.y.toFixed(1), h: +a.height.toFixed(1)},
                               inside: a.y >= r.y && a.y + a.height <= r.y + r.height}; }""")
        page.screenshot(path=str(SHOTS / "02b-one-line-1440-dark.png"))

        # ---------- new verse modal ----------
        set_state(page, "new")
        settle(page)
        report["new_modal"] = {
            "dialog": box(page, "#editorModal"),
            "title": box(page, "#editorModal .editor__title"),
            "title_text": page.inner_text("#editorModal .editor__title"),
            "field": box(page, "#editorModal .editor__field"),
            "textarea": box(page, "#editorModal textarea"),
            "actions": box(page, "#editorModal .editor__actions"),
            "save": box(page, "#editorModal .editor__save"),
            "cancel": box(page, "#editorModal .editor__cancel"),
            "delete_present": page.query_selector("#editorModal [data-verse-delete]") is not None,
            "focus": page.evaluate("() => document.activeElement.tagName"),
        }
        page.screenshot(path=str(SHOTS / "03-new-verse-1440-dark.png"))

        # ---------- a verse named by services ----------
        set_state(page, "used")
        settle(page)
        report["used_modal"] = {
            "title_text": page.inner_text("#editorModal .editor__title"),
            "delete_disabled": page.evaluate(
                """() => { const b = document.querySelector('#editorModal [data-verse-delete]');
                           return b ? b.disabled : null; }"""),
            "delete_border": style(page, "#editorModal .editor__delete", "borderColor"),
            "delete_colour": style(page, "#editorModal .editor__delete", "color"),
            "help": page.inner_text("#editorModal .editor__help"),
            "help_colour": style(page, "#editorModal .editor__help", "color"),
            "help_font": style(page, "#editorModal .editor__help", "font"),
        }
        page.screenshot(path=str(SHOTS / "04-edit-used-1440-dark.png"))

        # ---------- delete confirmation ----------
        set_state(page, "confirm")
        settle(page)
        report["confirm"] = {
            "title": page.inner_text("#editorModal .editor__confirm-title"),
            "hint": page.inner_text("#editorModal .editor__hint"),
            "card": box(page, "#editorModal .editor__confirm"),
            "actions": box(page, "#editorModal .editor__confirm .editor__actions"),
            "cancel": box(page, "#editorModal [data-editor-close]"),
            "delete": box(page, "#editorModal [data-confirm-delete]"),
        }
        page.screenshot(path=str(SHOTS / "05-delete-confirm-1440-dark.png"))

        # ---------- mode A: the rejected Reorder verses mode ----------
        # Its button exists only while A is being compared: at rest the page carries no
        # reorder control at all, which is the whole point of B.
        set_state(page, "rest")
        report["arrange_off"] = {
            "resting_has_button": page.evaluate(
                "() => { const b = document.querySelector('.read__reorder');"
                " return !!b && !b.hidden; }"),
            "hint_hidden": page.evaluate(
                "() => document.querySelector('.arrange-hint').hidden"),
        }
        set_state(page, "arrange")
        settle(page)
        report["arrange_on"] = {
            "toggle": box(page, ".read__reorder"),
            "toggle_label": page.inner_text(".read__reorder"),
            "hint": box(page, ".arrange-hint"),
            "row": box(page, ".v.is-compact"),
            "add_hidden": page.evaluate(
                "() => document.querySelector('.verse-add').hidden"),
        }
        page.screenshot(path=str(SHOTS / "06-arrange-mode-1440-dark.png"))

        rows = page.query_selector_all(".v")
        grip = rows[3].query_selector(".v__grip")
        start = grip.bounding_box()
        first = rows[0].bounding_box()
        start_frames(page)
        page.mouse.move(start["x"] + start["width"] / 2, start["y"] + start["height"] / 2)
        page.mouse.down()
        page.mouse.move(start["x"] + 6, first["y"] + 6, steps=16)
        page.wait_for_timeout(80)
        page.screenshot(path=str(SHOTS / "06b-arrange-dragging-1440-dark.png"))
        page.mouse.up()
        report["arrange_frames"] = frame_stats(page)
        settle(page)
        report["arrange_drag"] = page.evaluate(
            """() => ({order: [...document.querySelectorAll('.v .v__text')]
                        .map(el => el.textContent.trim().slice(0, 18)),
                       numbers: [...document.querySelectorAll('.v .v__n')]
                        .map(el => el.textContent),
                       compact: document.querySelectorAll('.v.is-compact').length})""")
        set_state(page, "rest")
        settle(page)
        report["arrange_off_after"] = page.evaluate(
            """() => ({order: [...document.querySelectorAll('.v .v__text')]
                        .map(el => el.textContent.trim().slice(0, 18)),
                       numbers: [...document.querySelectorAll('.v .v__n')]
                        .map(el => el.textContent),
                       rows: [...document.querySelectorAll('.v')]
                        .map(el => +el.getBoundingClientRect().height.toFixed(1))})""")
        page.screenshot(path=str(SHOTS / "07-after-drop-1440-dark.png"))

        # ---------- mode B: grab a grip in the reading view ----------
        set_state(page, "rest")
        rows = page.query_selector_all(".v")
        grip = rows[2].query_selector(".v__grip")
        start = grip.bounding_box()
        first = rows[0].bounding_box()
        page.hover(".v:nth-of-type(3)")
        start_frames(page)
        page.mouse.move(start["x"] + start["width"] / 2, start["y"] + start["height"] / 2)
        page.mouse.down()
        page.wait_for_timeout(90)
        report["grab_collapsed"] = {
            "compact_rows": page.evaluate(
                "() => document.querySelectorAll('.v.is-compact').length"),
            "row_height": page.evaluate(
                """() => +document.querySelector('.v').getBoundingClientRect().height.toFixed(1)"""),
        }
        page.screenshot(path=str(SHOTS / "07b-grab-collapsed-1440-dark.png"))
        page.mouse.move(start["x"] + 6, first["y"] + 6, steps=16)
        page.wait_for_timeout(80)
        page.mouse.up()
        report["grab_frames"] = frame_stats(page)
        settle(page)
        report["grab_drop"] = page.evaluate(
            """() => ({order: [...document.querySelectorAll('.v .v__text')]
                        .map(el => el.textContent.trim().slice(0, 18)),
                       numbers: [...document.querySelectorAll('.v .v__n')]
                        .map(el => el.textContent),
                       compact: document.querySelectorAll('.v.is-compact').length,
                       row_heights: [...document.querySelectorAll('.v')]
                        .map(el => +el.getBoundingClientRect().height.toFixed(1))})""")
        page.screenshot(path=str(SHOTS / "07c-grab-after-1440-dark.png"))

        # ---------- the empty song ----------
        set_state(page, "empty")
        report["empty"] = {
            "block": box(page, ".entry__empty"),
            "title": box(page, ".entry__empty-title"),
            "title_font": style(page, ".entry__empty-title", "font"),
            "hint": box(page, ".entry__empty-hint"),
            "add": box(page, ".entry__empty .verse-add__btn"),
        }
        page.screenshot(path=str(SHOTS / "08-empty-song-1440-dark.png"))

        # ---------- a hymn / restricted reader ----------
        set_state(page, "hymn")
        page.hover(".v")
        page.wait_for_timeout(200)
        report["locked"] = {
            "visible_grips": page.evaluate(
                """() => [...document.querySelectorAll('.v__grip')]
                    .filter(el => getComputedStyle(el).opacity !== '0'
                                  && el.getBoundingClientRect().width > 0).length"""),
            "add_visible": page.evaluate(
                """() => { const el = document.querySelector('.verse-add');
                           return !!el && getComputedStyle(el).display !== 'none'; }"""),
            "number_opacity_on_hover": page.evaluate(
                """() => { const n = document.querySelector('.v .v__n');
                           return n ? getComputedStyle(n).opacity : null; }"""),
            "acts_in_dom": page.evaluate(
                "() => document.querySelectorAll('.v__acts').length"),
        }
        page.screenshot(path=str(SHOTS / "09-hymn-no-controls-1440-dark.png"))

        # ---------- light ----------
        page.click("[data-theme-toggle]")
        set_state(page, "hover")
        settle(page)
        report["hover_1440_light"] = {
            "number_colour": style(page, ".v__n", "color"),
            "grip_colour": style(page, ".v__grip", "color"),
            "add_colour": style(page, ".verse-add__btn", "color"),
            "add_border": style(page, ".verse-add__btn", "borderTopColor"),
            "canvas": page.evaluate(
                "() => getComputedStyle(document.documentElement).getPropertyValue('--canvas')"),
        }
        page.screenshot(path=str(SHOTS / "10-hover-1440-light.png"))
        page.click("[data-theme-toggle]")

        # ---------- the long song: A and B on the case that motivated them ----------
        page.evaluate("() => document.querySelector('[data-long]').click()")
        set_state(page, "rest")
        report["long_rest"] = {
            "verses": page.evaluate("() => document.querySelectorAll('.v').length"),
            "row": box(page, ".v"),
            "body": box(page, "#readBody"),
            "scroll_height": page.evaluate("() => document.documentElement.scrollHeight"),
            "viewport": page.evaluate("() => innerHeight"),
        }
        page.screenshot(path=str(SHOTS / "14-long-rest-1440-dark.png"))

        set_state(page, "arrange")
        report["long_arrange"] = {
            "row": box(page, ".v"),
            "body": box(page, "#readBody"),
            "add_hidden": page.evaluate("() => document.querySelector('.verse-add').hidden"),
            "rows_in_view": page.evaluate(
                """() => [...document.querySelectorAll('.v')].filter(el => {
                       const r = el.getBoundingClientRect();
                       return r.bottom > 0 && r.top < innerHeight; }).length"""),
        }
        page.screenshot(path=str(SHOTS / "15-long-arrange-1440-dark.png"))

        set_state(page, "grab")
        report["long_grab"] = {
            "row_after_release": box(page, ".v"),
            "rows_in_view": page.evaluate(
                """() => [...document.querySelectorAll('.v')].filter(el => {
                       const r = el.getBoundingClientRect();
                       return r.bottom > 0 && r.top < innerHeight; }).length"""),
        }
        page.screenshot(path=str(SHOTS / "16-long-grab-1440-dark.png"))
        page.evaluate("() => document.querySelector('[data-long]').click()")

        # ---------- the shake: each row must move ONE slot, once, per crossing ------
        # The FLIP snapshot was once keyed by `data-verse`; two rows sharing a key threw
        # every row the list's whole height and slid it back on every crossing.
        page.evaluate("() => document.querySelector('[data-long]').click()")
        set_state(page, "arrange")
        set_state(page, "longdrag")
        # Wait for the trace's own verdict rather than a guessed duration: the gesture
        # holds twice (to read the hairlines once the rows have settled) before it drops.
        page.wait_for_function(
            "() => window.__dragTrace && window.__dragTrace.done === true",
            timeout=20000)
        report["long_drag_trace"] = page.evaluate(
            """() => { cancelAnimationFrame(window.__raf);
                       return window.__dragTrace || {}; }""")
        page.evaluate("() => document.querySelector('[data-long]').click()")

        # ---------- 420px ----------
        page.set_viewport_size({"width": 420, "height": 900})
        # At a phone width the shell's own panels cover the stage until the drawer is
        # closed; the slice is the stage, so the probe closes them the way the app does.
        page.evaluate(
            "() => { document.documentElement.dataset.nav = 'closed';"
            " document.documentElement.dataset.ch = 'closed';"
            " document.getElementById('panel').style.display = 'none';"
            " document.getElementById('chapters').style.display = 'none'; }")
        page.wait_for_timeout(150)
        set_state(page, "rest")
        report["rest_420"] = {
            "verse": box(page, ".v"),
            "number": box(page, ".v .v__n"),
            "text": box(page, ".v .v__text"),
            "add": box(page, ".verse-add__btn"),
            "add_wrap": box(page, ".verse-add"),
        }
        page.screenshot(path=str(SHOTS / "11-rest-420-dark.png"))

        set_state(page, "hover")
        settle(page)
        report["hover_420"] = page.evaluate(
            """() => { const v = document.querySelectorAll('.v')[1];
                       const a = v.querySelector('.v__acts').getBoundingClientRect();
                       const g = v.querySelector('.v__grip').getBoundingClientRect();
                       return {acts: {x:+a.x.toFixed(1), y:+a.y.toFixed(1),
                                      w:+a.width.toFixed(1), h:+a.height.toFixed(1)},
                               grip: {x:+g.x.toFixed(1), y:+g.y.toFixed(1),
                                      w:+g.width.toFixed(1), h:+g.height.toFixed(1)}}; }""")
        page.screenshot(path=str(SHOTS / "12-hover-420-dark.png"))

        set_state(page, "edit")
        settle(page)
        report["modal_420"] = {
            "dialog": box(page, "#editorModal"),
            "textarea": box(page, "#editorModal textarea"),
            "save": box(page, "#editorModal .editor__save"),
        }
        page.screenshot(path=str(SHOTS / "13-edit-420-dark.png"))

        browser.close()

    (HERE / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
