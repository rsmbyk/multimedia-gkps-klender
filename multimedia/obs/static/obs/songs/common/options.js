const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

export const LS_KEY_SONG_NUMBER_OF_LINES = 'OBS-SONGS-SONG-NUMBER-OF-LINES'
export const LS_KEY_SONG_TITLE_TEXT_SIZE = 'OBS-SONGS-SONG-TITLE-TEXT-SIZE'
export const LS_KEY_SONG_LYRIC_TEXT_SIZE = 'OBS-SONGS-SONG-LYRIC-TEXT-SIZE'

export const sizes = ['tiny', 'small', 'medium', 'large', 'huge']

const defaultNumberOfLines = 2
const defaultTitleTextSize = 'medium'
const defaultLyricTextSize = 'medium'

export let numberOfLines
export let titleTextSize
export let lyricTextSize

const getNumberOfLines = () => {
    let value = localStorage.getItem(LS_KEY_SONG_NUMBER_OF_LINES)
    if (value === null) value = defaultNumberOfLines
    return value
}

export const setNumberOfLines = (value) => {
    localStorage.setItem(LS_KEY_SONG_NUMBER_OF_LINES, value)
    numberOfLinesSubject.next(value)
}

export const numberOfLinesSubject = new BehaviorSubject(getNumberOfLines())
    .pipe(distinctUntilChanged())
export const titleTextSizeSubject = new BehaviorSubject()
export const lyricTextSizeSubject = new BehaviorSubject()

numberOfLinesSubject.subscribe(v => numberOfLines = v)
titleTextSizeSubject.subscribe(v => titleTextSize = v)
lyricTextSizeSubject.subscribe(v => lyricTextSize = v)

window.addEventListener('storage', ({key, newValue}) => {
    if (key === LS_KEY_SONG_NUMBER_OF_LINES)
        numberOfLinesSubject.next(newValue)
})
