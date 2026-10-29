"""Spec 155 — read back the projector's audio presentation lock.

Drives the slice's own projector route with a real recording and prints the readings the
spec quotes: the fullscreen takeover, every navigation input while it plays, and the three
ways the screen comes back (Space, a held Escape, the end of the recording).

    .venv/bin/python specs/155-audio-presentation-lock/preview/probe_lock.py \
        --base http://127.0.0.1:63404 --service 144

Exit code 0 when every requirement it covers reads as the spec says, 1 otherwise.
"""
import argparse
import json
import sys

from playwright.sync_api import sync_playwright

NAV_KEYS = ['ArrowRight', 'ArrowLeft', 'ArrowUp', 'ArrowDown',
            'PageDown', 'PageUp', 'Home', 'End',
            'Control+ArrowRight', 'Shift+ArrowRight']
DENY_FULLSCREEN = """Object.defineProperty(Element.prototype, 'requestFullscreen', {
  configurable: true, value: function () { return Promise.reject(new Error('denied')); }});"""


def active_screen(page):
    return page.get_attribute('body', 'data-current-screen')


def read(page, selector, attr):
    locator = page.locator(f'.screen.is-active {selector}')
    return locator.get_attribute(attr) if locator.count() else None


def open_audio_screen(page, base, service):
    page.goto(f'{base}/projector?service={service}', wait_until='load')
    page.wait_for_timeout(600)
    if page.get_attribute('body', 'data-showing') != 'true':
        page.keyboard.press('Space')
        page.wait_for_timeout(250)
    for _ in range(40):
        if page.evaluate("() => Boolean(document.querySelector('.screen.is-active [data-media-audio]'))"):
            break
        page.keyboard.press('Control+ArrowRight')
        page.wait_for_timeout(120)
    else:
        raise SystemExit(f'no audio screen reachable on service {service}')
    # the recording's bytes still have to arrive: the player only answers Space once its
    # metadata has loaded, which is the moment `data-playing` first appears
    page.wait_for_function("""() => {
        const play = document.querySelector('.screen.is-active [data-audio-play]');
        return Boolean(play) && play.dataset.playing !== undefined;
    }""", timeout=30000)


def playing_state(page):
    return read(page, '[data-audio-play]', 'data-playing')


