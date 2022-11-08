import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'

const title = $('#project-title')
const text = $('#project-text')

const updateSongInfo = ({ lyric }) => {
    text.text(lyric)
}

function updateTatibInfo(tatibItem) {
    title.text(tatibItem.title)
    text.text(tatibItem.text)
}

const doTransition = () => {
    text.transition({
        animation: 'fade in',
        queue: false,
    })
}

function resizeTitleFont() {
    let fontSize = 50

    do {
        title.css('fontSize', fontSize)
        fontSize -= 1
    } while (title.width() >= $(window).width() - 72)
}

function resizeTextFont() {
    let fontSize = 100

    do {
        text.css('fontSize', fontSize)
        fontSize -= 1
    } while (text.height() >= $(window).height() - title.height() - 72 && fontSize > 1)
}

bcSongs.songInfoSubject.subscribe(updateSongInfo)
bcSongs.songInfoSubject.subscribe(doTransition)
bcSongs.songInfoSubject.subscribe(resizeTitleFont)
bcSongs.songInfoSubject.subscribe(resizeTextFont)

bcTatib.tatibItemSubject.subscribe(updateTatibInfo)
bcTatib.tatibItemSubject.subscribe(doTransition)
bcTatib.tatibItemSubject.subscribe(resizeTitleFont)
bcTatib.tatibItemSubject.subscribe(resizeTextFont)
