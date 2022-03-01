import { BehaviorSubject } from '/static/helpers/rx.js';
import { ToggleButton } from '/static/helpers/buttons.js'
import * as doms from '/static/helpers/doms.js'

import * as bc from '../../common/bc.js'
import * as bookmarkManager from '../../common/bookmark-manager.js'

const songBookNumber = $('#display-song-book-number')
const songTitle = $('#display-song-title')
const songVerseList = $('#display-song-verses')
const songLyricList  = $('#display-song-lyric-list')

const btnStatusActive = $('#display-button-status-active')
const btnStatusInactive = $('#display-button-status-inactive')

const btnPrevSong = $('#display-btn-prev-song')
const btnNextSong = $('#display-btn-next-song')
const btnPrevVerse = $('#display-btn-prev-verse')
const btnNextVerse = $('#display-btn-next-verse')
const btnPrevLyric = $('#display-btn-prev-lyric')
const btnNextLyric = $('#display-btn-next-lyric')

const placeholderSongInfo = $('#display-placeholder-song-info')
const placeholderSongVerses = $('#display-placeholder-song-verses')
const placeholderSongLyricList = $('#display-placeholder-song-lyric-list')
const containerSongLyricList = $('#display-container-song-lyric-list')

let activeSong
let activeVerses
let activeLyrics
let activeSongIndex
let activeVerseIndex
let activeLyricIndex

const activeSongSubject = new BehaviorSubject()
const activeVersesSubject = new BehaviorSubject()
const activeLyricsSubject = new BehaviorSubject()
const activeSongIndexSubject = new BehaviorSubject()
const activeVerseIndexSubject = new BehaviorSubject()
const activeLyricIndexSubject = new BehaviorSubject()

let numberOfLine = 2

const displayPlaceholders = () => {
    songBookNumber.hide()
    songTitle.hide()
    songVerseList.hide()
    containerSongLyricList.hide()

    placeholderSongInfo.show()
    placeholderSongVerses.show()
    placeholderSongLyricList.show()
}

const hidePlaceholders = () => {
    placeholderSongInfo.hide()
    placeholderSongVerses.hide()
    placeholderSongLyricList.hide()

    songBookNumber.show()
    songTitle.show()
    songVerseList.show()
    containerSongLyricList.show()
}

const resetIndices = () => {
    activeSongIndexSubject.next(null)
    activeVerseIndexSubject.next(null)
    activeLyricIndexSubject.next(null)
}

const setIdle = () => {
    toggleButtonStatus.setInactive()
    resetIndices()
    displayPlaceholders()
}

const init = () => {
    toggleButtonStatus.setInactive()
    activeSongIndexSubject.next(0)
    hidePlaceholders()
}

const onBookmarkItemsUpdated = bookmarkItems => {
    if (bookmarkItems === null || bookmarkItems.length === 0) setIdle()
    else init()
}

const updateSongBookNumber = value => {
    songBookNumber.text(value !== null ? value : '-')
    songBookNumber.css('visibility', value === null ? 'hidden' : 'visible')
}

const updateSongTitle = value => songTitle.text(value)

const updateSongVerseList = activeVerses => {
    const createVerseText = ({ number: verseNumber }, index) => {
        const item = doms.createDOMFromJSON({
            tag: 'span',
            classList: ['ui', 'inverted', 'text'],
            innerText: verseNumber,
        })

        item
            .css('cursor', 'pointer')
            .css('padding-left', '0.28em')
            .css('padding-right', '0.28em')
            .click(() => activeVerseIndexSubject.next(index))

        return item
    }

    songVerseList.empty()
    songVerseList.append(...activeVerses.map(createVerseText))
}

const updateSong = activeSongIndex => {
    if (activeSongIndex === null)
        return

    activeSongSubject.next(bookmarkManager.bookmarkItems[activeSongIndex])
}

const updateVerses = activeSong => {
    activeVersesSubject.next(activeSong.verse_info)
    activeVerseIndexSubject.next(0)
}

const updateSongInfo = activeSong => {
    updateSongBookNumber(activeSong.song_info.book_number)
    updateSongTitle(activeSong.song_info.title + (activeSong.song_info.is_untitled ? ' *' : ''))
}

