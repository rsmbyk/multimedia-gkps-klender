import { BehaviorSubject } from 'rxjs'

export const LS_KEY_SONG_NUMBER_OF_LINES = 'OBS-SONGS-SONG-NUMBER-OF-LINES'
export const LS_KEY_SONG_TITLE_TEXT_SIZE = 'OBS-SONGS-SONG-TITLE-TEXT-SIZE'
export const LS_KEY_SONG_LYRIC_TEXT_SIZE = 'OBS-SONGS-SONG-LYRIC-TEXT-SIZE'

export const sizes = ['tiny', 'small', 'medium', 'large', 'huge']

const defaultNumberOfLines = 1
const defaultTitleTextSize = 'medium'
const defaultLyricTextSize = 'medium'

export let numberOfLines
export let titleTextSize
export let lyricTextSize

const numberOfLinesSubject = new BehaviorSubject()
const titleTextSizeSubject = new BehaviorSubject()
const lyricTextSizeSubject = new BehaviorSubject()

numberOfLinesSubject.subscribe(v => numberOfLines = v)
titleTextSizeSubject.subscribe(v => titleTextSize = v)
lyricTextSizeSubject.subscribe(v => lyricTextSize = v)

export let onNumberOfLinesChanged
export let onLyricTextSizeChanged
export let onTitleTextSizeChanged

window.addEventListener('storage', ({key, newValue}) => {
    if (key === LS_KEY_SONG_NUMBER_OF_LINES) {
        numberOfLinesSubject.next(newValue)
        if (onNumberOfLinesChanged !== null)
            onNumberOfLinesChanged(newValue)
    }
    else if (key === LS_KEY_SONG_TITLE_TEXT_SIZE && onTitleTextSizeChanged !== null)
        onTitleTextSizeChanged(newValue)
    else if (key === LS_KEY_SONG_LYRIC_TEXT_SIZE && onLyricTextSizeChanged !== null)
        onLyricTextSizeChanged(newValue)
})

export const setNumberOfLines = (value) => {
    localStorage.setItem(LS_KEY_SONG_NUMBER_OF_LINES, value)
    numberOfLinesSubject.next(getNumberOfLines())
}

const getNumberOfLines = () => {
    let value = localStorage.getItem(LS_KEY_SONG_NUMBER_OF_LINES)
    if (value === null) value = defaultNumberOfLines
    return value
}

$(window).on('load', () => {
    numberOfLinesSubject.next(getNumberOfLines())
})
