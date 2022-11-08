import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'

const lyricText = $('#lyric-text')

const updateSongInfo = ({ lyric }) => {
    lyricText.text(lyric)
}

function updateTatibInfo(tatibItem) {
    lyricText.text(tatibItem.text)
}

const doTransition = () => {
    lyricText.transition({
        animation: 'fade in',
        queue: false,
    })
}

function resizeFont() {
    let fontSize = 100

    do {
        lyricText.css('fontSize', fontSize)
        fontSize -= 1
    } while (lyricText.height() >= 680)
}

bcSongs.songInfoSubject.subscribe(updateSongInfo)
bcSongs.songInfoSubject.subscribe(doTransition)
bcSongs.songInfoSubject.subscribe(resizeFont)

bcTatib.tatibItemSubject.subscribe(updateTatibInfo)
bcTatib.tatibItemSubject.subscribe(doTransition)
bcTatib.tatibItemSubject.subscribe(resizeFont)
