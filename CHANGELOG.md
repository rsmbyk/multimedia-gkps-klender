# Changelog

How versioning works (single SemVer from `0.5.0`, area labels, and release
timing) is documented in [`docs/VERSIONING.md`](docs/VERSIONING.md).

Sections `0.4.x` and earlier use the legacy per-app **App Versions** blocks;
keep them as history. New releases use one SemVer and area labels only.

---

## Unreleased

### Changes

- `[test]` Add current-state regression coverage for API (songs, bookmarks,
  tatib, bible, search), shared helpers, OBS BroadcastChannel/storage/hotkeys,
  and isolatable web contracts; pytest uses Compose Postgres via host `:5433`.
- `[fix]` Exclude the current bookmark from name+date uniqueness on update;
  scope tatib `insert_after` order shifts to the same tata ibadah.
- `[docs]` Adopt lightweight docs-native Spec-Driven Development (`docs/SDD.md`,
  `specs/` layout, Cursor rule); SDD sits above TDD for in-scope product work.
- `[docs]` Adopt Git Flow, TDD toolchain docs, and single-SemVer versioning
  (first tagged release under the new scheme will be `0.5.0`).
- `[docs, deploy]` Add production deploy runbook for the working Vercel + `main`
  setup (legacy `vercel.json` routing, env vars, static files, landmines).
- `[deploy, docker]` Make Docker Compose the only local app runtime with a
  built-in Postgres service; remove `docker-compose.local.yml` and stop pointing
  local `.env` at Neon.
- `[dj]` Remove `DJANGO_DEVELOPMENT_MODE` / app SQLite; require `DATABASE_URL`
  and `DJANGO_SECRET_KEY`, and refuse `DJANGO_DEBUG=True` when `VERCEL` is set.
- `[docs, test]` Document Docker-only local workflow; add env-safety unit tests.
- `[docker]` Add `scripts/copy_neon_to_local.sh` to dump Neon into Compose Postgres.

---

## Version `0.4.17`

### App Versions

- Django: `v0.4.dj11`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj11]` Restored `vercel.json` WSGI routing after zero-config deploy produced Vercel 404s with no runtime logs.

---

## Version `0.4.16`

### App Versions

- Django: `v0.4.dj10`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj10]` Removed legacy `vercel.json` `builds` config; Vercel now uses zero-configuration Django detection via `manage.py`.

---

## Version `0.4.15`

### App Versions

- Django: `v0.4.dj9`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj9]` Dropped failing Vercel `build.sh` static-build step; serve static files via WhiteNoise finders on Vercel and raised the lambda size limit.

---

## Version `0.4.14`

### App Versions

- Django: `v0.4.dj8`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj8]` Restored legacy Vercel `builds` routing and added `build.sh` to run `collectstatic` into `_static` for CDN serving.

---

## Version `0.4.13`

### App Versions

- Django: `v0.4.dj7`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj7]` Fixed production 500 by running `collectstatic` on Vercel (legacy `builds` config skipped it) and serving static assets from the CDN with manifest storage.

---

## Version `0.4.12`

### App Versions

- Django: `v0.4.dj6`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj6]` Auto-allow Vercel deployment hosts (`*.vercel.app`, `VERCEL_URL`) so production no longer returns Django 400 Bad Request.

---

## Version `0.4.11`

### App Versions

- Django: `v0.4.dj5`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj5]` Aligned Vercel Python pin with the platform default (3.12) after 3.11 conflicted with auto-generated `requires-python`; kept `psycopg2-binary` 2.9.9 and bumped PyYAML for wheel compatibility.

---

## Version `0.4.10`

### App Versions

- Django: `v0.4.dj4`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj4]` Fixed Vercel production build by pinning Python 3.11 and upgrading `psycopg2-binary` to a version with prebuilt wheels.

---

## Version `0.4.9`

### App Versions

- Django: `v0.4.dj3`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[dj3]` Merged `railway-migration` production deployment config (WhiteNoise static files, Railway/Vercel WSGI entrypoint, `vercel.json`).
- `[dj3]` Restored safe local defaults for `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS` while keeping production overrides via environment variables.

---

## Version `0.4.8`

### App Versions

- Django: `v0.4.dj2`
- Bible: `v0.4.b11`
- Songs: `v0.4.s30`
- Tatib: `v0.4.t21`
- Project: `v0.4.p13`

### Changes

- `[b11, s30, t21, p13]` Restored dock and project navigation hotkeys after BehaviorSubject and hotkeys-js regressions.
- `[s30]` Fixed songbooks dropdown stuck on Loading when API responses did not reach the UI.
- `[dj2]` Added Docker Compose setup for local development with optional Postgres.
- `[dj2]` Fixed container entrypoint execution on Windows-shared-folder CRLF line endings.
- `[dj2]` Read Django ALLOWED_HOSTS from `.env` so LAN devices can reach the app during testing.

---

## Version `0.4.6`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b10`
- Songs: `v0.4.s29`
- Tatib: `v0.4.t20`
- Project: `v0.4.p12`

