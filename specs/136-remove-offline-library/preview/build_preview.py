"""Spec 136 preview builder — the app without the offline library, and the Go To's loading states.

Takes the real pages the worktree's own server serves: `/home/` (the reading shell that carries the
rail) and `/projector?service=143` (the service projector with its corner cue, shortcuts button and
Go To panel). It removes the offline control, the offline panel and the offline scripts from the
reading page — the change itself — and applies the proposed loading state to the projector in three
files, one per way the state is reached.

The shell, rail, panels, stage, type, colours and words are the project's; only the removal and the
loading treatment are the proposal.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/136-remove-offline-library/preview/build_preview.py [base] [service]

Defaults: `http://127.0.0.1:8769`, `143`.
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8769').rstrip('/')
SERVICE = sys.argv[2] if len(sys.argv) > 2 else '143'
HERE = pathlib.Path(__file__).parent

# The proposal, as it would sit in projector.css: one spinner in the chosen row's
# count slot, one beside the shortcuts button. Both reuse the app's own spinner
# idiom (18px in the editor, 2px border, 800ms linear, off under reduced motion).
PROPOSAL = """
/* --- spec 136 preview: the Go To's loading state --- */
.projector-find__row.is-loading { cursor: progress; }
.projector-find__row.is-loading .projector-find__count { display: none; }
.projector-find__spinner,
.cue-loading {
  box-sizing: border-box; flex: none; border-radius: 50%;
  border: 2px solid var(--whisper); border-top-color: var(--quiet);
  animation: goto-load-spin 800ms linear infinite;
}
.projector-find__spinner { width: 12px; height: 12px; }
.cue-loading {
  position: absolute; z-index: 5; right: 74px; bottom: 25px;
  width: 14px; height: 14px;
}
@keyframes goto-load-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) {
  .projector-find__spinner, .cue-loading { animation: none; }
}
.projector-find input:disabled { color: var(--quiet); cursor: not-allowed; }
"""

REMOVE_READING = """() => {
  const gone = [];
  const drop = (sel, label) => {
    const node = document.querySelector(sel);
    if (node) { node.remove(); gone.push(label); }
  };
  drop('link[href*="offline.css"]', 'offline.css');
  drop('#offlineSyncButton', 'rail offline button');
  drop('#offlineSyncPanel', 'offline panel');
  drop('#offlineSavedSource', 'saved-copy label');
  document.querySelectorAll('script[src*="offline"]').forEach((node) => {
    node.remove(); gone.push(node.getAttribute('src'));
  });
  return gone;
}"""

STRIP_SCRIPTS = """() => {
  document.querySelectorAll('script').forEach((node) => node.remove());
}"""

OPEN_FIND = """() => {
  const panel = document.querySelector('#projectorFind');
  const dismiss = document.querySelector('#projectorFindDismiss');
  panel.hidden = false;
  panel.setAttribute('data-state', 'loading');
  dismiss.hidden = false;
  document.body.classList.add('find-open');
  document.querySelector('#projectorFindInput').disabled = true;
}"""


def relative_assets(html):
    """The previews are opened from disk: point every asset at the repo's own files."""
    return re.sub(r'(["\'(\s])(?:https?://[^/"\']+)?/static/', r'\1../../../static/', html)


def capture(page, url):
    page.goto(BASE + url, wait_until='networkidle')
    return page.content()


def write(path, html):
    (HERE / path).write_text(html, encoding='utf-8')
    print(f'wrote {path} ({len(html) / 1024:.1f} KB)')


