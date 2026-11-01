---
id: ITEM-186
status: in-review
title: 'A fresh clone starts on a machine with no HOME, and the converter uses the computer''s own fonts'
type: feat
priority: P2
effort: M
created: 2026-11-01
updated: 2026-11-01
spec: specs/182-host-font-detection/spec.md
branch: feat/182-host-font-detection
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/483
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/482
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-186: A fresh clone starts on a machine with no HOME, and the converter uses the computer's own fonts

## Summary

On a fresh checkout of a second computer the stack does not start. `docker-compose.yml` mounts the
operator's font directory as `${GKPS_FONTS_DIR:-$HOME/.local/share/gkps-fonts}`, and `HOME` is not an
environment variable on Windows, so Compose substitutes nothing and asks Docker for
`/.local/share/gkps-fonts`, which is not a path on that machine. The `media` container refuses the
mount, and with it the whole `docker compose up`.

The same line is the only route for the two Office faces (`Britannic Bold`, `Berlin Sans FB Demi`)
into the converter, so every computer needs a folder copied by hand from a machine that runs Office —
a step nobody can guarantee across the operators' laptops.

The card asks for two things: a fallback that needs no home directory, and a stack that reads the
fonts the computer already has. A host-side launcher detects the platform and mounts that platform's
font directories read-only; the image's metric-compatible substitutes stay as the fallback for a
machine that has none of them.

## Notes

Measured on Docker Desktop 29.8.2, 2026-11-01:

- `env -u HOME docker compose config` resolves the media volume's source to
  `/.local/share/gkps-fonts`.
- A missing bind source is never an empty mount: short syntax creates the directory when it sits
  under a shared root; a foreign path (`/Library/Fonts`) answers `mounts denied: The path … is not
  shared from the host`; a Windows path on Linux answers `invalid volume specification`; long syntax
  with `create_host_path: false` answers `bind source path does not exist`. Each one stops the whole
  stack, not just the one service.
- The fontconfig aliases in `docker/slides-fonts.conf` all use `binding="same"`, which overrides a
  font that is installed. With `Liberation Sans` aliased to `Noto Serif`, `fc-match "Liberation
  Sans"` returned `Noto Serif`. With `binding="weak"` it returned `Liberation Sans`, and a missing
  family (`NoSuchFamilyXYZ`) still resolved to its substitute. Unless the binding changes, mounting
  the host's fonts would change nothing for any of the eight aliased families.
- Font directories by platform: Windows `C:/Windows/Fonts` and
  `%LOCALAPPDATA%\Microsoft\Windows\Fonts`; macOS `/System/Library/Fonts`, `/Library/Fonts`,
  `~/Library/Fonts`; Linux `/usr/share/fonts`, `~/.local/share/fonts`. `C:/Windows/Fonts` covers an
  Office install and carries no username.
- The derived PDF is keyed on the renderer's version and its font inventory
  (`multimedia/local_media.py`), so a host font that becomes visible correctly invalidates an older
  conversion.
- Nothing enters the image: the fonts are read where the machine already licenses them, which is why
  the image keeps shipping only the free substitutes.
- `.env` stays a documented step: with no `.env` at all, `docker compose config` fails earlier, on the
  required `GKPS_MEDIA_PRODUCTION_ORIGIN`. The `HOME` failure is what a computer hits after following
  the setup instructions.

## Acceptance sketch

- A checkout with `.env` filled as documented, and no `HOME` exported, starts every service of the
  stack; the media service's font mount resolves to a path inside the checkout.
- Running the launcher on Windows, macOS and Linux mounts that platform's font directories read-only;
  `docker compose up` on its own still works, without host fonts.
- A deck set in Calibri or Britannic Bold is drawn in the real face when the computer has it, and in
  the image's substitute when it does not.
- No font file is copied into the repository or the image by this change.

## Links

- Spec: —
- Related items: ITEM-179 (the render-fidelity slice that introduced the mounted directory)
- Produced by: ADR-less design discussion of 2026-11-01, recorded in the slice's `research.md`
