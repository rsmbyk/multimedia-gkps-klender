"""What a projector advance costs, measured on two builds side by side.

The change is the time between the operator's key press and the first frame that can
show the new screen, so this measures the key's own handling -- the work that stands
between the press and the paint -- and the layout reads the fitting spends doing it.
Both builds are served from a checkout of the same service; only the slice's
`static/web/projector.js` differs.

    <venv>/bin/python specs/219-projector-fit-cost/preview/probe.py \
        --develop http://127.0.0.1:63404 --slice http://127.0.0.1:8791 --service 144

Two cadences, because the slice fits the screens either side of the one showing in idle
time: `paced` leaves 250 ms between presses, which is how an operator advances on the
beat of the liturgy and enough idle time for that work to run; `rapid` presses with no
gap at all, so nothing can run in between and every screen must be fitted on arrival.
`paced` is the number the operator feels; `rapid` is the floor the slice cannot go below.
"""
import argparse
import json
import statistics

from playwright.sync_api import sync_playwright

SETUP = """() => {
  const proto = Element.prototype;
  window.__probe = {sizes: {}, times: [], probes: [], done: false};
  window.__orig = {s: Object.getOwnPropertyDescriptor(proto, 'scrollHeight'),
                   c: Object.getOwnPropertyDescriptor(proto, 'clientHeight')};
  window.__n = 0;
  Object.defineProperty(proto, 'scrollHeight', {configurable: true,
    get() { window.__n += 1; return window.__orig.s.get.call(this); }});
  Object.defineProperty(proto, 'clientHeight', {configurable: true,
    get() { window.__n += 1; return window.__orig.c.get.call(this); }});
  document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));
  return 'ready';
}"""

STEP = """() => {
  const screens = [...document.querySelectorAll('#projectorScreens .screen[data-screen]')];
  const before = Number(document.body.dataset.currentScreen);
  if (!screens[before + 1]) { window.__probe.done = true; return null; }
  window.__n = 0;
  const started = performance.now();
  document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));
  const took = +(performance.now() - started).toFixed(2);
  const index = Number(document.body.dataset.currentScreen);
  const lines = screens[index].querySelector('.screen__lines');
  window.__probe.times.push(took);
  if (lines) {
    window.__probe.sizes[index] = parseFloat(getComputedStyle(lines).fontSize);
    window.__probe.probes.push(window.__n);
  }
  return took;
}"""

RESTORE = """() => {
  const proto = Element.prototype;
  Object.defineProperty(proto, 'scrollHeight', window.__orig.s);
  Object.defineProperty(proto, 'clientHeight', window.__orig.c);
  return 'restored';
}"""


def measure(page, url, service, gap):
    page.goto(f'{url}/projector?service={service}')
    page.wait_for_load_state('networkidle')
    page.wait_for_selector('.screen.is-active')
    page.evaluate(SETUP)
    while not page.evaluate('() => window.__probe.done'):
        page.evaluate(STEP)
        if gap:
            page.wait_for_timeout(gap)
    probe = json.loads(page.evaluate('() => JSON.stringify(window.__probe)'))
    page.evaluate(RESTORE)
    return probe


def summary(times):
    times = sorted(value for value in times if value > 0)
    return {
        'n': len(times),
        'median': round(statistics.median(times), 2),
        'mean': round(statistics.mean(times), 2),
        'p90': round(times[int(len(times) * 0.9)], 2),
        'max': round(times[-1], 2),
    }


def report(name, probe):
    stats = summary(probe['times'])
    probes = probe['probes']
    print(f'  {name:8} median {stats["median"]:6}  mean {stats["mean"]:6}  '
          f'p90 {stats["p90"]:6}  worst {stats["max"]:7}  '
          f'| reads per advance  mean {statistics.mean(probes):6.1f}  worst {max(probes):4}  '
          f'| screens with words {len(probes)}')
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--develop', required=True, help='the build without the change')
    parser.add_argument('--slice', required=True, help='the build with the change')
    parser.add_argument('--service', default='144', help='the service id both builds show')
    parser.add_argument('--gap', type=int, default=250, help='milliseconds between presses')
    args = parser.parse_args()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        print(f'paced advance, {args.gap} ms between presses (the operator on the beat):')
        develop_paced = measure(page, args.develop, args.service, args.gap)
        report('develop', develop_paced)
        slice_paced = measure(page, args.slice, args.service, args.gap)
        report('slice', slice_paced)

        print('rapid advance, no gap (nothing can be fitted ahead of time):')
        develop_rapid = measure(page, args.develop, args.service, 0)
        report('develop', develop_rapid)
        slice_rapid = measure(page, args.slice, args.service, 0)
        report('slice', slice_rapid)
        browser.close()

    for label, develop, sliced in (('paced', develop_paced, slice_paced),
                                   ('rapid', develop_rapid, slice_rapid)):
        shared = sorted(set(develop['sizes']) & set(sliced['sizes']))
        differs = [key for key in shared if develop['sizes'][key] != sliced['sizes'][key]]
        # develop fits the arriving screen while the arrival morph is still running, so its
        # arrival size is not the size a screen rests at; a difference here is expected and
        # is not a regression. The comparison that matters is against develop's AT-REST
        # size, which `verify_sizes.py` makes.
        print(f'{label}: screens compared {len(shared)}  arrival sizes differing from '
              f'develop\'s mid-morph fit {len(differs)} '
              f'(compare at rest with verify_sizes.py)')


if __name__ == '__main__':
    main()