const updateActiveVerseMarker = activeVerseIndex => {
    if (activeVerseIndex === null)
        return

    songVerseList.children().addClass('disabled')
    songVerseList.children().eq(activeVerseIndex).removeClass('disabled')
}

const buildLyrics = activeVerseIndex => {
    if (activeVerseIndex === null)
        return

    const joinAdjacentText = lyricTexts => {
        const result = []
        let joinedTexts = ''

        for (let i=0; i < lyricTexts.length; i++) {
            if (joinedTexts.length !== 0) joinedTexts += '\n'
            joinedTexts += lyricTexts[i]

            if ((i+1) % numberOfLine === 0) {
                result.push(joinedTexts)
                joinedTexts = ''
            }
        }

        if (joinedTexts.length > 0) result.push(joinedTexts)
        return result
    }

    const lyric = activeVerses[activeVerseIndex].lyric
    activeLyricsSubject.next(joinAdjacentText(lyric.split('\n')))
}

const updateLyricList = activeLyrics => {
    const createLyricTextItem = (lyricText, index) => {
        const item = doms.createDOMFromJSON({
            tag: 'div',
            classList: ['item'],
            children: [
                {
                    tag: 'i',
                    classList: ['inverted', 'middle', 'aligned', 'small', 'map', 'marker', 'icon'],
                    innerText: '',
                },
                {
                    tag: 'div',
                    classList: ['middle', 'aligned', 'content'],
                    innerText: lyricText,
                },
            ],
        })

        const icoMarker = item.find('i.icon')
        if (index !== activeLyricIndex) icoMarker.hide()

        item.click(() => activeLyricIndexSubject.next(index))

        return item
    }

    songLyricList.empty()
    songLyricList.append(...activeLyrics.map(createLyricTextItem))
    containerSongLyricList.animate({ scrollTop: 0 }, 200)

    activeLyricIndexSubject.next(0)
}

const updateActiveLyricMarker = activeLyricIndex => {
    if (activeLyricIndex === null)
        return

    songLyricList.find('.item i.icon').hide()
    songLyricList.children().eq(activeLyricIndex).find('i.icon').show()
}

const nextSong = () => {
    const nextSongIndex =
        Math.min(activeSongIndex + 1, bookmarkManager.bookmarkItems.length - 1)

    if (nextSongIndex !== activeSongIndex)
        activeSongIndexSubject.next(nextSongIndex)
}

const prevSong = () => {
    const prevSongIndex =
        Math.max(activeSongIndex - 1, 0)

    if (prevSongIndex !== activeSongIndex)
        activeSongIndexSubject.next(prevSongIndex)
}

const nextVerse = () => {
    const nextVerseIndex =
        Math.min(activeVerseIndex + 1, activeVerses.length - 1)

    if (nextVerseIndex !== activeVerseIndex)
        activeVerseIndexSubject.next(nextVerseIndex)
}

const prevVerse = () => {
    const prevVerseIndex =
        Math.max(activeVerseIndex - 1, 0)

    if (prevVerseIndex !== activeVerseIndex)
        activeVerseIndexSubject.next(prevVerseIndex)
}

const nextLyric = () => {
    const nextLyricIndex =
        Math.min(activeLyricIndex + 1, activeLyrics.length - 1)

    if (nextLyricIndex !== activeLyricIndex)
        activeLyricIndexSubject.next(nextLyricIndex)
}

const prevLyric = () => {
    const prevLyricIndex =
        Math.max(activeLyricIndex - 1, 0)

    if (prevLyricIndex !== activeLyricIndex)
        activeLyricIndexSubject.next(prevLyricIndex)
}

const evaluateButton = (button, isValid) => {
    if (isValid) button.removeClass('disabled')
    else button.addClass('disabled')
}

const postStatusMessage = status => {
    bc.postStatusMessage(status)
}

