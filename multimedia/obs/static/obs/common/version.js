/**
 * Single product SemVer for the whole app (OBS docks/sources, web, API).
 * Bump only on release/* or hotfix/* per docs/VERSIONING.md.
 */
export const APP_VERSION = '0.5.2'

/** Display string for footers (same as APP_VERSION under the current scheme). */
export function formatAppVersion() {
  return APP_VERSION
}

/**
 * Fill every `[data-app-version]` node under `root` with the product version.
 * @param {ParentNode} [root=document]
 */
export function applyAppVersion(root = document) {
  const label = formatAppVersion()
  root.querySelectorAll('[data-app-version]').forEach((node) => {
    node.textContent = label
  })
}