### Changes

- `[b8, s29, t20, p11]` Added a feature to switch control between apps from Project's source page.
- `[b9]` Added a dropdown in Bible's display tab to switch language between Indonesian and Simalungun.
- `[b10]` The corresponding Chapter will also be opened in Browse tab when selecting Verse from History tab.
- `[p12]` Added a page to configure Project's source styles (colours and possibly other settings in the future).

---

## Version `0.4.5`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b7`
- Songs: `v0.4.s28`
- Tatib: `v0.4.t19`
- Project: `v0.4.p10`

### Changes

- `[b4, s19, t12, p7]` Dock can now be controlled from Project's source page.
- `[b5, s20, t13, p8]` Fixed an error where Project's source cannot be activated while opening multiple page of Project's source.
- `[b6, s21, t14]` ToggleButton will not execute its onActive and onInactive if the state it change into would not change'.
- `[s22, t15]` Songs info and Tatib item won't be broadcasted if the Dock is inactive.
- `[s23]` Changed the order of which the SongInfo are broadcasted to increase consistency when changing lyric.
- `[p9]` Changed the order of which the transition is done to hide the flickering when resizing texts.
- `[t16]` TatibItem of type End of Section and End of Tatib will not be broadcasted anymore and will be replaced with empty texts instead.
- `[b7, s24, t17]` Fixed ToggleButton not being initialized properly due to bad initial active state initialization order.
- `[p10]` Changed background colour of Project's source.
- `[s25]` Fixed a bug where Bookmark item in Bookmark tab not being updated when displaying a single Song.
- `[s26]` Added a feature to reactivate Bookmark after displaying individual Songs.
- `[s27]` Allowed empty name, allowed some symbols, and increase max length on Bookmark's name.
- `[t18]` Allowed some symbols and increase max length on Tatib's name.
- `[s28, t19]` Reworded Bookmark's and Tatib's Name input field regexes and error prompts.

---

## Version `0.4.4`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b3`
- Songs: `v0.4.s18`
- Tatib: `v0.4.t11`
- Project: `v0.4.p6`

### Changes

- `[p4]` [Hotfix] Fixed projection title persists upon switching from Tatib and Bible with a title.
- `[b3]` Fixed StatusButton not working due to the change on the structure of StatusSubject.
- `[t11]` A description/note can now be added to TatibItem of type EndOfSection.
- `[p5]` Changed projection text color to white.
- `[p6]` Increased projection container's padding to 64px.

---

## Version `0.4.3`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b2`
- Songs: `v0.4.s18`
- Tatib: `v0.4.t10`
- Project: `v0.4.p3`

### Changes

