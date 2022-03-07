import * as bc from '../common/bc.js';

const songSegment = $('#song-segment')
const songInfo = $('#song-info')
const songBookInfo = $('#song-book-info')

const songBookNumber = $('#song-book-number')
const songVerseNumber = $('#song-verse-number')
const songTitle = $('#song-title')
const songLyric = $('#song-lyric')

const updateSongInfo = ({ bookNumber, verseNumber, title, is_untitled, lyric }) => {
    if (bookNumber === null) songBookInfo.hide()
    else songBookInfo.show()

    if (is_untitled) songInfo.hide()
    else songInfo.show()

    songBookNumber.text(bookNumber)
    songVerseNumber.text(verseNumber)
    songTitle.text(title)
    songLyric.text(lyric)
}

const updateDisplayState = status => {
    if (status === true) songSegment.removeClass('hidden')
    else songSegment.addClass('hidden')
}

bc.songInfoSubject.subscribe(updateSongInfo)
bc.statusSubject.subscribe(updateDisplayState)

bc.postStatusMessage(false)
