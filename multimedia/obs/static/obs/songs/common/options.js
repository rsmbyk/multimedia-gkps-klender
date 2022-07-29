const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

export const LS_KEY_NUMBER_OF_LINES = 'OBS_SONGS_DOCK_SETTINGS_NUMBER_OF_LINES'
export const LS_KEY_DISPLAY_MODE = 'OBS_SONGS_DOCK_SETTINGS_DISPLAY_MODE'

export const DISPLAY_MODE_SEGMENT = 0
export const DISPLAY_MODE_BOX = 1
export const DISPLAY_MODE_OUTLINE = 2

const defaultDisplayMode = DISPLAY_MODE_SEGMENT
const defaultNumberOfLines = 2

export const getDisplayMode = () => {
    let value = localStorage.getItem(LS_KEY_DISPLAY_MODE)
    if (value === null) value = defaultDisplayMode
    // as this value needs to be processed raw in some switch
    // expressions, and not used directly in string template
    // (at the time of writing this comment), I decided
    // to parse the displayMode value retrieved from localStrorage
    // to integer.
    return parseInt(value)
}

export const getNumberOfLines = () => {
    let value = localStorage.getItem(LS_KEY_NUMBER_OF_LINES)
    if (value === null) value = defaultNumberOfLines
    return value
}

export const setDisplayMode = value => {
    localStorage.setItem(LS_KEY_DISPLAY_MODE, value)
    displayModeSubject.next(value)
}

export const setNumberOfLines = (value) => {
    localStorage.setItem(LS_KEY_NUMBER_OF_LINES, value)
    numberOfLinesSubject.next(value)
}

export const displayModeSubject = new BehaviorSubject(getDisplayMode()).pipe(distinctUntilChanged())
export const numberOfLinesSubject = new BehaviorSubject(getNumberOfLines()).pipe(distinctUntilChanged())

window.addEventListener('storage', ({ key, newValue }) => {
    if (key === LS_KEY_NUMBER_OF_LINES)
        numberOfLinesSubject.next(newValue)

    if (key === LS_KEY_DISPLAY_MODE)
        // value passed through storage event listener get cast
        // to string. We need to convert it back to integer here.
        displayModeSubject.next(parseInt(newValue))
})
