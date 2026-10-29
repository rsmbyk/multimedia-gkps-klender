# Fold: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets` · 2026-10-28

## Capabilities touched

| capability | operations | before | after |
| --- | --- | --- | --- |
| `reading` | 2 × `added` (`R22`, `R23`) | 21 requirements | 23 requirements |

The numbers are not the ones this slice drafted: `R20` and `R21` were taken on `develop` while it was in
review (specs 147 and 145 folded first), so the delta lands as `R22` and `R23`, and the card is `ITEM-158`
for the same reason (`ITEM-155` had gone to spec 147). A requirement number and a card ID are claimed when
they land, not when they are written.

No `modified`, no `removed`, no `renamed`. `R9` — the Tata Ibadah list's own buckets — is the requirement
this slice borrows its windows and words from, and it is unchanged: the Media Library takes the same three
labels, and the transfer history takes those three plus two rungs of its own.

## What was written

**`R22` — The Media Library list groups by age, not by upload day.** Added as a full block with six
scenarios (the three buckets · the edges · early January · the sort · a filtered bucket · the row). It
fixes the three buckets to `R9`'s windows and words, the present day to `Asia/Jakarta`, the heading to the
list's existing `h2.media-library__group` with a `data-bucket`, and the two interactions the old per-day
heading never had: a size sort draws no heading, and an ascending sort reverses the buckets.

**`R23` — The transfer history groups by age, with today and the last week split out.** Added as a full
block with six scenarios (the five rungs · the edges · a running transfer · the rail · an undatable row ·
the empty history). It states the two extra rungs as rolling windows measured from the draw, dates a row by
its start, keeps active-first inside a bucket, gives the heading its `h3` and its keys, and keeps the rail
a progress popover with no headings.

## Header

`last folded` stays 2026-10-28 (the file was folded earlier the same day by spec 143); this slice is
prepended to the `slices` list.

## Accepted gaps

None — the one Converge finding (`C1`, the `Unused` half of `R22`'s filter rule unexercised) was closed
with a test before this fold, so nothing is held back as `not folded — accepted gap`.

## Behaviour the delta declines to claim

- The Media Library still has no saved copy, so `R22` carries no saved-renderer clause; the file's earlier
  saved-copy requirements remain retired as that file's own note says.
- The rail's flyout is stated by exclusion in `R23` (no headings) rather than given a requirement of its
  own: its active-row and seen-divider behaviour already shipped under spec 113's surface and did not
  change here.
