import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'
import * as bcBible from '../../bible/common/bc.js'
import {
    formatPassageProjectContent,
    formatSongProjectContent,
    formatTatibProjectContent,
} from './format.js'

const title = $('#project-title')
const text = $('#project-text')

const updateSongInfo = (songInfo) => {
    const content = formatSongProjectContent(songInfo)
    title.text(content.title)
    text.text(content.text)
}

function updateTatibInfo(tatibItem) {
    const content = formatTatibProjectContent(tatibItem)
    title.text(content.title)
    text.text(content.text)
}

function updatePassageInfo(passage) {
    const content = formatPassageProjectContent(passage)
    title.text(content.title)
    text.text(content.text)
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
bcSongs.songInfoSubject.subscribe(resizeTitleFont)
bcSongs.songInfoSubject.subscribe(resizeTextFont)
bcSongs.songInfoSubject.subscribe(doTransition)

bcTatib.tatibItemSubject.subscribe(updateTatibInfo)
bcTatib.tatibItemSubject.subscribe(resizeTitleFont)
bcTatib.tatibItemSubject.subscribe(resizeTextFont)
bcTatib.tatibItemSubject.subscribe(doTransition)

bcBible.passageSubject.subscribe(updatePassageInfo)
bcBible.passageSubject.subscribe(resizeTitleFont)
bcBible.passageSubject.subscribe(resizeTextFont)
bcBible.passageSubject.subscribe(doTransition)
