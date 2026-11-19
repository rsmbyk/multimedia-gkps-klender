"""Assemble the static preview for spec 204 from the product's own materials.

Inputs (all captured or copied, nothing hand-drawn):
  fixtures/dock-rendered.html   the real /obs/dock page, as the server renders it
  fixtures/service-N.json       the real entry/screen islands of each service
  static/styles/design/*.css    the product's tokens and dock stylesheet
  static/web/*.js               the product's display-session, display and dock scripts

Output: index.html + assets/. The dock's own script carries ONE added line — the
drafted reset in openService(), gated on window.__openReset so the same page can run
today's rule for comparison. Nothing else in the product's code or CSS is edited.

Run from the repo root:
    .venv/bin/python specs/204-dock-entry-open-reset/preview/build.py
"""
import json
import os
import re
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FIX = os.path.join(HERE, 'fixtures')
ASSETS = os.path.join(HERE, 'assets')

CSS = ['tokens.css', 'obs-dock.css']
JS = ['display-session.js', 'display.js', 'obs-dock.js', 'projector-library.js']
IMG = ['gkps.png']

RESET_LINE = (
    "    /* PREVIEW ONLY (spec 204): the drafted reset, gated so this page can also run\n"
    "       today's rule. The slice's own line is unconditional. */\n"
    "    if (window.__openReset !== false) entryOverrides.clear();\n"
)


def read(path):
    with open(path, encoding='utf-8') as handle:
        return handle.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)


manifest = json.loads(read(os.path.join(FIX, 'manifest.json')))
services = manifest['services']
keep = {s['service'] for s in services}
base_sha = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', 'origin/develop'],
                          capture_output=True, text=True, check=True).stdout.strip()

html = read(os.path.join(FIX, 'dock-rendered.html'))

# 1. the product's own asset URLs, pointed at the copies beside this page
html = re.sub(r'/static/(styles/design|web|assets)/', r'./assets/', html)

# 2. the picker keeps the services whose payloads were captured; empty buckets go
row_re = re.compile(r'<li>\s*<button type="button" class="servicerow".*?</li>', re.S)


def keep_row(match):
    sid = re.search(r'data-service="(\d+)"', match.group(0))
    return match.group(0) if sid and sid.group(1) in keep else ''


html = row_re.sub(keep_row, html)
section_re = re.compile(r'<section data-bucket="[^"]*">.*?</section>', re.S)
html = section_re.sub(lambda m: m.group(0) if '<li>' in m.group(0) else '', html)

# 3. the panel sits in a frame so the review rail can stand beside it
start = html.index('<main class="dock"')
end = html.index('</main>') + len('</main>')
html = html[:start] + '<div class="dockframe">\n' + html[start:end] + '\n</div>' + html[end:]

# 4. preview chrome: the rail's stylesheet, the payloads, the shim, the rail itself
html = html.replace('<link rel="stylesheet" href="./assets/obs-dock.css">',
                    '<link rel="stylesheet" href="./assets/obs-dock.css">\n'
                    '<link rel="stylesheet" href="./preview.css">')

payloads = {s['service']: json.loads(read(os.path.join(FIX, f'service-{s["service"]}.json')))
            for s in services}
island = ('<script id="previewPayloads" type="application/json">'
          + json.dumps(payloads, ensure_ascii=False).replace('</', '<\\/')
          + '</script>')
html = html.replace('<script src="./assets/display-session.js"></script>',
                    island + '\n<script src="./shim.js"></script>\n'
                    '<script src="./assets/display-session.js"></script>')

buttons = '\n    '.join(
    f'<button type="button" data-open="{s["service"]}">Open “{s["name"][:18]}”'
    f' ({s["entries"]})</button>' for s in services)
rail = read(os.path.join(HERE, 'rail.html')).replace('{{BASE_SHA}}', base_sha) \
                                            .replace('{{SERVICE_BUTTONS}}', buttons)
html = html.replace('<script src="./assets/obs-dock.js"></script>',
                    '<script src="./assets/obs-dock.js"></script>\n' + rail +
                    '\n<script src="./rail.js"></script>')
html = html.replace('<title>', '<title>[preview 204] ', 1)
write(os.path.join(HERE, 'index.html'), html)

# 5. the assets: byte copies, except the dock script's one gated line
os.makedirs(ASSETS, exist_ok=True)
for name in CSS:
    shutil.copyfile(os.path.join(ROOT, 'static/styles/design', name), os.path.join(ASSETS, name))
for name in IMG:
    shutil.copyfile(os.path.join(ROOT, 'static/assets', name), os.path.join(ASSETS, name))
for name in JS:
    text = read(os.path.join(ROOT, 'static/web', name))
    if name == 'obs-dock.js':
        anchor = '  function openService(id, name, date) {\n'
        if anchor not in text:
            raise SystemExit('openService anchor not found — re-read the product script')
        if 'entryOverrides.clear();' in text:
            # Implement has landed: the product's own unconditional clear becomes the
            # preview's gated one, so the page still runs both rules from the same code.
            text = text.replace('    entryOverrides.clear();\n',
                                '    if (window.__openReset !== false) entryOverrides.clear();\n',
                                1)
        else:
            text = text.replace(anchor, anchor + RESET_LINE, 1)
    write(os.path.join(ASSETS, name), text)

print('built index.html from develop', base_sha)
print('services:', ', '.join(f'{s["service"]} ({s["entries"]} entries)' for s in services))
print('picker rows kept:', len(row_re.findall(html)))
