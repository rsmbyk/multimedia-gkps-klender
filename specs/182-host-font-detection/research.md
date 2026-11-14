# Research — the computer's own fonts reach the converter

Every decision below was measured on the working machine on 2026-11-01 (Docker Desktop 29.8.2,
fontconfig on Fedora 42, Compose v2). Provenance is a command, not a belief.

## D001 — The font mount's default lives inside the checkout, not under `$HOME`

**Decision.** `docker-compose.yml` mounts `${GKPS_FONTS_DIR:-./.fonts}` at
`/usr/share/fonts/operator`.

**Rationale.** A compose default cannot name a variable the computer may not have. `HOME` is absent on
Windows, where the shell exports `USERPROFILE` instead, so the current default collapses to
`/.local/share/gkps-fonts` and the media service refuses the mount. A relative source is resolved by
Compose against the project directory, needs no variable at all, and lands under the repository — which
is already shared with Docker on every platform because it is bind-mounted at `.:/app`.

**Alternatives.** Keep `$HOME` (fails on Windows). A named volume (nobody could put a font into it).
A required `.env` variable (moves the failure rather than removing it).

**Provenance.** `env -u HOME docker compose config` resolved the source to `/.local/share/gkps-fonts`;
with the new default and `HOME` unset it resolves to `<checkout>/.fonts` and creates nothing until a
run.

## D002 — The platform is detected by a host launcher, never by Compose

**Decision.** Two thin wrappers, `docker/up.sh` (POSIX sh, macOS and Linux) and `docker/up.ps1`
(Windows PowerShell 5.1+), detect the platform's font directories, write a small compose override into
the system temp directory, and run `docker compose -f docker-compose.yml -f <override> <command>`.

**Rationale.** Compose has no optional mount and cannot ask the host what it is. A missing or foreign
source is fatal in every shape, so "mount everything and let the absent ones be empty" does not exist:
short syntax creates the directory when it sits under a shared root, and otherwise the daemon refuses —
`mounts denied: The path /Library/Fonts is not shared from the host`, `invalid volume specification`
for `C:/Windows/Fonts` on Linux, `bind source path does not exist` for `create_host_path: false`. Each
one stops the whole stack, not just one service.

**Alternatives.** Mount every known directory unconditionally (fails three ways, measured). Per-OS
compose files chosen by hand (that is the launcher without the detection). A custom compose plugin (a
second runtime to maintain).

**Provenance.** All four failure shapes reproduced on the working machine; see the card's Notes.

## D003 — The launcher writes a generated override, rather than filling fixed slots

**Decision.** The launcher emits only the mounts it found, into
`${TMPDIR:-/tmp}/gkps-host-fonts.yaml` (Windows: `%TEMP%\gkps-host-fonts.yaml`), and passes it as the
second `-f`.

**Rationale.** The number of directories differs per platform (two on Windows, three on macOS, one or
two on Linux) and any of them may be absent. A generated file keeps the committed compose file honest:
plain `docker compose up` mounts the operator's directory and nothing else, while the launcher adds
what exists. Multiple `-f` files merge volume lists by appending, which was measured.

**Alternatives.** Three fixed slots defaulting to an empty directory inside the checkout (creates a
junk folder on every start). A required `.env` list (back to hand configuration, per computer).

**Provenance.** `docker compose -f compose.yaml -f compose.host.yaml config` showed the override's
volumes appended after the base's, and a source containing spaces resolved intact. An override whose
`volumes` list is empty — or which carries no `volumes` key at all — merges cleanly and leaves the
base mount untouched, so the launcher may always write its file, even when it found no directory.

## D004 — Host fonts are mounted under `/usr/share/fonts/host`

**Decision.** Every detected directory is mounted read-only at `/usr/share/fonts/host/<n>`.

**Rationale.** The image's fontconfig already scans `/usr/share/fonts` recursively, so nothing in the
configuration has to be told about a new directory. Measured inside the media image: a directory
mounted at `/usr/share/fonts/host` was scanned (`fc-list | grep -c /usr/share/fonts/host` = 1) and its
font answered `fc-match` ahead of the image's own copy of the same family.

**Alternatives.** A directory outside the font tree plus an explicit `<dir>` entry for every mount
(more moving parts, same result).

**Provenance.** `docker run --rm -v <dir>:/usr/share/fonts/host:ro multimedia-gkps-klender-media
sh -c 'fc-cache -f; fc-list | grep -c /usr/share/fonts/host; fc-match "Liberation Sans"'`.

## D005 — The operator's directory beats the computer's, by explicit directory order

**Decision.** `docker/slides-fonts.conf` names the two directories explicitly, operator first:
`<dir>/usr/share/fonts/operator</dir>` then `<dir>/usr/share/fonts/host</dir>`.

**Rationale.** Fontconfig resolves two files claiming one family by the order its directories are
listed. Measured with two copies of `Liberation Sans` in `.../operator` and `.../host`: listing
operator first made `fc-match` return the operator copy, and listing host first made it return the
host copy — the generic `/usr/share/fonts` scan did not decide it.