- `[p1]` Text in projection display will now resize automatically to fit the screen.
- `[p2]` Title texts (in Tatib and Title Passage in Bible) will now be displayed on top of the display screen.
- `[p3]` Bible app will now work with project display.
- `[s9]` Added a button to open currently active Bookmark from Display tab.
- `[s10]` Added a button to open currently active Song from Display tab.
- `[s11]` SongShortcutButton will now be hidden when no active Song available.
- `[b2, s12, t9]` Added DateUtil module.
- `[s13]` Replaced the check when updating bookmarked verses to currently assigned Bookmark instead of the one in BookmarkManager.
- `[s14]` Added a parameter of type Function to be executed when bookmarked verses is updated when opening SongDetail modal.
- `[s15]` Added a popup on AddToBookmark and Bookmarked buttons in SongDetail modal that hint the name and date of currently assigned Bookmark.
- `[s16]` Added a button to display only selected verses in SongDetail modal.
- `[s17, t10]` Removed hover effect on (SongDetailModal's Verse list, Bookmark list, and Tatib list) in Dock.
- `[s18]` Limit the line clamp size when hovering search result in SongSearch tab.

---

## Version `0.4.2`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b1`
- Songs: `v0.4.s8`
- Tatib: `v0.4.t8`
- Project: `v0.4.p0`

### Changes

- `[b1, s5, t5]` Added an option to skip the toggle action when toggling a ToggleButton.
- `[s6, t6]` The status broadcast message that is forwarded to the Subject will now forward the whole object instead of the status value only.
- `[s7, t7]` The display tab will not re-broadcast the status message upon receiving a status broadcast message anymore.
- `[s8, t8]` Added an option to not notify the Subject when sending status broadcast message.
- `[p0]` Added a new app: `project` to show a full screen display of lyrics and tatib (and passage possibly in the future) texts.

---

## Version `0.4.1 Hotfix`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b0`
- Songs: `v0.4.s4`
- Tatib: `v0.4.t4`

### Hotfix Changes

- `[s4]` The displayed lyrics will be set to empty string upon reaching last lyric.

---

## Version `0.4`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b0`
- Songs: `v0.4.s3`
- Tatib: `v0.4.t4`

### Changes

- `[s1]` Added two display modes (Box and Outline DisplayModes) to use in Options.
- `[dj1, t1]` Added buttons to insert TatibItems right after a specific item.
- `[t2]` The page will now scroll to the last (detected) position before refreshing the TatibItem list.
- `[s2, t3]` The PreviewSegment in web will now be closed when trying to do other actions.
- `[s3, t4]` Added a PreviewSegment into the EditModals in Web that shows live preview of the currently edited items.

---

## Version `0.3.9`

### App Versions

- Django: `v0.3.dj3`
- Bible: `v0.3.b18`
- Songs: `v0.3.s42`
- Tatib: `v0.3.t19`

### Changes

- `[t16]` Title/Header-like can now be added to TataIbadahItem to provide additional text/info to the screen.
- `[s40, t17]` Fixed the scaling of Web Preview font-size.
- `[s41, t18]` Added a Button(s) to navigate back to the root URL of the web.
- `[s42, t19]` The top layout of some pages in the web is now in fixed position to improve the QoL when navigating around and/or editing Songs/TataIbadahItems.

---

## Version `0.3.8`

### App Versions

- Django: `v0.3.dj3`
- Bible: `v0.3.b18`
- Songs: `v0.3.s39`
- Tatib: `v0.3.t15`

### Changes

- `[s37]` NKB (Nyanyikanlah Kidung Baru) hymn book is now available.
- `[s38, t15]` Song's Verse and TataIbadahItem can now be previewed in the web by clicking the preview button (black eye icon).
- `[s39]` Deleted Bookmarks can now be viewed and restored to be used again.
- `[dj3]` Added and updated some Django Model Admins.

---

## Version `0.3.7`

### App Versions

- Django: `v0.3.dj2`
- Bible: `v0.3.b18`
- Songs: `v0.3.s36`
- Tatib: `v0.3.t14`

### Changes

- `[b12, s26, t1]` Added an indicator to indicate whether the Dock windows are being focused or not.
- `[b13, t2]` Added keyboard navigation support to Bible and Tatib dock.
- `[s27]` Fixed wrapping issue on overflowing texts in songs' Source Segment.
- `[t3]` Added reorder functionality to Tatib web.
- `[s28]` Fixed not-working codes to check disabled buttons.
- `[b14, s29]` Changed indicator button's icon to cross.
- `[t4]` Changed tatib's tab icon to cross.
- `[b15, s30, t5]` Changed Dock's background colour.
- `[t6]` Changed tatib's colour theme to red.
- `[t7]` Fixed a bug where TatibItem not actually being posted to BroadcastChannel on changing active item index.
- `[t8]` Fixed tatib's web page title.
- `[t9]` Removed tatib's Source Segment's label.
- `[t10]` Removed unused codes.
- `[t11]` Fixed an error accessing Tatib's name when there is no active tab.
- `[b16, s31, t12]` Fixed a bug where the Dock keep updating StatusButton's indefinitely when opening multiple dock windows.
- `[s32]` Replaced ReplaySubject with BehaviorSubject.
- `[s33]` Added more infos in string representation of Bookmark model class.
- `[b17, s34, t13]` Fixed a bug where the Dock's display status not being updated when specifically refreshing the source.
- `[s35, t14]` Changed Paste Modal's positive button's text to "Display".
- `[b18, s36]` Reduced margins and paddings by a little.

---

## Version `0.3.6`

### App Versions

- Django: `v0.3.dj2`
- Songs: `v0.3.s25`
- Bible: `v0.3.b11`
- Tatib: `v0.3.t0`

### Changes

- `[s24, b10]` Reduced Source Segment's height by the following methods:
  - Reducing segment's padding.
  - Reducing divider's margin.
  - Changing label's size to big.
- `[s25, b11]` Added an option to change the colour of Source's Label Icon.
- `[t0]` Added a new app: Tatib

---

## Version `0.3.5`

### App Versions

- Django: `v0.3.dj2`
- Songs: `v0.3.s23`
- Bible: `v0.3.b9`

### Changes

- `[s12]` Increased Song's Title length limit to 64 characters.
- `[s13]` Added keyboard support to navigate through the song.
- `[s14, b5]` Added a QoL support to block texts in DisplayTab from being selected by cursor clicks.
- `[b6]` Added a title in HistoryTab.
- `[s15]` Allowed some common symbols to be used in SongBook's and Song's title.
- `[s16, b7]` Added exit transitions when deactivating source.
- `[s17]` Added Song info (BookNumber and Title) on PrevSongButton and NextSongButton popups.
- `[dj2, s18]` Added reorder functionality to BookmarkDetailModal
- `[s19]` Fixed an error when updating popup on PrevSongButton and NextSongButton on empty Bookmark (and no active Bookmark).
- `[s20, b8]` Added an option to change Text Colour of the source.
- `[s21]` Changed Text Size options value to be numerical (in pixels).
- `[s22, b9]` Fixed an issue in which the source displaying brief exit transition when reloading both the dock and source.
- `[s23]` Allowed the same song to be added multiple of times to the same Bookmark.

---

## Version 0.3.4

### Songs (v0.3.s11)

- [s11] Remove "disabled days of week" in Bookmark form.
