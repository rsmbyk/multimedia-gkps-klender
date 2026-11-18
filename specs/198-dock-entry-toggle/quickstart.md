# Quickstart — spec 198 (the 2026-11-18 revision)

Repo: `~/Projects/multimedia-gkps-klender-198`, branch `feat/198-dock-entry-toggle`. Everything
runs through the compose stack; the web container mounts the repo live, so host edits are visible
without a rebuild. Static files are served from `static/` directly in dev — no `collectstatic`
needed locally.

## Serve the slice

```sh
cd ~/Projects/multimedia-gkps-klender-198
docker compose up -d web
# the dock: http://127.0.0.1:<web-port>/obs/dock   (docker compose port web 8000)
```

The approved preview (Gate 1) is static at `specs/198-dock-entry-toggle/preview/index.html` —
open it directly, or `python3 -m http.server 8137 --directory .` from the repo root.

## Run the tests

```sh
# fast lane (server-side; includes multimedia.web.test_obs_dock)
DB_PORT=57155 docker compose exec -T web python manage.py test \
  --exclude-tag=e2e --noinput -v 1

# this slice's E2E (Playwright; needs `playwright install chromium` in the container once)
DB_PORT=57155 docker compose exec -T web python manage.py test \
  tests.e2e.test_obs_dock --keepdb

# the seven projection suites the rewire touches
DB_PORT=57155 docker compose exec -T web python manage.py test \
  tests.e2e.test_display_session tests.e2e.test_display_session_refresh \
  tests.e2e.test_dock_goto tests.e2e.test_dock_keys \
  tests.e2e.test_obs_overlay tests.e2e.test_obs_overlay_wrap \
  tests.e2e.test_obs_dock --keepdb

# gates before delivery
DB_PORT=57155 docker compose exec -T web python manage.py check
DB_PORT=57155 docker compose exec -T web python manage.py makemigrations --check --dry-run
```

## The manual checks (steps a person follows; E2E covers the rest)

1. **The door** — open a service in the dock; click a non-live entry's header: the block morphs
   open over 230 ms, the chevron flips down, `aria-expanded` flips, and **nothing goes on air**
   (`gkps-display` untouched). Click again: it closes.
2. **The jump** — expand an entry, click one of its screen rows: exactly that screen goes on air,
   `aria-current` moves to it, the block stays open. The header click from step 1 never does this.
3. **The live row** — hover the on-air entry: selected tint, **no chevron**. Click its header:
   nothing happens — it cannot collapse. Put another entry on air; blocks you left open stay open,
   the departed entry's stored state applies again.
4. **Mid-crossing click** — during a crossing hand-off, click another entry's header: nothing
   tears; the request is recorded and lands when the morph settles (the block ends in its
   effective state). *This is the one timing feel only a human hand can judge — quickstart #4 IS
   the traceability table's `manual` row.*
5. **Breaks and empties** — a section break and a verse-less song render no chevron, ever; their
   header clicks do nothing.
6. **Reduced motion** — OS/browser `prefers-reduced-motion: reduce` (or the preview's checkbox):
   the swap is instant, the chevron flips without transition, no `is-morph` ever appears.
7. **Reload** — reload the dock: every hand-opened block is gone; only the live block is open;
   `gkps-display` is untouched.
8. **In OBS** — the dock runs inside OBS's browser source: the 230 ms morph feel, the chevron's
   vertical centring on the real header height, and the reduce path are checked there, on the
   operator's machine.

## Honest limits

- The static preview approximates reduce-motion with a checkbox; the real path is the OS setting
  (the E2E uses Playwright's `reduced_motion` context, which is the browser's real path).
- A service whose entries renumber between re-reads (an edit that adds/removes entries above a
  peeked one) re-keys that peek — accepted (research D003): overrides are session-scoped by
  design, and a renumbering re-read is a content edit.
- The mid-crossing queue (FR-009) is asserted structurally in code (inspection I3); its *feel*
  is manual check #4.
