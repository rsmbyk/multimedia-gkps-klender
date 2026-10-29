"""Read the audio projector screen's own numbers off the live route (spec 156).

    # from the slice's worktree, with its server on 8815:
    python specs/156-audio-play-indicator/preview/measure.py [base-url] [service]

It walks to the service's first audio entry, then reports the play/pause control, the seek bar and the
times in the three states the requirement names — paused, playing, and playing-idle — at three
viewports. Every number in the spec's `## UI/UX` comes from this script.
"""
import json
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8815'
SERVICE = sys.argv[2] if len(sys.argv) > 2 else '144'
VIEWPORTS = [(1920, 1200), (1280, 800), (640, 480)]

BOX = '''(el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const b = getComputedStyle(el, '::before');
    return {
        w: +r.width.toFixed(2), h: +r.height.toFixed(2),
        x: +r.left.toFixed(2), y: +r.top.toFixed(2),
        opacity: cs.opacity, radius: cs.borderRadius, background: cs.backgroundColor,
        glyph: { content: b.content, w: b.width, h: b.height, borderLeft: b.borderLeftWidth },
    };
}'''


def read(page, selector):
    element = page.locator(selector).first
    return element.evaluate(BOX) if element.count() else None


def at_audio(page, base, service):
    page.goto(f'{base}/projector?service={service}', wait_until='networkidle')
    page.keyboard.press('Space')
    page.wait_for_timeout(300)
    for _ in range(8):
        if page.locator('.screen.is-active .screen__audio-player').count():
            break
        page.keyboard.press('Control+ArrowRight')
        page.wait_for_timeout(250)
    page.wait_for_selector('.screen.is-active .screen__audio-player', timeout=8000)
    page.wait_for_timeout(1500)


def main():
    report = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for width, height in VIEWPORTS:
            page = browser.new_page(viewport={'width': width, 'height': height})
            at_audio(page, BASE, SERVICE)
            key = f'{width}x{height}'
            state = {'paused': {}}
            for name, selector in {
                'play': '.screen.is-active .screen__audio-play',
                'seek': '.screen.is-active .screen__audio-seek',
                'times': '.screen.is-active .screen__audio-times',
                'player': '.screen.is-active .screen__audio-player',
            }.items():
                state['paused'][name] = read(page, selector)
            state['paused']['dataPlaying'] = page.locator(
                '.screen.is-active .screen__audio-play').get_attribute('data-playing')

            page.locator('.screen.is-active .screen__audio-play').click()
            page.wait_for_timeout(900)
            state['playing'] = {
                'play': read(page, '.screen.is-active .screen__audio-play'),
                'dataPlaying': page.locator('.screen.is-active .screen__audio-play').get_attribute('data-playing'),
                'elapsed': page.locator('.screen.is-active [data-audio-elapsed]').inner_text(),
            }

            page.wait_for_timeout(4200)
            state['idle'] = {
                'play': read(page, '.screen.is-active .screen__audio-play'),
                'seek': read(page, '.screen.is-active .screen__audio-seek'),
                'times': read(page, '.screen.is-active .screen__audio-times'),
                'dataPlaying': page.locator('.screen.is-active .screen__audio-play').get_attribute('data-playing'),
                'classes': page.locator('.screen.is-active .screen__audio-box').get_attribute('class'),
            }

            # any activity brings the chrome back; then the control is clickable again
            page.mouse.move(int(width / 2), int(height - 120))
            page.wait_for_timeout(500)
            state['returned'] = {
                'play': read(page, '.screen.is-active .screen__audio-play'),
                'seek': read(page, '.screen.is-active .screen__audio-seek'),
                'classes': page.locator('.screen.is-active .screen__audio-box').get_attribute('class'),
            }

            page.locator('.screen.is-active .screen__audio-play').click()
            page.wait_for_timeout(600)
            state['pausedAgain'] = {
                'play': read(page, '.screen.is-active .screen__audio-play'),
                'dataPlaying': page.locator('.screen.is-active .screen__audio-play').get_attribute('data-playing'),
                'classes': page.locator('.screen.is-active .screen__audio-box').get_attribute('class'),
            }
            report[key] = state
            page.close()
        browser.close()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