def main():
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        # 1. The reading shell, with the offline feature gone.
        capture(page, '/home/')
        gone = page.evaluate(REMOVE_READING)
        print('removed from the reading page:', ', '.join(gone))
        page.evaluate(STRIP_SCRIPTS)
        write('after.html', relative_assets(page.content()))

        # 2. The projector, in the three ways the loading state is reached.
        capture(page, f'/projector?service={SERVICE}')
        page.evaluate(STRIP_SCRIPTS)
        page.add_style_tag(content=PROPOSAL)
        page.evaluate("""() => {
          const keys = document.querySelector('.keys');
          const spinner = document.createElement('span');
          spinner.className = 'cue-loading';
          spinner.setAttribute('role', 'status');
          spinner.setAttribute('aria-label', 'Loading');
          keys.parentNode.insertBefore(spinner, keys);
          document.querySelectorAll('script[type="application/json"]').forEach((n) => n.remove());
        }""")

        # 2a. G opened before the index arrived: the panel is up, asking nothing yet.
        page.evaluate(OPEN_FIND)
        page.evaluate("""() => {
          const row = document.querySelector('#projectorFindResults');
          row.classList.add('is-loading');
          row.disabled = true;
          document.querySelector('.projector-find__suggestion').textContent = 'Loading search\\u2026';
          document.querySelector('.projector-find__count').textContent = '0 / 0';
          const spinner = document.createElement('span');
          spinner.className = 'projector-find__spinner';
          spinner.setAttribute('aria-hidden', 'true');
          row.appendChild(spinner);
        }""")
        write('projector-index-loading.html', relative_assets(page.content()))
        page.goto(BASE + f'/projector?service={SERVICE}', wait_until='networkidle')
        page.evaluate(STRIP_SCRIPTS)
        page.add_style_tag(content=PROPOSAL)
        page.evaluate("""() => {
          const keys = document.querySelector('.keys');
          const spinner = document.createElement('span');
          spinner.className = 'cue-loading';
          spinner.setAttribute('role', 'status');
          spinner.setAttribute('aria-label', 'Loading');
          keys.parentNode.insertBefore(spinner, keys);
        }""")

        # 2b. A result chosen: the row holds the spinner, the field is locked, the cue waits.
        page.evaluate(OPEN_FIND)
        page.evaluate("""() => {
          const input = document.querySelector('#projectorFindInput');
          input.value = 'KJ 152';
          input.setAttribute('value', 'KJ 152');
          const row = document.querySelector('#projectorFindResults');
          row.classList.add('is-loading');
          row.disabled = true;
          document.querySelector('.projector-find__suggestion').textContent = 'KJ 152 Ada Kuasa';
          const count = document.querySelector('.projector-find__count');
          count.textContent = '1 / 1';
          const spinner = document.createElement('span');
          spinner.className = 'projector-find__spinner';
          spinner.setAttribute('aria-hidden', 'true');
          row.appendChild(spinner);
        }""")
        write('projector-selection-loading.html', relative_assets(page.content()))

        # 2d. The fetch failed: the state restores and the row says so.
        page.evaluate("""() => {
          const row = document.querySelector('#projectorFindResults');
          row.classList.remove('is-loading');
          row.disabled = false;
          document.querySelector('.projector-find__spinner').remove();
          document.querySelector('.projector-find__suggestion').textContent = 'Could not load \u2014 try again';
          const count = document.querySelector('.projector-find__count');
          count.textContent = '1 / 1';
          document.querySelector('#projectorFindInput').disabled = false;
          document.querySelector('.cue-loading').remove();
        }""")
        write('projector-selection-error.html', relative_assets(page.content()))

        # 2c. A chapter crossing: the panel is closed, the cue carries the wait.
        page.goto(BASE + f'/projector?service={SERVICE}', wait_until='networkidle')
        page.evaluate(STRIP_SCRIPTS)
        page.add_style_tag(content=PROPOSAL)
        page.evaluate("""() => {
          const keys = document.querySelector('.keys');
          const spinner = document.createElement('span');
          spinner.className = 'cue-loading';
          spinner.setAttribute('role', 'status');
          spinner.setAttribute('aria-label', 'Loading');
          keys.parentNode.insertBefore(spinner, keys);
        }""")
        write('projector-chapter-loading.html', relative_assets(page.content()))

        browser.close()


if __name__ == '__main__':
    main()
