const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

export const LS_KEY_NUMBER_OF_LINES = 'OBS_SONGS_DOCK_SETTINGS_NUMBER_OF_LINES'

const defaultNumberOfLines = 2

export const getNumberOfLines = () => {
    let value = localStorage.getItem(LS_KEY_NUMBER_OF_LINES)
    if (value === null) value = defaultNumberOfLines
    return value
}

export const setNumberOfLines = (value) => {
    localStorage.setItem(LS_KEY_NUMBER_OF_LINES, value)
    numberOfLinesSubject.next(value)
}

export const numberOfLinesSubject = new BehaviorSubject(getNumberOfLines()).pipe(distinctUntilChanged())

window.addEventListener('storage', ({ key, newValue }) => {
    if (key === LS_KEY_NUMBER_OF_LINES)
        numberOfLinesSubject.next(newValue)
})
