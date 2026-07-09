/**
 * Bind a keyboard shortcut using hotkeys-js.
 * Uses window.hotkeys explicitly so bindings work inside ES modules.
 */
export const bind = (keys, callback) => {
    window.hotkeys(keys, callback)
}