const postSongInfo = activeLyricIndex => {
    if (activeLyricIndex === null)
        return

    bc.postSongInfoMessage(
        activeSong.song_info.book_number,
        activeVerses[activeVerseIndex].number,
        activeSong.song_info.title,
        activeSong.song_info.is_untitled,
        activeLyrics[activeLyricIndex],
    )
}

const updateStatusButton = status => {
    if (status === true) toggleButtonStatus.setActive()
    else toggleButtonStatus.setInactive()
}

const evaluateButtonStatusActive = bookmarkItems =>
    evaluateButton(btnStatusActive, bookmarkItems !== null && bookmarkItems.length !== 0)
const evaluateButtonStatusInactive = bookmarkItems =>
    evaluateButton(btnStatusInactive, bookmarkItems !== null && bookmarkItems.length !== 0)

const evaluateButtonNextSong = activeSongIndex =>
    evaluateButton(btnNextSong, activeSongIndex !== null && activeSongIndex !== bookmarkManager.bookmarkItems.length - 1)
const evaluateButtonPrevSong = activeSongIndex =>
    evaluateButton(btnPrevSong, activeSongIndex !== null && activeSongIndex !== 0)
const evaluateButtonNextVerse = activeVerseIndex =>
    evaluateButton(btnNextVerse, activeVerseIndex !== null && activeVerseIndex !== activeVerses.length - 1)
const evaluateButtonPrevVerse = activeVerseIndex =>
    evaluateButton(btnPrevVerse, activeVerseIndex !== null && activeVerseIndex !== 0)
const evaluateButtonNextLyric = activeLyricIndex =>
    evaluateButton(btnNextLyric, activeLyricIndex !== null && activeLyricIndex !== activeLyrics.length - 1)
const evaluateButtonPrevLyric = activeLyricIndex =>
    evaluateButton(btnPrevLyric, activeLyricIndex !== null && activeLyricIndex !== 0)

const toggleButtonStatus = new ToggleButton(
    btnStatusActive,
    btnStatusInactive,
    () => {
        postStatusMessage(true)
        postSongInfo(activeLyricIndex)
    },
    () => {
        postStatusMessage(false)
    },
)

btnNextSong.click(nextSong)
btnPrevSong.click(prevSong)
btnNextVerse.click(nextVerse)
btnPrevVerse.click(prevVerse)
btnNextLyric.click(nextLyric)
btnPrevLyric.click(prevLyric)

bookmarkManager.bookmarkItemsSubject.subscribe(onBookmarkItemsUpdated)
bookmarkManager.bookmarkItemsSubject.subscribe(evaluateButtonStatusActive)
bookmarkManager.bookmarkItemsSubject.subscribe(evaluateButtonStatusInactive)

bc.statusSubject.subscribe(updateStatusButton)

activeSongIndexSubject.subscribe(v => activeSongIndex = v)
activeSongIndexSubject.subscribe(updateSong)
activeSongIndexSubject.subscribe(evaluateButtonNextSong)
activeSongIndexSubject.subscribe(evaluateButtonPrevSong)

activeSongSubject.subscribe(v => activeSong = v)
activeSongSubject.subscribe(updateSongInfo)
activeSongSubject.subscribe(updateVerses)

activeVersesSubject.subscribe(v => activeVerses = v)
activeVersesSubject.subscribe(updateSongVerseList)

activeVerseIndexSubject.subscribe(v => activeVerseIndex = v)
activeVerseIndexSubject.subscribe(updateActiveVerseMarker)
activeVerseIndexSubject.subscribe(buildLyrics)
activeVerseIndexSubject.subscribe(evaluateButtonNextVerse)
activeVerseIndexSubject.subscribe(evaluateButtonPrevVerse)

activeLyricsSubject.subscribe(v => activeLyrics = v)
activeLyricsSubject.subscribe(updateLyricList)

activeLyricIndexSubject.subscribe(v => activeLyricIndex = v)
activeLyricIndexSubject.subscribe(updateActiveLyricMarker)
activeLyricIndexSubject.subscribe(evaluateButtonNextLyric)
activeLyricIndexSubject.subscribe(evaluateButtonPrevLyric)
activeLyricIndexSubject.subscribe(postSongInfo)

$('#tab-display .ui.has-popup').popup()