**Alternatives.** Let fontconfig pick (the owner chose the folder deliberately, so a random winner is
wrong). Copy the operator's files over the host's at container start (an entrypoint that mutates a
read-only mount).

**Provenance.** `FONTCONFIG_FILE=<conf> fc-match -f '%{file}' 'Liberation Sans'` over three
configurations: parent only, operator-first, host-first.

## D006 — Every alias uses `binding="weak"`, so an installed face wins

**Decision.** All eight aliases in `docker/slides-fonts.conf` change from `binding="same"` to
`binding="weak"`.

**Rationale.** `binding="same"` overrides the real family even when it is installed: aliasing
`Liberation Sans` to `Noto Serif` made `fc-match "Liberation Sans"` return `Noto Serif` although
Liberation Sans was present. `binding="weak"` returned Liberation Sans, and a family that is genuinely
absent still resolved to its substitute. Without this change the mounts of D004 would change nothing
for any mapped family — including the two Office faces the slice exists for.

**Alternatives.** Drop the aliases (the build fails on a monospaced answer, which is the reason they
exist). Ship the real fonts (licensing).

**Provenance.** `FONTCONFIG_FILE=<conf> fc-match` with a present family and a missing one, for
`same`, `weak` and `strong`.

## D007 — The directories each platform contributes

| Platform | Mounted when present |
| --- | --- |
| Windows | `C:/Windows/Fonts`; `%LOCALAPPDATA%\Microsoft\Windows\Fonts` |
| macOS | `/System/Library/Fonts`; `/Library/Fonts`; `~/Library/Fonts` |
| Linux | `/usr/share/fonts`; `~/.local/share/fonts` |
| All | `~/.local/share/gkps-fonts` — the old default, so an installed computer keeps its fonts |

**Rationale.** `C:/Windows/Fonts` is where Office installs its faces and carries no user name, so the
Windows path needs no detection beyond `Test-Path`. The per-user directory is where a Store-installed or
user-installed font lands. The old home-directory folder is kept because the documentation told
operators to use it.

**Alternatives.** Windows system directory only (misses per-user installs — a recorded assumption
covers this if it is rejected). Enumerate the font database instead of directories (needs a host-side
font parser).

**Provenance.** Platform conventions; the paths are the ones fontconfig and Windows document as their
font locations.

## D008 — The entrypoint refreshes the cache when either directory exists

**Decision.** `docker/entrypoint.sh` runs `fc-cache -f` when `/usr/share/fonts/operator` **or**
`/usr/share/fonts/host` exists.

**Rationale.** It already does this for the operator directory; the host mount is the same kind of
change to the same cache, and a stale cache would keep the new faces out until a manual refresh.

**Alternatives.** Rely on fontconfig's own freshness checks (works for a file added, not for a
directory mounted at start).

**Provenance.** `docker/entrypoint.sh:14` today; the cache is what the renderer identity reads.

## D009 — The version level is `minor`

**Decision.** `bump: minor` — `1.26.0`.

**Rationale.** A new capability appears (`local-stack`: the stack starts on a computer that does not
export `HOME`, and reads that computer's fonts). It is not a breaking change: plain `docker compose up`
still works, and the image's substitutes still apply where a face is absent.

**Provenance.** `docs/PROCESS.md` VER-10 (a new capability is `minor`).

## D010 — The launcher asks the daemon what it is, because an unshared bind is silently empty

**Decision.** `docker/up.sh` reads `docker info --format '{{.OperatingSystem}}'`; when it answers
`Docker Desktop` on macOS or Linux, the system-wide directories are skipped with a printed reason and a
pointer to File Sharing, and only home-directory sources are mounted. The Windows launcher mounts
`C:/Windows/Fonts` unconditionally, because the whole `C:` drive is shared by default. After a
successful `up`, both launchers look inside the container once and warn when none of the mounted
directories showed a font.

**Rationale.** Docker Desktop mounts a path it cannot read as an **empty directory**, without an error:
`docker run -v /usr/share/fonts:/probe:ro alpine ls /probe` returned nothing on this machine while
`docker inspect` still reported the bind. The stack would start, look healthy, and quietly draw with
the image's faces. A warning that the mount is empty is the only signal an operator can act on, and the
daemon's own answer is a reliable way to avoid creating the empty mount in the first place.

**Alternatives.** Probe each directory by running a throwaway container (an extra image and container
per start). Mount everything and trust the daemon (measured to fail silently). Skip system directories
on every platform (would lose `/usr/share/fonts` on a native Linux engine, where they work).

**Provenance.** `docker run --rm -v /usr/share/fonts:/probe:ro alpine:latest sh -c 'ls /probe | wc -l'`
→ `0`, with `docker inspect` showing the bind present; the same path mounted from `$HOME` lists its
files. `docker info --format '{{.OperatingSystem}}'` → `Docker Desktop` on this machine.

## Open unknowns

None. The four failure shapes, the directory-order precedence, the `weak` binding, the recursive scan
and the multi-file merge are all measured; the remaining platform-specific behaviour (a real Windows
machine, a real macOS machine) is covered by the manual verification in `plan.md`, not by a guess.
