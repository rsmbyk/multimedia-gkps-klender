const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const BC_NAME_SONG_INFO = 'OBS-SONGS-SONG-INFO'
const BC_NAME_STATUS = 'OBS-SONGS-STATUS'
const BC_NAME_CONTROL = 'OBS-SONGS-CONTROL'

export const songInfoSubject = new BehaviorSubject()
export const statusSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const controlSubject = new BehaviorSubject()

const bcSongInfo = new BroadcastChannel(BC_NAME_SONG_INFO)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)
const bcControl = new BroadcastChannel(BC_NAME_CONTROL)

export const postSongInfoMessage = (bookNumber, verseNumber, title, is_untitled, lyric) => {
    bcSongInfo.postMessage({
        bookNumber: bookNumber,
        verseNumber: verseNumber,
        title: title,
        is_untitled: is_untitled,
        lyric: lyric,
    })
}

export const postStatusMessage = (status, skipUpdateSubject) => {
    bcStatus.postMessage({
        status: status,
    })

    if (!skipUpdateSubject) {
        statusSubject.next(status)
    }
}

export function postControlMessage(control) {
    bcControl.postMessage({
        control: control,
    })
}

bcSongInfo.onmessage = ({ data: songInfo }) => songInfoSubject.next(songInfo)
bcStatus.onmessage = ({ data: status }) => statusSubject.next(status)
bcControl.onmessage = ({ data: control }) => controlSubject.next(control)

songInfoSubject.subscribe(console.log)
statusSubject.subscribe(console.log)
controlSubject.subscribe(console.log)
