"""Utilities for deciding which CI test lanes a change must run."""

from __future__ import annotations

import subprocess


def changed_paths(base: str | None, head: str | None) -> list[str] | None:
    """Return changed paths, or None when a revision cannot be compared."""
    if not base or not head or set(base) == {"0"}:
        return None
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base, head],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None
    return result.stdout.splitlines()


def docs_only(paths: list[str] | None) -> bool:
    if paths is None:
        return False
    excluded = ("docs/", "specs/", "backlog/")
    excluded_files = {"VERSION", "CHANGELOG.md"}
    return all(path.startswith(excluded) or path in excluded_files for path in paths)
