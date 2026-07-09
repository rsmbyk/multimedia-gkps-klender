# Versioning

This project uses **two levels** of version numbers: a **release version** for the
whole repo and **per-app versions** for each OBS plugin (plus the Django backend).

See [`CHANGELOG.md`](../CHANGELOG.md) for the history of shipped versions.

## Release version

Format: `MAJOR.MINOR.PATCH` (e.g. `0.4.6`)

A release bundles whatever app and backend versions were current when that
release was cut. Each release section in `CHANGELOG.md` lists those versions
under **App Versions**.

## Per-app versions (OBS plugins)

The four OBS browser-source apps each have their own counter:

| App | Letter | Version example | Shown in UI |
|-----|--------|-----------------|-------------|
| Bible | `b` | `v0.4.b10` | Bible dock → Bible tab |
| Songs | `s` | `v0.4.s29` | Songs dock → Songbooks tab |
| Tatib | `t` | `v0.4.t20` | Tatib dock → Tatibs tab |
| Project | `p` | `v0.4.p12` | Project source page `<title>` |

Format: `v{major}.{letter}{number}`

- **major** — matches the current release line (e.g. `0.4` while release `0.4.x` is active)
- **letter** — identifies the app (`b`, `s`, `t`, `p`)
- **number** — increments when **that app** changes, independently of the others

Example: Songs can move from `s28` → `s29` while Bible stays at `b10` within the
same release `0.4.6`.

## Django / backend version

The web admin, REST API, and Django apps use a separate counter:

- Format: `v0.4.dj1` (letter `dj` = Django)
- Tracked in `CHANGELOG.md` under **App Versions**
- Not displayed in OBS dock UI

## Where versions are defined

Versions are **hardcoded in templates** (there is no central runtime config):

| App | File |
|-----|------|
| Songs | `multimedia/obs/templates/songs/dock/tabs/songbooks.html` |
| Bible | `multimedia/obs/templates/bible/dock/tabs/bible.html` |
| Tatib | `multimedia/obs/templates/tatib/dock/tabs/tatibs.html` |
| Project | `multimedia/obs/templates/project/source/index.html` |

When you change an app, bump its version in the matching template **and** record
the change in `CHANGELOG.md`.

## Changelog change tags

Each bullet in `CHANGELOG.md` is prefixed with the app(s) it affects:

```text
[b8, s29, t20, p11] Added a feature to switch control between apps...
[b10] The corresponding Chapter will also be opened in Browse tab...
[dj1, t1] Added buttons to insert TatibItems right after a specific item.
```

| Tag | Meaning |
|-----|---------|
| `[s29]` | Songs only |
| `[b10, s29]` | Bible and Songs |
| `[dj1]` | Django backend / web / API |
| `[p12]` | Project source only |

Use the appropriate letter(s) when adding changelog entries. Bump the version
number for every app tag you add (e.g. a `[s30]` entry implies Songs is now
`v0.4.s30`).

## Checklist when shipping a change

1. Identify which app(s) changed (`b`, `s`, `t`, `p`, `dj`).
2. Increment each affected app's version counter in its template (if OBS-facing).
3. Add a changelog entry under the current or new release section with the
   correct `[tag]` prefix.
4. Update **App Versions** in that release section if any counter moved.
