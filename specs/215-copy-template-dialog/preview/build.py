"""Builds preview/index.html from the fragments the server actually sends.

`fragments.json` holds `#editorContent`'s innerHTML, read off the running dev
server for a service (304) and a template (151). The preview page puts those
verbatim into the dialog and adds only what this slice introduces: the copy
confirmation as a dialog of its own.

    .venv/bin/python specs/215-copy-template-dialog/preview/build.py
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[2]
fragments = json.loads((HERE / 'fragments.json').read_text())

# The two product sheets are copied, never retyped: a stale copy would let this page
# measure a stylesheet the product no longer serves.
for sheet in ('tokens.css', 'components.css'):
    (HERE / sheet).write_text((ROOT / 'static/styles/design' / sheet).read_text())


def clean(html):
    """Strip the things a static page must not carry: a real CSRF token, a form
    that would post to a server this page does not have, and the confirmation the
    server still renders inside the body — this slice replaces it, and the page
    carries the new one once, outside the two fragments."""
    html = re.sub(r'name="csrfmiddlewaretoken" value="[^"]*"',
                  'name="csrfmiddlewaretoken" value="PREVIEW"', html)
    html = html.replace(' method="post"', ' data-preview-form')
    html = re.sub(r' action="[^"]*"', '', html)
    cut = html.find('<div class="editor__confirm-layer"')
    if cut != -1:
        html = html[:cut].rstrip() + '\n</div>\n'
    return html


CONFIRM = """
      <!-- The slice's one new component. The product includes this inside
           .editor__body (reading/_editor_form.html); it is position: fixed, so
           where it sits in the tree changes nothing on screen. -->
      <div class="editor__confirm-layer" data-copy-confirm hidden>
        <div class="editor__confirm confirm--dialog" role="alertdialog" aria-modal="true"
             aria-labelledby="copyConfirmTitle" aria-describedby="copyConfirmLead">
          <h3 id="copyConfirmTitle">Copy as template?</h3>
          <p class="confirm__lead" id="copyConfirmLead">A new template from this Tata Ibadah —
            same entries, in the same order. The one you are editing does not change.</p>

          <div class="editor__field">
            <label for="copyName">Name</label>
            <input id="copyName" type="text" maxlength="64" autocomplete="off"
                   value="9 Agustus 2026 (Copy)" data-copy-name>
          </div>

          <ul class="confirm__facts">
            <li><strong>No service date.</strong> A template is not tied to a day.</li>
            <li><strong>Stays a template.</strong> It can never become a normal Tata Ibadah.</li>
            <li><strong>Can be copied again.</strong> Copying does not use it up.</li>
          </ul>

          <div class="editor__confirm-actions">
            <button type="button" class="editor__cancel" data-copy-cancel>Cancel</button>
            <button type="button" class="editor__save" data-copy-accept>Copy as template</button>
          </div>
        </div>
      </div>
"""

PAGE = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Copy as template — a dialog of its own</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
<link rel="stylesheet" href="preview.css">
</head>
<body>
<div class="pv">
  <header class="pv__bar">
    <div class="pv__tabs" role="tablist" aria-label="State">
      <button role="tab" data-state="edit" aria-selected="true">Edit modal</button>
      <button role="tab" data-state="confirm" aria-selected="false">Copy as template</button>
    </div>
    <div class="pv__right">
      <button class="pv__size" type="button" data-size-toggle>Service dialog</button>
      <button class="pv__theme" type="button" data-theme-toggle>Dark</button>
    </div>
  </header>

  <p class="pv__note" data-note></p>

  <div class="pv__stage">
    <div class="pv__page">
      <div class="pv__rail"></div>
      <div class="pv__list">
        <div class="pv__row"></div><div class="pv__row pv__row--sel"></div>
        <div class="pv__row"></div><div class="pv__row"></div><div class="pv__row"></div>
      </div>
      <div class="pv__canvas"></div>
    </div>
    <div class="pv__scrim"></div>

    <dialog class="editor pv__dialog" open>
      <div class="editor__content" id="editorContent">
        <div data-fragment="service">{service}</div>
        <div data-fragment="template" hidden>{template}</div>
{confirm}
      </div>
    </dialog>
  </div>

  <p class="pv__hint">1 edit modal · 2 copy dialog · <kbd>s</kbd> service/template dialog · <kbd>t</kbd> theme · <kbd>Esc</kbd> closes the copy dialog</p>
</div>
<script src="preview.js"></script>
</body>
</html>
"""

(HERE / 'index.html').write_text(
    PAGE.format(service=clean(fragments['service']),
                template=clean(fragments['template']),
                confirm=CONFIRM))
print('wrote', HERE / 'index.html')
