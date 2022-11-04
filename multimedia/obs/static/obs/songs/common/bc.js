const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const BC_NAME_SONG_INFO = 'OBS-SONGS-SONG-INFO'
const BC_NAME_STATUS = 'OBS-SONGS-STATUS'

export const songInfoSubject = new BehaviorSubject()
export const statusSubject = new BehaviorSubject().pipe(distinctUntilChanged())

const bcSongInfo = new BroadcastChannel(BC_NAME_SONG_INFO)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)

export const postSongInfoMessage = (bookNumber, verseNumber, title, is_untitled, lyric) => {
    bcSongInfo.postMessage({
        bookNumber: bookNumber,
        verseNumber: verseNumber,
        title: title,
        is_untitled: is_untitled,
        lyric: lyric,
    })
}

export const postStatusMessage = status => {
    bcStatus.postMessage({
        status: status,
    })

    statusSubject.next(status)
}

bcSongInfo.onmessage = ({ data: songInfo }) => songInfoSubject.next(songInfo)

bcStatus.onmessage = ({ data: status }) => statusSubject.next(status)

songInfoSubject.subscribe(console.log)
statusSubject.subscribe(console.log)
