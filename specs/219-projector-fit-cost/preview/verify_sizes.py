"""The sizes the slice shows, against the sizes develop shows at rest.

Develop fits the arriving screen while the arrival morph is still running, so it measures
the words 14 px lower than they come to rest and picks a size that is too small; the same
screen fitted by a resize lands on a larger one. The slice fits at rest, so its advance
must agree with develop's *resize* on every screen -- and with develop's advance only
where the morph made no difference.

    <venv>/bin/python specs/219-projector-fit-cost/preview/verify_sizes.py \
        --develop http://127.0.0.1:63404 --slice http://127.0.0.1:8791 --service 144
"""
import argparse
import json

from playwright.sync_api import sync_playwright

ARRIVE = """() => {
  const screens = [...document.querySelectorAll('#projectorScreens .screen[data-screen]')];
  const before = Number(document.body.dataset.currentScreen);
  if (!screens[before + 1]) return null;
  document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));
  const index = Number(document.body.dataset.currentScreen);
  const lines = screens[index].querySelector('.screen__lines');
  if (!lines) return {screen: index, arrival: null, resized: null};
  const arrival = parseFloat(getComputedStyle(lines).fontSize);
  window.dispatchEvent(new Event('resize'));
  return {screen: index, arrival: arrival,
          resized: parseFloat(getComputedStyle(lines).fontSize)};
}"""


def walk(page, url, service):
    page.goto(f'{url}/projector?service={service}')
    page.wait_for_load_state('networkidle')
    page.wait_for_selector('.screen.is-active')
    page.evaluate("() => document.dispatchEvent("
                  "new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}))")
    seen = {}
    while True:
        step = page.evaluate(ARRIVE)
        if step is None:
            return seen
        if step['arrival'] is not None:
            seen[step['screen']] = step


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--develop', required=True)
    parser.add_argument('--slice', required=True)
    parser.add_argument('--service', default='144')
    args = parser.parse_args()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        develop = walk(page, args.develop, args.service)
        sliced = walk(page, args.slice, args.service)
        browser.close()

    shared = sorted(set(develop) & set(sliced))
    morph = [key for key in shared if develop[key]['arrival'] != develop[key]['resized']]
    off_rest = [key for key in shared if develop[key]['resized'] != sliced[key]['arrival']]
    print(f'screens compared {len(shared)}')
    print(f'develop fits an advance smaller than its own resize on {len(morph)} screens')
    print(f'slice advance differs from develop resize on {len(off_rest)} screens')
    for key in off_rest[:8]:
        print(f'  screen {key}: develop resize {develop[key]["resized"]}px, '
              f'slice {sliced[key]["arrival"]}px')
    print('sample:', json.dumps({key: develop[key] for key in shared[:3]}))


if __name__ == '__main__':
    main()
