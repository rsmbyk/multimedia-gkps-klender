# Spec 253 preview — Use template progress

Self-contained static preview assembled from the repo's own `tokens.css`, `generate.css` and
`components.css` plus the real `_generate_modal.html` class anatomy. Open `index.html` in a browser;
`::preview` in chat renders it but the sandbox has no `sessionStorage`, so the persistence readout
only works from a real file URL.

- `index.html` — generated, self-contained page. Do not hand-edit.
- `build_preview.py` — rebuilds `index.html` from the repo CSS and the markup below.
- `probe.py` — Playwright behaviour probe; run with the repo venv python.

## Measured (Playwright, 1440×1000, dark, 1×)

- Confirm card: **347.5 × 184.6 px**, at x 49, y 321.7 inside the 840 × 760 modal sheet.
- Layer: `inset: 0`, 24px padding, `z-index: 6`; card `padding: 20px 22px 18px`, radius 12px.
- Title `650 17px/1.3`, body `400 13px/1.5`, action gap 8px, action top margin 8px.
- Zero console errors; all 10 behaviour assertions pass.

## States reachable by hand

1. **Clean** — open template A or B with no saved progress; Cancel closes with no confirm.
2. **Dirty** — press **Set** on a slot or **Choose** then pick an option. The sessionStorage readout
   shows `gkps:generate:<id>` written immediately.
3. **Confirm** — press Cancel, click outside, or Escape. The layer reads "Your progress is saved in
   this browser session… pick up where you left off", with **Stay** and **Leave**.
4. **Stay** — dismiss the layer; the modal and settled rows remain.
5. **Leave** — close; reopen the same template and the settled rows, step, name and date return.
6. **Reload** — reload the page then reopen the template; progress is still there.
7. **Independent templates** — open B while A has progress; B starts empty. Switch back to A; its
   progress returns.
8. **Create** — on step 2, press Create; that template's saved progress is cleared and the next open
   starts empty. A failed Create (not simulated here) keeps it.
9. **Session boundary** — press **Clear session**, or close and reopen the browser; all progress is
   gone.
