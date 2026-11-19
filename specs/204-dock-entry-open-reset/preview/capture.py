"""Capture the real dock page and the real service payloads the preview runs on.

The preview is static: it carries the product's own rendered markup, stylesheets and
scripts, and the entry/screen islands exactly as `/projector?service=N` serves them.
Only the network is stubbed — the dock's own parse path runs unchanged.

Run from the repo root with the project venv:
    .venv/bin/python specs/204-dock-entry-open-reset/preview/capture.py [base-url]
"""
import json
import os
import re
import sys
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:63404').rstrip('/')
HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, 'fixtures')
SERVICES = ['155', '149', '142', '144', '145']


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as response:
        return response.read().decode('utf-8')


def island(html, element_id):
    match = re.search(
        r'<script[^>]*id="' + element_id + r'"[^>]*>(.*?)</script>', html, re.S)
    if not match:
        raise SystemExit(f'island {element_id} not found')
    return json.loads(match.group(1))


os.makedirs(FIX, exist_ok=True)
dock = get('/obs/dock')
with open(os.path.join(FIX, 'dock-rendered.html'), 'w', encoding='utf-8') as handle:
    handle.write(dock)

manifest = []
for sid in SERVICES:
    html = get('/projector?service=' + sid)
    data = {'entries': island(html, 'projectorEntryData'),
            'screens': island(html, 'projectorScreenData')}
    with open(os.path.join(FIX, f'service-{sid}.json'), 'w', encoding='utf-8') as handle:
        json.dump(data, handle, ensure_ascii=False)
    row = re.search(r'data-service="' + sid + r'" data-name="([^"]*)"\s*\n?\s*data-date="([^"]*)"',
                    dock)
    kinds = {}
    for entry in data['entries']:
        kinds[entry.get('type')] = kinds.get(entry.get('type'), 0) + 1
    manifest.append({'service': sid,
                     'name': row.group(1) if row else '',
                     'date': row.group(2) if row else '',
                     'entries': len(data['entries']),
                     'screens': len(data['screens']),
                     'kinds': kinds})
    print(sid, manifest[-1]['name'][:30], len(data['entries']), 'entries',
          len(data['screens']), 'screens', kinds)

with open(os.path.join(FIX, 'manifest.json'), 'w', encoding='utf-8') as handle:
    json.dump({'base': BASE, 'services': manifest}, handle, ensure_ascii=False, indent=1)
print('captured from', BASE)
