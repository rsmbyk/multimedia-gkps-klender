const BC_NAME_SONG_INFO = 'OBS-SONGS-SONG-INFO'
const BC_NAME_STATUS = 'OBS-SONGS-STATUS'

let onSongInfoMessage
let onStatusMessage

const bcSongInfo = new BroadcastChannel(BC_NAME_SONG_INFO)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)

export const setOnSongInfoMessage = callback => {
    onSongInfoMessage = callback
}

export const setOnStatusMessage = callback => {
    onStatusMessage = callback
}

export const postSongInfoMessage = (bookNumber, verseNumber, title, lyric) => {
    bcSongInfo.postMessage({
        bookNumber: bookNumber,
        verseNumber: verseNumber,
        title: title,
        lyric: lyric,
    })
}

export const postStatusMessage = status => {
    bcStatus.postMessage({
        status: status,
    })
}

bcSongInfo.onmessage = ({data: {bookNumber, verseNumber, title, lyric}}) => {
    if (onSongInfoMessage !== null)
        onSongInfoMessage(bookNumber, verseNumber, title, lyric)
}

bcStatus.onmessage = ({data: {status}}) => {
    if (onStatusMessage !== null)
        onStatusMessage(status)
}