def probe(base, service):
    readings = {}
    checks = []

    def check(name, ok, detail):
        checks.append({'check': name, 'ok': bool(ok), 'detail': detail})

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        # --- a recording takes the screen -----------------------------------
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        open_audio_screen(page, base, service)
        readings['audio_screen'] = active_screen(page)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        page.wait_for_timeout(900)

        box = page.evaluate("""() => {
            const e = document.fullscreenElement;
            const r = e.getBoundingClientRect();
            return {className: e.className, x: r.x, y: r.y, width: r.width, height: r.height,
                    background: getComputedStyle(e).backgroundColor};
        }""")
        readings['fullscreen_element'] = box
        check('FR-004 the audio box is the fullscreen element',
              'screen__audio-box' in box['className'], box['className'])
        check('SC-003 it fills the viewport',
              (box['width'], box['height']) == (1440, 900) and box['x'] == 0 and box['y'] == 0,
              f"{box['width']}x{box['height']} at ({box['x']}, {box['y']})")
        readings['cue_inside_fullscreen'] = page.evaluate("""() => {
            const cue = document.getElementById('corner-cue');
            const e = document.fullscreenElement;
            return Boolean(cue && e && e.contains(cue));
        }""")
        check('FR-004 the corner cue is off screen',
              readings['cue_inside_fullscreen'] is False, str(readings['cue_inside_fullscreen']))

        # --- every navigation input is inert --------------------------------
        moved = {}
        for key in NAV_KEYS:
            before = active_screen(page)
            page.keyboard.press(key)
            page.wait_for_timeout(180)
            moved[key] = {'before': before, 'after': active_screen(page)}
            moved[key]['moved'] = moved[key]['before'] != moved[key]['after']
        page.keyboard.press('g')
        page.wait_for_timeout(250)
        moved['g'] = {'opened': page.evaluate("() => !document.getElementById('projectorFind').hidden")}
        page.keyboard.press('j')
        page.wait_for_timeout(250)
        moved['j'] = {'opened': page.evaluate(
            "() => document.body.classList.contains('entry-list-open')")}
        readings['inputs_while_playing'] = moved
        check('FR-001 no key moves the projector',
              not any(v['moved'] for k, v in moved.items() if 'moved' in v),
              json.dumps({k: v for k, v in moved.items() if 'moved' in v}))
        check('FR-003 the Go To and entry list stay shut',
              moved['g']['opened'] is False and moved['j']['opened'] is False, json.dumps(
                  {'g': moved['g'], 'j': moved['j']}))
        readings['elapsed_while_playing'] = page.inner_text('.screen.is-active [data-audio-elapsed]')
        readings['still_playing_after_inputs'] = playing_state(page)

        def seconds(clock):
            minutes, _, secs = clock.partition(':')
            return int(minutes) * 60 + int(secs or 0)

        # the pointer while the takeover is in force: the zones are off screen, and a
        # click where the next zone sits must not move the projector either
        page.mouse.click(1400, 450)
        page.wait_for_timeout(300)
        readings['after_fullscreen_zone_click'] = active_screen(page)
        check('FR-002 a click where the next zone sits moves nothing',
              readings['after_fullscreen_zone_click'] == readings['audio_screen'],
              f"{readings['audio_screen']} -> {readings['after_fullscreen_zone_click']}")
        check('a stray input never stops the recording',
              readings['still_playing_after_inputs'] == 'true', readings['still_playing_after_inputs'])

        # --- Space gives the screen back, keeping the place -----------------
        kept = readings['elapsed_while_playing']
        page.keyboard.press('Space')
        page.wait_for_timeout(700)
        readings['after_space'] = {
            'playing': playing_state(page),
            'fullscreen': page.evaluate('() => Boolean(document.fullscreenElement)'),
            'screen': active_screen(page),
            'elapsed': page.inner_text('.screen.is-active [data-audio-elapsed]'),
        }
        check('FR-005 Space pauses and leaves fullscreen',
              readings['after_space']['playing'] == 'false'
              and readings['after_space']['fullscreen'] is False
              and readings['after_space']['screen'] == readings['audio_screen'],
              json.dumps(readings['after_space']))
        check('SC-002 the place is kept',
              readings['after_space']['elapsed'] != '0:00'
              and seconds(readings['after_space']['elapsed']) >= seconds(kept)
              and seconds(readings['after_space']['elapsed']) - seconds(kept) <= 2,
              f"{kept} -> {readings['after_space']['elapsed']}")
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(300)
        readings['after_pause_arrow_right'] = active_screen(page)
        check('the keys come back after the pause',
              readings['after_pause_arrow_right'] != readings['audio_screen'],
              f"{readings['audio_screen']} -> {readings['after_pause_arrow_right']}")
        page.close()

        # --- a held Escape exits and pauses ---------------------------------
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        open_audio_screen(page, base, service)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        page.wait_for_timeout(600)
        page.keyboard.down('Escape')
        page.wait_for_timeout(1300)
        page.keyboard.up('Escape')
        page.wait_for_timeout(400)
        readings['after_escape'] = {
            'fullscreen': page.evaluate('() => Boolean(document.fullscreenElement)'),
            'playing': playing_state(page),
            'screen': active_screen(page),
        }
        check('FR-006 leaving fullscreen pauses the recording',
              readings['after_escape']['fullscreen'] is False
              and readings['after_escape']['playing'] == 'false'
              and readings['after_escape']['screen'] == readings['audio_screen'],
              json.dumps(readings['after_escape']))
        page.close()

        # --- the end of the recording returns on its own --------------------
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        open_audio_screen(page, base, service)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        page.evaluate("""() => {
            const seek = document.querySelector('.screen.is-active .screen__audio-box [data-audio-seek]');
            const box = seek.getBoundingClientRect();
            seek.dispatchEvent(new PointerEvent('pointerdown', {clientX: box.left + box.width - 2,
                clientY: box.top + box.height / 2, pointerId: 1, bubbles: true}));
        }""")
        page.wait_for_timeout(3000)
        readings['after_end'] = {
            'fullscreen': page.evaluate('() => Boolean(document.fullscreenElement)'),
            'playing': playing_state(page),
            'elapsed': page.inner_text('.screen.is-active [data-audio-elapsed]'),
        }
        check('FR-007 the end of the recording returns the screen',
              readings['after_end']['fullscreen'] is False
              and readings['after_end']['playing'] == 'false',
              json.dumps(readings['after_end']))
        page.close()

        # --- a refused fullscreen still locks -------------------------------
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.add_init_script(DENY_FULLSCREEN)
        open_audio_screen(page, base, service)
        page.keyboard.press('Space')
        page.wait_for_timeout(1000)
        denied = {'fullscreen': page.evaluate('() => Boolean(document.fullscreenElement)'),
                  'playing': playing_state(page)}
        for key in ['ArrowRight', 'Control+ArrowRight', 'Home']:
            before = active_screen(page)
            page.keyboard.press(key)
            page.wait_for_timeout(200)
            denied[key] = before != active_screen(page)
        page.mouse.click(1400, 450)   # the right mouse zone, still painted when fullscreen is refused
        page.wait_for_timeout(300)
        denied['mouse zone'] = active_screen(page) not in (None, '')
        moved_by_zone = active_screen(page)
        readings['fullscreen_refused'] = {'state': denied, 'screen_after_zone': moved_by_zone}
        check('FR-008 a refused fullscreen still locks keys and zones',
              denied['fullscreen'] is False and denied['playing'] == 'true'
              and not denied['ArrowRight'] and not denied['Control+ArrowRight']
              and not denied['Home'] and moved_by_zone == readings['audio_screen'],
              json.dumps(readings['fullscreen_refused']))
        page.keyboard.press('Space')
        page.wait_for_timeout(400)
        freed = active_screen(page)
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(300)
        check('FR-008 pausing gives the keys back',
              freed != active_screen(page), f"{freed} -> {active_screen(page)}")
        page.close()

        browser.close()

    return readings, checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:63404')
    parser.add_argument('--service', type=int, default=144)
    args = parser.parse_args()
    readings, checks = probe(args.base, args.service)
    print(json.dumps(readings, indent=2))
    print()
    for item in checks:
        print(('ok   ' if item['ok'] else 'FAIL ') + item['check'])
        if not item['ok']:
            print(f"      {item['detail'][:300]}")
    failed = [item for item in checks if not item['ok']]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks read as the spec says")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
