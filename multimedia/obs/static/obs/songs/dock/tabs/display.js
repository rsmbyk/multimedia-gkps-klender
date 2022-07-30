import { BehaviorSubject } from '/static/helpers/rx.js';
import { ToggleButton } from '/static/helpers/buttons.js'
import * as doms from '/static/helpers/doms.js'

import * as focusManager from '../../../common/focusManager.js'

import * as bc from '../../common/bc.js'

import * as options from '../../common/options.js'
import * as bookmarkManager from '../common/bookmark-manager.js'

const hasPopup = $('#tab-display .hasPopup')

const dropdownSongs = $('#display-dropdown-songs')

const songBookNumber = $('#display-song-book-number')
const songTitle = $('#display-song-title')
const songVerseList = $('#display-song-verses')
const songLyricList  = $('#display-song-lyric-list')

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevSong = $('#display-btn-prev-song')
const buttonNextSong = $('#display-btn-next-song')
const buttonPrevVerse = $('#display-btn-prev-verse')
const buttonNextVerse = $('#display-btn-next-verse')
const buttonPrevLyric = $('#display-btn-prev-lyric')
const buttonNextLyric = $('#display-btn-next-lyric')
const buttonLastLyric = $('#display-btn-last-lyric')
const buttonLastVerse = $('#display-btn-last-verse')

const placeholderSongInfo = $('#display-placeholder-song-info')
const placeholderSongVerses = $('#display-placeholder-song-verses')
const placeholderSongLyricList = $('#display-placeholder-song-lyric-list')
const containerSongLyricList = $('#display-container-song-lyric-list')

let songTitlePopupTimer

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

