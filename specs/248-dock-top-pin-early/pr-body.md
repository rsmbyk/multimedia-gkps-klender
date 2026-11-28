Spec 248 — the runner's live header now pins at the top as soon as the header itself reaches the fold, mirroring spec 208's bottom pin. The clone takes over from the sticky header at 0 px with no hop; while it owns the edge the source is hidden, so exactly one header is painted.

Measured on the live dock (420 × 860, dark, 1×): first pin moved from scrollTop 1164 to 1056 (108 px earlier); takeover at `blockTop = -2 px` with the real header and the clone both at 0 px; 490 probe frames with 0 boundary mismatches. The bottom pin, NEXT band, go-to strip, click act and reduced-motion path are unchanged.

Verification: 9 test · 4 inspection · 1 manual. New E2E module 7/7 (two cases proven red on unmodified develop), dock pin regression modules 23/23. The full browser matrix is deferred to the push step by repo convention.

Folded `dock/R19` as modified (19 requirements unchanged, scenarios 75 → 76). One carried-over Go To claim was found false on develop as well; it is kept as an explicit retraction in research D006.

Done: ITEM-265 (anchor issue #639), closed in the pre-merge delivery commit with `bump: patch`; VERSION 1.37.8 and the changelog line land in that commit, release_version stays empty until release.

Push-step `tests.e2e`: 971 tests, 34 failures / 52 errors. The dock-follow error and sampled text-wrap, media-bucket and tatib failures reproduce identically on unmodified develop at c72b5ee3; the four dock modules touched or adjacent to this slice pass 32/32 after integrating develop. Vercel's deployment check is failing for its own account-billing reason, not a build result.

Refs #639
