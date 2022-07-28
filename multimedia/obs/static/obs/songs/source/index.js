import * as bc from '../common/bc.js'

const songInfo = $('#song-info')
const songBookInfo = $('#song-book-info')

const songBookNumber = $('#song-book-number')
const songVerseNumber = $('#song-verse-number')
const songTitle = $('#song-title')
const songLyric = $('.songLyric')

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

const doTransition = () => {
    songLyric.transition({
        animation: 'fade in',
        queue: false,
    })
}

bc.songInfoSubject.subscribe(updateSongInfo)
bc.songInfoSubject.subscribe(doTransition)
