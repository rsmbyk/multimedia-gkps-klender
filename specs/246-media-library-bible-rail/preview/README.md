# Live preview — spec 246

URL: `http://127.0.0.1:8769/` (dev server started from this worktree; no deep links).

Steps:

1. Open `/`, then click the **Media Library** rail tile. The library stage paints; the sidebar is
   closed and the rail tile is current.
2. Click the **Alkitab** rail tile. With the fix the shell fetches `/bible/` and the sidebar shows
   its book rows; on the unmodified app at `http://127.0.0.1:63404/` this same click opens an empty
   panel with "No books yet." and makes no request.
3. Click **Kidung** (or **Tata Ibadah**) and then **Alkitab** again: both surfaces work, which is the
   workaround the report describes.
4. Click a section's own tile once it is on stage: it still toggles the panel without a fetch.

States reachable by hand: media library on stage · first section click · own-tile toggle ·
cross-section switch · direct `/media-library/` load. `preview/probe.py` prints the measured
before/after numbers against both servers at 1440×900, dark mode, 1×.