const displayPlaceholders = () => {
    dropdownSongs.hide()
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

    dropdownSongs.show()
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

const createSongsDropdownMenuItem = (bookmarkItem, index) => {
    return {
        value: index,
        name: `${bookmarkItem.song_info.title} ${bookmarkItem.song_info.is_untitled ? '*' : ''}`,
        description: bookmarkItem.song_info.book_number,
        descriptionVertical: true,
    }
}

const updateSongsDropdown = bookmarkItems => {
    if (bookmarkItems === null || bookmarkItems.length === 0)
        return

    dropdownSongs
        .dropdown('change values', bookmarkItems.map(createSongsDropdownMenuItem))
        .dropdown('setting', 'onChange', value => {
            if (!isNaN(parseInt(value)) && parseInt(value) !== activeSongIndex) {
                activeSongIndexSubject.next(parseInt(value))
            }
        })
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
    if (activeVerseIndex === undefined || activeVerseIndex === null)
        return

    const joinAdjacentText = lyricTexts => {
        const result = []
        let joinedTexts = ''

        for (let i=0; i < lyricTexts.length; i++) {
            if (joinedTexts.length !== 0) joinedTexts += '\n'
            joinedTexts += lyricTexts[i]

            if ((i+1) % options.getNumberOfLines() === 0) {
                result.push(joinedTexts)
                joinedTexts = ''
            }
        }

        if (joinedTexts.length > 0) result.push(joinedTexts)
        result.push('--- END ---')
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
                    classList: ['inverted', 'middle', 'aligned', 'small', 'map', 'marker', 'alternate', 'icon'],
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
        activeLyricIndex !== activeLyrics.length - 1 ? activeLyrics[activeLyricIndex] : '',
    )
}

const updateStatusButton = status => {
    if (status === true) toggleButtonStatus.setActive()
    else toggleButtonStatus.setInactive()
}

const getSongButtonPopupContent = bookmarkItem => {
    const { song_info: { book_number, title, is_untitled } } = bookmarkItem
    const songTitle = title + (is_untitled ? ' *' : '')
    const songBookNumber = book_number !== null ? `${book_number}` : null
    return book_number !== null ? `${songBookNumber} (${songTitle})` : songTitle
}

const updateNextSongButtonPopup = activeSongIndex => {
    if (activeSongIndex !== null && activeSongIndex !== bookmarkManager.bookmarkItems.length - 1) {
        const nextSong = bookmarkManager.bookmarkItems[activeSongIndex + 1]
        buttonNextSong.attr('data-content', getSongButtonPopupContent(nextSong))
    }
}

const updatePrevSongButtonPopup = activeSongIndex => {
    if (activeSongIndex !== null && activeSongIndex !== 0) {
        const prevSong = bookmarkManager.bookmarkItems[activeSongIndex - 1]
        buttonPrevSong.attr('data-content', getSongButtonPopupContent(prevSong))
    }
}

const evaluateButtonStatusActive = bookmarkItems =>
    evaluateButton(buttonStatusActive, bookmarkItems !== null && bookmarkItems.length !== 0)
const evaluateButtonStatusInactive = bookmarkItems =>
    evaluateButton(buttonStatusInactive, bookmarkItems !== null && bookmarkItems.length !== 0)

const evaluateButtonNextSong = activeSongIndex =>
    evaluateButton(buttonNextSong, activeSongIndex !== null && activeSongIndex !== bookmarkManager.bookmarkItems.length - 1)
const evaluateButtonPrevSong = activeSongIndex =>
    evaluateButton(buttonPrevSong, activeSongIndex !== null && activeSongIndex !== 0)
const evaluateButtonNextVerse = activeVerseIndex =>
    evaluateButton(buttonNextVerse, activeVerseIndex !== null && activeVerseIndex !== activeVerses.length - 1)
const evaluateButtonPrevVerse = activeVerseIndex =>
    evaluateButton(buttonPrevVerse, activeVerseIndex !== null && activeVerseIndex !== 0)
const evaluateButtonNextLyric = activeLyricIndex =>
    evaluateButton(buttonNextLyric, activeLyricIndex !== null && activeLyricIndex !== activeLyrics.length - 1)
const evaluateButtonPrevLyric = activeLyricIndex =>
    evaluateButton(buttonPrevLyric, activeLyricIndex !== null && activeLyricIndex !== 0)

const onLastLyricReached = activeLyricIndex => {
    if (activeLyricIndex !== null && activeLyricIndex === activeLyrics.length - 1) {
        toggleButtonStatus.setInactive()
        if (activeVerseIndex !== activeVerses.length - 1) {
            buttonNextLyric.hide()
            buttonLastLyric.show()
        }
        else if (activeSongIndex !== bookmarkManager.bookmarkItems.length - 1) {
            buttonNextLyric.hide()
            buttonLastVerse.show()
        }
    }
    else {
        buttonLastLyric.hide()
        buttonLastVerse.hide()
        buttonNextLyric.show()
    }
}

const toggleButtonStatus = new ToggleButton(
    buttonStatusActive,
    buttonStatusInactive,
    () => {
        if (activeLyricIndex === activeLyrics.length - 1)
            return false

        postStatusMessage(true)
        postSongInfo(activeLyricIndex)
    },
    () => {
        postStatusMessage(false)
    },
)

buttonNextSong.click(nextSong)
buttonPrevSong.click(prevSong)
buttonNextVerse.click(nextVerse)
buttonPrevVerse.click(prevVerse)
buttonNextLyric.click(nextLyric)
buttonPrevLyric.click(prevLyric)

buttonLastLyric.click(() => {
    nextVerse()
    toggleButtonStatus.setActive()
})

buttonLastVerse.click(() => {
    nextSong()
    toggleButtonStatus.setActive()
})

songTitle.click(() => {
    navigator.clipboard.writeText(activeSong.title)
        .then(() => {
            songTitle
                .popup({
                    on: 'manual',
                    inverted: true,
                })
                .popup('show')

            clearTimeout(songTitlePopupTimer)
            songTitlePopupTimer = setTimeout(() => songTitle.popup('hide'), 800)
        })
})


focusManager.registerFocusChange('green')

bookmarkManager.bookmarkItemsSubject.subscribe(onBookmarkItemsUpdated)
bookmarkManager.bookmarkItemsSubject.subscribe(updateSongsDropdown)
bookmarkManager.bookmarkItemsSubject.subscribe(evaluateButtonStatusActive)
bookmarkManager.bookmarkItemsSubject.subscribe(evaluateButtonStatusInactive)

bc.statusSubject.subscribe(updateStatusButton)

options.numberOfLinesSubject.subscribe(() => buildLyrics(activeVerseIndex))

activeSongIndexSubject.subscribe(v => activeSongIndex = v)
activeSongIndexSubject.subscribe(updateSong)
activeSongIndexSubject.subscribe(evaluateButtonNextSong)
activeSongIndexSubject.subscribe(evaluateButtonPrevSong)
activeSongIndexSubject.subscribe(updateNextSongButtonPopup)
activeSongIndexSubject.subscribe(updatePrevSongButtonPopup)

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
activeLyricIndexSubject.subscribe(onLastLyricReached)
activeLyricIndexSubject.subscribe(postSongInfo)

hasPopup.popup()
