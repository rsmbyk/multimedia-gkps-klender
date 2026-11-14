"""Spec 132 preview probe — what the Tata Ibadah sidebar's buckets look like.

Opens the running worktree, reads the dated list's groups in order, prints each
heading, its row count, the first and last row, and the heading's drawn form; then
saves a screenshot of the panel at 1440x900.

    /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
        specs/132-tatib-sidebar-date-buckets/preview/probe_date_buckets.py [url] [out.png]
"""
import sys

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8766/tatib/'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/tmp/tatib-132-panel.png'

READ = """() => {
  const groups = [...document.querySelectorAll('#panelBody .group')];
  return groups.map(group => {
    const head = group.querySelector('.group__head');
    const rows = [...group.querySelectorAll('.book .book__n')].map(n => n.textContent.trim());
    const style = head ? getComputedStyle(head) : null;
    return {
      bucket: group.dataset.bucket || '',
      text: head ? head.textContent.trim() : null,
      drawn: style ? style.textTransform : null,
      size: style ? style.fontSize : null,
      position: style ? style.position : null,
      rows: rows.length,
      first: rows[0] || null,
      last: rows[rows.length - 1] || null,
    };
  });
}"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(URL, wait_until='networkidle')
        groups = page.evaluate(READ)
        for group in groups:
            print(f"{group['bucket'] or '(none)':18} {group['text']!r:22} "
                  f"drawn={group['drawn']} {group['size']} {group['position']} "
                  f"rows={group['rows']:3} first={group['first']!r} last={group['last']!r}")
        # The divider between two groups, measured rather than assumed.
        divider = page.evaluate("""() => {
          const groups = [...document.querySelectorAll('#panelBody .group')];
          const second = groups[1];
          if (!second) return null;
          const style = getComputedStyle(second);
          return {border: style.borderTopWidth, margin: style.marginTop, padding: style.paddingTop};
        }""")
        print('divider between groups 1 and 2:', divider)
        page.screenshot(path=OUT)
        print('screenshot:', OUT)
        browser.close()


if __name__ == '__main__':
    main()
