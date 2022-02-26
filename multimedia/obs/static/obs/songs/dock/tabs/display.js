const { BehaviorSubject } = rxjs

import { ToggleButton } from '/static/helpers/buttons.js'
import * as doms from '/static/helpers/doms.js'

import * as bc from '../../common/bc.js'

import * as bookmarkManager from '../../common/bookmark-manager.js'

const songBookNumber = $('#display-song-book-number')
const songTitle      = $('#display-song-title')
const songVerses     = $('#display-song-verses')
const songLyricList  = $('#display-song-lyric-list')

const btnStatusActive   = $('#display-button-status-active')
const btnStatusInactive = $('#display-button-status-inactive')

const btnPrevSong  = $('#display-btn-prev-song')
const btnNextSong  = $('#display-btn-next-song')
const btnPrevVerse = $('#display-btn-prev-verse')
const btnNextVerse = $('#display-btn-next-verse')
const btnPrevLyric = $('#display-btn-prev-lyric')
const btnNextLyric = $('#display-btn-next-lyric')

const placeholderSongInfo = $('#display-placeholder-song-info')
const placeholderSongVerses = $('#display-placeholder-song-verses')
const placeholderSongLyricList = $('#display-placeholder-song-lyric-list')

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

const toggleButtonStatus = new ToggleButton(
    btnStatusActive,
    btnStatusInactive,
    () => bc.postStatusMessage(true),
    () => bc.postStatusMessage(false),
)

const update = bookmarkItems => {
    if (bookmarkItems === null || bookmarkItems.length === 0) setIdle()
    else init()
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

const resetIndices = () => {
    activeSongIndexSubject.next(undefined)
    activeVerseIndexSubject.next(undefined)
    activeLyricIndexSubject.next(undefined)
}

const displayPlaceholders = () => {
    placeholderSongInfo.show()
    placeholderSongVerses.show()
    placeholderSongLyricList.show()

    songBookNumber.hide()
    songTitle.hide()
    songVerses.hide()
    songLyricList.hide()
}

const hidePlaceholders = () => {
    songBookNumber.show()
    songTitle.show()
    songVerses.show()
    songLyricList.show()

    placeholderSongInfo.hide()
    placeholderSongVerses.hide()
    placeholderSongLyricList.hide()
}

const setSongBookNumber = value => songBookNumber.text(value)
const setSongTitle = value => songTitle.text(value)

const setSongVerses = activeVerses => {
    if (activeVerses === undefined)
        return

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

    songVerses.empty()
    songVerses.append(...activeVerses.map(createVerseText))
}

const updateSong = activeSongIndex => {
    if (activeSongIndex === undefined)
        return

    activeSongSubject.next(bookmarkManager.bookmarkItems[activeSongIndex])
    activeVersesSubject.next(bookmarkManager.bookmarkItems[activeSongIndex].verse_info)
    activeVerseIndexSubject.next(0)
}

const updateSongInfo = activeSong => {
    if (activeSong === undefined)
        return

    setSongBookNumber(activeSong.song_info.book_number)
    setSongTitle(activeSong.song_info.title)
}

const updateActiveVerseMarker = activeVerseIndex => {
    if (activeVerseIndex === undefined)
        return

    songVerses.children().addClass('disabled')
    songVerses.children().eq(activeVerseIndex).removeClass('disabled')
}

const buildLyrics = activeVerseIndex => {
    if (activeVerseIndex === undefined)
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
    if (activeLyrics === undefined)
        return

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
    songLyricList.parent().animate({ scrollTop: 0 }, 200)

    activeLyricIndexSubject.next(0)
}

const updateActiveLyricMarker = activeLyricIndex => {
    if (activeLyricIndex === undefined)
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

const postSongInfo = activeLyricIndex => {
    if (activeLyricIndex === undefined)
        return

    bc.postSongInfoMessage(
        activeSong.song_info.book_number,
        activeVerses[activeVerseIndex].number,
        activeSong.song_info.title,
        activeLyrics[activeLyricIndex],
    )
}

const updateStatusButton = status => {
    if (status === true)
        toggleButtonStatus.setActive()
    else
        toggleButtonStatus.setInactive()
}

const evaluateButtonStatusActive = bookmarkItems =>
    evaluateButton(btnStatusActive, bookmarkItems !== null && bookmarkItems.length !== 0)
const evaluateButtonStatusInactive = bookmarkItems =>
    evaluateButton(btnStatusInactive, bookmarkItems !== null && bookmarkItems.length !== 0)

const evaluateButtonNextSong = activeSongIndex =>
    evaluateButton(btnNextSong, activeSongIndex !== undefined && activeSongIndex !== bookmarkManager.bookmarkItems.length - 1)
const evaluateButtonPrevSong = activeSongIndex =>
    evaluateButton(btnPrevSong, activeSongIndex !== undefined && activeSongIndex !== 0)
const evaluateButtonNextVerse = activeVerseIndex =>
    evaluateButton(btnNextVerse, activeVerseIndex !== undefined && activeVerseIndex !== activeVerses.length - 1)
const evaluateButtonPrevVerse = activeVerseIndex =>
    evaluateButton(btnPrevVerse, activeVerseIndex !== undefined && activeVerseIndex !== 0)
const evaluateButtonNextLyric = activeLyricIndex =>
    evaluateButton(btnNextLyric, activeLyricIndex !== undefined && activeLyricIndex !== activeLyrics.length - 1)
const evaluateButtonPrevLyric = activeLyricIndex =>
    evaluateButton(btnPrevLyric, activeLyricIndex !== undefined && activeLyricIndex !== 0)

btnNextSong.click(nextSong)
btnPrevSong.click(prevSong)
btnNextVerse.click(nextVerse)
btnPrevVerse.click(prevVerse)
btnNextLyric.click(nextLyric)
btnPrevLyric.click(prevLyric)

bookmarkManager.bookmarkItemsSubject.subscribe(update)
bookmarkManager.bookmarkItemsSubject.subscribe(evaluateButtonStatusActive)
bookmarkManager.bookmarkItemsSubject.subscribe(evaluateButtonStatusInactive)

bc.statusSubject.subscribe(updateStatusButton)

activeSongIndexSubject.subscribe(v => activeSongIndex = v)
activeSongIndexSubject.subscribe(updateSong)
activeSongIndexSubject.subscribe(evaluateButtonNextSong)
activeSongIndexSubject.subscribe(evaluateButtonPrevSong)

activeSongSubject.subscribe(v => activeSong = v)
activeSongSubject.subscribe(updateSongInfo)

activeVersesSubject.subscribe(v => activeVerses = v)
activeVersesSubject.subscribe(setSongVerses)

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
