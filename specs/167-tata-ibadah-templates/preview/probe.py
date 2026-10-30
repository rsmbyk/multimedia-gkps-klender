"""Spec 167 preview probe.

Opens the static preview in Chromium, walks every state the spec claims, writes one
screenshot per state into ``shots/`` and prints the measured numbers as JSON.

    ~/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/167-tata-ibadah-templates/preview/probe.py
"""

from __future__ import annotations

import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)
URL = (HERE / "index.html").as_uri()


def box(page, selector):
    node = page.locator(selector).first
    if not node.count():
        return None
    return node.evaluate(
        "el => { const r = el.getBoundingClientRect();"
        " return {x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1)}; }"
    )


def shot(page, name):
    page.screenshot(path=str(SHOTS / f"{name}.png"))


def main() -> None:
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(URL)
        page.wait_for_timeout(250)

        report["template_page"] = {
            "read": box(page, ".read"),
            "eyebrow": page.locator("#read .read__eyebrow").inner_text(),
            "actions": [b.strip() for b in page.locator(".read__project button").all_inner_texts()],
            "projector_controls": page.locator("[data-project-open], [data-project-window]").count(),
            "slot_rows": page.locator(".tatib__item--slot").count(),
            "choice_options": page.locator(".choice__option").count(),
            "add_buttons_visible": page.locator(".entry__add-btn").count(),
        }
        shot(page, "01-template-page")

        page.locator('[data-surface="kinds"]').click()
        page.set_viewport_size({"width": 1440, "height": 1200})
        page.wait_for_timeout(300)
        report["kinds"] = {
            "fixed": page.locator(".kinds .tatib__item--entry").count(),
            "fillins": page.locator(".kinds .tatib__item--slot").count(),
            "choices": page.locator(".kinds .tatib__item--choice").count(),
            "options": page.locator(".kinds .choice__option").count(),
            "body": box(page, "#kinds .read__body"),
            "page_height": page.evaluate("document.documentElement.scrollHeight"),
        }
        shot(page, "19-kinds-top")
        page.screenshot(path=str(SHOTS / "20-kinds-full.png"), full_page=True)
        page.locator(".kinds__head").nth(1).evaluate("el => el.scrollIntoView({block: 'start'})")
        page.wait_for_timeout(250)
        shot(page, "21-kinds-fillins")
        page.locator(".kinds__head").nth(2).evaluate("el => el.scrollIntoView({block: 'start'})")
        page.wait_for_timeout(250)
        shot(page, "22-kinds-choices")

        page.locator('[data-surface="template"]').click()
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(250)

        page.locator("[data-toggle-bars]").click()
        page.wait_for_timeout(250)
        report["bars_1440"] = {
            "start_inner": box(page, ".entry__start-inner"),
            "read_body": box(page, ".read__body"),
            "john_overflow": page.locator(".entry__start-inner").first.evaluate(
                "el => ({scroll: el.scrollWidth, client: el.clientWidth,"
                " height: el.getBoundingClientRect().height})"
            ),
        }
        shot(page, "02-template-page-bars")
        page.locator("[data-toggle-bars]").click()

        page.locator('[data-surface="new"]').click()
        page.wait_for_timeout(200)
        report["new_normal"] = {
            "frame": box(page, "#newModal"),
            "switch": box(page, "#newModal [data-kind-switch]"),
            "date_hidden": page.locator("[data-new-date]").evaluate("el => el.hidden"),
            "save": box(page, "#newModal .editor__save"),
        }
        shot(page, "03-new-normal")

        page.locator('[data-kind="template"]').click()
        page.wait_for_timeout(250)
        report["new_template"] = {
            "date_hidden": page.locator("[data-new-date]").evaluate("el => el.hidden"),
            "switch_selected": page.locator("[data-kind-switch]").get_attribute("data-selected"),
            "thumb": box(page, "#newModal .screen-mode__thumb"),
        }
        shot(page, "04-new-template")
        page.locator("#newModal [data-close]").click()

        page.locator('[data-surface="edit"]').click()
        page.wait_for_timeout(200)
        report["edit"] = {
            "frame": box(page, "#editModal"),
            "switch_present": page.locator("#editModal [data-kind-switch]").count(),
            "copy_button": page.locator("[data-copy-open]").inner_text(),
            "copy_button_box": box(page, "[data-copy-open]"),
        }
        shot(page, "05-edit")
        page.locator("[data-copy-open]").click()
        page.wait_for_timeout(200)
        report["copy_confirm"] = {
            "layer": box(page, "[data-copy-confirm] .confirm"),
            "title": page.locator("#copyTitle").inner_text(),
            "actions": [b.strip() for b in page.locator("[data-copy-confirm] button").all_inner_texts()],
        }
        shot(page, "06-copy-confirm")
        page.locator("[data-copy-cancel]").click()
        page.locator("#editModal [data-close]").click()

        page.locator('[data-surface="generate"]').click()
        page.wait_for_timeout(250)
        report["generate_step1"] = {
            "frame": box(page, "#generateModal"),
            "next_disabled": page.locator("#generateModal [data-generate-next]").is_disabled(),
            "status": page.locator("#generateModal [data-generate-status]").inner_text(),
            "fixed_opacity": page.locator(".g-stage-row[data-fixed]").first.evaluate(
                "el => getComputedStyle(el).opacity"
            ),
            "rows": page.locator('[data-generate-step="1"] .g-row, [data-generate-step="1"] .g-stage-row').count(),
            "slots": page.locator("[data-slot-row], [data-choice-row]").count(),
            "body": page.locator('#generateModal [data-generate-step="1"]').evaluate(
                "el => ({scroll: el.scrollHeight, client: el.clientHeight})"
            ),
            "fonts": {
                "slot_title": page.locator(".g-title").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "slot_value": page.locator("#generateModal .g-value").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "fixed_heading": page.locator(".g-stage-row .read__sec").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "fixed_body": page.locator(".g-stage-row .tatib__tx").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "page_heading": page.locator("#read .read__sec").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "page_body": page.locator("#read .tatib__tx").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "page_slot_title": page.locator("#read .slot__title").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "page_slot_state": page.locator("#read .slot__state").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "modal_slot_label": page.locator(".g-label").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
                "page_slot_label": page.locator("#read .slot__kind").first.evaluate(
                    "el => getComputedStyle(el).font"
                ),
            },
        }
        shot(page, "07-generate-unsettled")
        page.locator('#generateModal [data-generate-step="1"]').evaluate("el => el.scrollTop = el.scrollHeight")
        page.wait_for_timeout(250)
        shot(page, "07b-generate-unsettled-bottom")
        page.locator('#generateModal [data-slot-row="media"]').first.scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        shot(page, "07c-generate-media")
        page.locator('#generateModal [data-choice-row="media"]').first.scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        shot(page, "07d-generate-choices")
        page.locator('#generateModal [data-slot-row="media"]').nth(4).scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        shot(page, "07e-generate-media-tail")
        page.locator('#generateModal [data-generate-step="1"]').evaluate("el => el.scrollTop = 0")
        page.wait_for_timeout(150)

        page.locator('#generateModal [data-choice-row="song"] [data-choice-open]').click()
        page.wait_for_timeout(200)
        report["choose"] = {
            "card": box(page, '#generateModal [data-choose="song"] .choose'),
            "options": page.locator('#generateModal [data-choose="song"] [data-choose-pick]').count(),
            "preview_buttons": page.locator('#generateModal [data-choose="song"] [data-choose-preview]').count(),
        }
        shot(page, "08-choose")
        page.locator('#generateModal [data-choose="song"] [data-choose-preview]').first.click()
        page.wait_for_timeout(150)
        report["choose_preview_open"] = page.locator('#generateModal [data-choose="song"] .choose__content').first.evaluate(
            "el => !el.hidden"
        )
        shot(page, "09-choose-preview")
        page.locator('#generateModal [data-choose="song"] [data-choose-pick]').first.click()
        page.wait_for_timeout(200)

        page.locator('#generateModal [data-choice-row="passage"] [data-choice-open]').click()
        page.wait_for_timeout(200)
        report["choose_passage"] = {
            "card": box(page, '#generateModal [data-choose="passage"] .choose'),
            "options": [t.strip() for t in page.locator('#generateModal [data-choose="passage"] .choose__ref').all_inner_texts()],
        }
        shot(page, "08b-choose-passage")
        page.locator('#generateModal [data-choose="passage"] [data-choose-pick]').nth(1).click()
        page.wait_for_timeout(200)

        page.locator('#generateModal [data-choice-row="text"] [data-choice-open]').click()
        page.wait_for_timeout(200)
        report["choose_text"] = {
            "card": box(page, '#generateModal [data-choose="text"] .choose'),
            "options": [t.strip() for t in page.locator('#generateModal [data-choose="text"] .choose__ref').all_inner_texts()],
        }
        shot(page, "08c-choose-text")
        page.locator('#generateModal [data-choose="text"] [data-choose-pick]').nth(2).click()
        page.wait_for_timeout(200)

        for key, shot_name in (
            ("media", "08e-choose-media"),
            ("media-plain", "08f-choose-media-plain"),
            ("text-plain", "08g-choose-text-plain"),
        ):
            page.locator('#generateModal [data-choice-row="%s"] [data-choice-open]' % key).click()
            page.wait_for_timeout(200)
            report["choose_" + key] = {
                "card": box(page, '#generateModal [data-choose="%s"] .choose' % key),
                "options": [t.strip() for t in page.locator('#generateModal [data-choose="%s"] .choose__ref' % key).all_inner_texts()],
            }
            shot(page, shot_name)
            picks = page.locator('#generateModal [data-choose="%s"] [data-choose-pick]' % key)
            picks.first.click()
            page.wait_for_timeout(150)

        for kind in ("song", "text"):
            page.locator('#generateModal [data-slot-row="%s"] [data-slot-action]' % kind).click()
            page.wait_for_timeout(120)
        report["generate_settled"] = {
            "next_disabled": page.locator("#generateModal [data-generate-next]").is_disabled(),
            "status": page.locator("#generateModal [data-generate-status]").inner_text(),
            "values": [v.strip() for v in page.locator("#generateModal .g-value").all_inner_texts()],
            "song_bait": page.locator('#generateModal [data-choice-row="song"] [data-choice-value]').evaluate(
                "el => { const b = el.querySelector('.g-bait');"
                " return b ? {text: b.textContent, color: getComputedStyle(b).color,"
                " valueColor: getComputedStyle(el).color} : null; }"
            ),
        }
        shot(page, "10-generate-settled")
        page.locator('#generateModal [data-choice-row="media"]').first.scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        shot(page, "10b-generate-settled-choices")

        page.locator("#generateModal [data-generate-next]").click()
        page.wait_for_timeout(200)
        report["generate_step2"] = {
            "status_visible": page.locator("#generateModal [data-generate-status]").is_visible(),
            "create_visible": page.locator("#generateModal [data-generate-create]").is_visible(),
            "back_visible": page.locator("#generateModal [data-generate-back]").is_visible(),
            "name": page.locator("#generateName").input_value(),
        }
        shot(page, "11-generate-step2")

        page.locator("#generateModal [data-generate-create]").click()
        page.wait_for_timeout(200)
        report["create_confirm"] = {
            "card": box(page, "[data-create-confirm] .confirm"),
            "message": page.locator("#createMessage").inner_text(),
        }
        shot(page, "12-create-confirm")
        page.locator("[data-create-cancel]").click()
        page.evaluate("document.getElementById('generateModal').close()")

        # Narrower window: the template add bar and the generate frame.
        page.set_viewport_size({"width": 900, "height": 900})
        page.wait_for_timeout(200)
        page.locator("[data-toggle-bars]").click()
        page.wait_for_timeout(250)
        report["bars_900"] = {
            "start_inner": box(page, ".entry__start-inner"),
            "read_body": box(page, ".read__body"),
            "overflow": page.locator(".entry__start-inner").first.evaluate(
                "el => ({scroll: el.scrollWidth, client: el.clientWidth,"
                " height: el.getBoundingClientRect().height})"
            ),
        }
        shot(page, "13-template-bars-900")
        page.locator('[data-add="fillin"]').first.click()
        page.wait_for_timeout(250)
        report["fillin_modal"] = {
            "frame": box(page, "#fillinModal"),
            "kinds": [t.strip() for t in page.locator("#fillinModal .kind-pick button").all_inner_texts()],
            "pressed": page.locator("#fillinModal .kind-pick button[aria-pressed='true']").inner_text(),
        }
        shot(page, "35-add-fillin")
        page.locator("#fillinModal [data-close]").first.click()
        page.wait_for_timeout(200)
        page.locator('[data-add="choice"]').first.click()
        page.wait_for_timeout(250)
        report["choice_modal"] = {
            "frame": box(page, "#choiceModal"),
            "kinds": [t.strip() for t in page.locator("#choiceModal .kind-pick button").all_inner_texts()],
            "pressed": page.locator("#choiceModal .kind-pick button[aria-pressed='true']").inner_text(),
        }
        shot(page, "36-add-choice")
        page.locator("#choiceModal [data-close]").first.click()
        page.wait_for_timeout(200)
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(200)
        page.locator('[data-surface="empty"]').click()
        page.wait_for_timeout(250)
        empty_btn = page.locator('#emptyChoiceModal [data-choice-row="none"] .g-action')
        report["empty_choice"] = {
            "frame": box(page, "#emptyChoiceModal"),
            "disabled": empty_btn.is_disabled(),
            "label": empty_btn.inner_text(),
            "value": page.locator('#emptyChoiceModal [data-choice-row="none"] .g-value').inner_text(),
            "status": page.locator('#emptyChoiceModal .generate__status').inner_text(),
            "next_disabled": page.locator("#emptyChoiceModal .generate__next").is_disabled(),
        }
        shot(page, "40-generate-no-options")
        page.locator("#emptyChoiceModal [data-close]").first.click()
        page.wait_for_timeout(200)
        page.set_viewport_size({"width": 900, "height": 900})
        page.wait_for_timeout(200)
        page.locator('[data-surface="generate"]').click()
        page.wait_for_timeout(250)
        report["generate_900"] = {
            "frame": box(page, "#generateModal"),
            "foot": box(page, ".generate__foot"),
        }
        shot(page, "14-generate-900")

        page.set_viewport_size({"width": 420, "height": 860})
        page.wait_for_timeout(250)
        shot(page, "15-generate-420")
        report["generate_420"] = {
            "frame": box(page, "#generateModal"),
            "foot": box(page, ".generate__foot"),
        }
        page.evaluate("document.getElementById('generateModal').close()")
        page.wait_for_timeout(250)
        report["bars_420"] = {
            "start_inner": box(page, ".entry__start-inner"),
            "read_body": box(page, ".read__body"),
            "overflow": page.locator(".entry__start-inner").first.evaluate(
                "el => ({scroll: el.scrollWidth, client: el.clientWidth,"
                " height: el.getBoundingClientRect().height})"
            ),
        }
        shot(page, "16-template-bars-420")

        # Dark mode: the new components must ride the tokens, not paint their own colours.
        page.set_viewport_size({"width": 1440, "height": 900})
        page.locator("[data-toggle-bars]").click()
        page.locator("[data-toggle-theme]").click()
        page.wait_for_timeout(250)
        shot(page, "17-template-dark")
        page.locator('[data-surface="generate"]').click()
        page.wait_for_timeout(250)
        shot(page, "18-generate-dark")
        report["dark"] = {
            "theme": page.evaluate("document.documentElement.dataset.theme"),
            "canvas": page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--canvas').trim()"),
            "generate_frame": box(page, "#generateModal"),
        }

        report["console_errors"] = errors
        browser.close()

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
