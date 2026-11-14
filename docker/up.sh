#!/bin/sh
# Start the stack with this computer's own fonts mounted beside the operator's folder.
#
# Compose cannot detect a platform and has no optional mount: a source it cannot find stops the whole
# stack. So the directories are chosen here, written to a small override, and passed as a second -f.
# Plain `docker compose up` keeps working — it mounts the operator's folder and nothing else.
#
#   ./docker/up.sh              # up -d, with this computer's fonts
#   ./docker/up.sh --build      # up -d --build
#   ./docker/up.sh --print      # show the merged configuration, start nothing
set -eu

cd "$(dirname "$0")/.."

override="${TMPDIR:-/tmp}/gkps-host-fonts.yaml"
count=0
added_dirs=
labels=
skipped=

add_dir() {
    dir="$1"
    [ -n "$dir" ] || return 0
    [ -d "$dir" ] || return 0
    count=$((count + 1))
    quoted=$(printf '%s' "$dir" | sed "s/'/''/g")
    added_dirs="$added_dirs$quoted "
    if [ -n "$labels" ]; then labels="$labels,"; fi
    labels="$labels$count=$quoted"
    printf "\n      - type: bind\n        source: '%s'\n        target: /usr/share/fonts/host/%s\n        read_only: true" \
        "$quoted" "$count" >>"$override"
}

skip_dir() {
    dir="$1"
    [ -d "$dir" ] || return 0
    skipped="$skipped $dir"
}

# Docker Desktop shares only a few host roots, and a bind of a path it does not share mounts an EMPTY
# directory instead of failing: the stack would start and the image's own faces would quietly win.
# The launcher therefore asks the daemon what it is, and keeps the system-wide directories only for an
# engine that can actually read them.
docker_os=$(docker info --format '{{.OperatingSystem}}' 2>/dev/null || true)
case "$docker_os" in
*"Docker Desktop"*) shares_home_only=1 ;;
*) shares_home_only=0 ;;
esac

: >"$override"
printf 'services:\n  media:\n    volumes:' >>"$override"

case "$(uname -s)" in
Darwin)
    if [ "$shares_home_only" -eq 1 ]; then
        skip_dir /System/Library/Fonts
        skip_dir /Library/Fonts
    else
        add_dir /System/Library/Fonts
        add_dir /Library/Fonts
    fi
    add_dir "${HOME:-}/Library/Fonts"
    ;;
*)
    if [ "$shares_home_only" -eq 1 ]; then
        skip_dir /usr/share/fonts
    else
        add_dir /usr/share/fonts
    fi
    add_dir "${HOME:-}/.local/share/fonts"
    ;;
esac

# The folder the documentation named before this change, so an installed computer keeps its fonts.
add_dir "${HOME:-}/.local/share/gkps-fonts"

if [ "$count" -eq 0 ]; then
    printf ' []\n' >>"$override"
else
    printf '\n' >>"$override"
    printf "    environment:\n      GKPS_MEDIA_FONT_LABELS: '%s'\n" "$labels" >>"$override"
fi

print_only=0
if [ $# -gt 0 ] && [ "$1" = "--print" ]; then
    print_only=1
    shift
fi

if [ "$count" -eq 0 ]; then
    printf 'gkps: no font directory found on this computer\n' >&2
else
    printf 'gkps: font directories from this computer (%s):\n' "$count" >&2
    for dir in $added_dirs; do
        printf 'gkps:   %s\n' "$dir" >&2
    done
fi
for dir in $skipped; do
    printf 'gkps: skipped %s — the Docker daemon cannot read it from the host; add it under Docker Desktop > Settings > Resources > File Sharing\n' "$dir" >&2
done

if [ "$print_only" -eq 1 ]; then
    exec docker compose -f docker-compose.yml -f "$override" config "$@"
fi

if [ $# -eq 0 ]; then
    set -- up -d
fi
case "$1" in
--*) set -- up -d "$@" ;;
esac

docker compose -f docker-compose.yml -f "$override" "$@"
status=$?

# A shared path Docker cannot read mounts as an empty directory without an error, so the start is
# followed by one look inside: nothing visible means the operator is told instead of quietly drawing
# with the image's faces.
if [ "$status" -eq 0 ] && [ "$1" = "up" ] && [ "$count" -gt 0 ]; then
    seen=$(docker compose -f docker-compose.yml -f "$override" exec -T media sh -c \
        'fc-list 2>/dev/null | grep -c "/usr/share/fonts/host/"' 2>/dev/null || printf '0')
    if [ "${seen:-0}" -eq 0 ]; then
        printf 'gkps: the mounted font directories showed no font to the companion\n' >&2
        printf 'gkps: check Docker > Settings > Resources > File Sharing for the paths above\n' >&2
    fi
fi

exit "$status"
