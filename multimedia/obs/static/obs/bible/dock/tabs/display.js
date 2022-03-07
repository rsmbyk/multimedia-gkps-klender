const { map } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'
import { ToggleButton } from '/static/helpers/buttons.js'
import * as tabManager from '/static/helpers/tab-manager.js'

import * as bc from '../../common/bc.js'

import * as historyManager from '../common/history-manager.js'

const hasPopup = $('#tab-display .hasPopup')

const textBookName = $('#display-book-name')
const textChapterNumber = $('#display-chapter-number')
const textVerseNumber = $('#display-verse-number')
const textVerseTitle = $('#display-verse-title')
const containerVerseTitle = $('#display-container-verse-title')
const textVerseText = $('#display-verse-text')

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevVerse = $('#display-button-prev-verse')
const buttonNextVerse = $('#display-button-next-verse')

const placeholderChapterNumber = $('#display-placeholder-chapter-number')
const placeholderVerseNumber = $('#display-placeholder-verse-number')
const placeholderPassage = $('#display-placeholder-passage')
const containerPassage = $('#display-container-passage')

let translation
let chapterNumber
let verses
let verseNumber

const translationSubject = new BehaviorSubject()
const chapterNumberSubject = new BehaviorSubject().pipe(map(v => parseInt(v)))
const versesSubject = new BehaviorSubject()
const verseNumberSubject = new BehaviorSubject()

buttonPrevVerse.click(() => {
    verseNumberSubject.next(verseNumber - 1)
})

buttonNextVerse.click(() => {
    verseNumberSubject.next(verseNumber + 1)
})

const displayChapterNumber = () => {
    placeholderChapterNumber.hide()
    textBookName.show()
    textChapterNumber.show()
}

const displayVerseNumber = () => {
    placeholderVerseNumber.hide()
    textVerseNumber.show()
}

const displayPassage = () => {
    placeholderPassage.hide()
    containerPassage.show()
}

const setIdle = () => {
    textBookName.hide()
    textChapterNumber.hide()
    textVerseNumber.hide()
    containerPassage.hide()

    placeholderChapterNumber.show()
    placeholderVerseNumber.show()
    placeholderPassage.show()

    buttonStatusActive.addClass('disabled')
    buttonStatusInactive.addClass('disabled')

    buttonPrevVerse.addClass('disabled')
    buttonNextVerse.addClass('disabled')
}

const activateStatusButton = () => {
    buttonStatusActive.removeClass('disabled')
    buttonStatusInactive.removeClass('disabled')
}

const updateBookName = translation => {
    textBookName.text(translation.translation)
}

const updateChapterNumber = chapterNumber => {
    textChapterNumber.text(chapterNumber)
    displayChapterNumber()
}

const updateVerseNumber = verseNumber => {
    textVerseNumber.text(verseNumber)
    displayVerseNumber()
}

const updatePassage = verseNumber => {
    const verse = verses.find(e => e.verse === verseNumber)
    textVerseTitle.text(verse.title)
    textVerseText.text(verse.text)

    if (verse.title.length === 0) containerVerseTitle.hide()
    else containerVerseTitle.show()

    displayPassage()
}

const updateStatusButton = status => {
    if (status === true && !toggleButtonStatus.isActive) toggleButtonStatus.setActive()
    else if (status === false && toggleButtonStatus.isActive) toggleButtonStatus.setInactive()
}

const updatePrevVerseButton = verseNumber => {
    if (verseNumber === 1) buttonPrevVerse.addClass('disabled')
    else buttonPrevVerse.removeClass('disabled')
}

const updateNextVerseButton = verseNumber => {
    if (verseNumber === verses.length) buttonNextVerse.addClass('disabled')
    else buttonNextVerse.removeClass('disabled')
}

const postStatusMessage = status => {
    bc.postStatusMessage(status)
}

const postPassage = () => {
    const verse = verses.find(e => e.verse === verseNumber)
    bc.postPassage(
        translation.translation,
        chapterNumber,
        verseNumber,
        verse.title,
        verse.text,
    )
}

export const display = (translation, chapterNumber, verses, verseNumber) => {
    translationSubject.next(translation)
    chapterNumberSubject.next(chapterNumber)
    versesSubject.next(verses)
    verseNumberSubject.next(verseNumber === undefined ? 1 : verseNumber)
    activateStatusButton()
    historyManager.addItem(translation, chapterNumber, verses, verseNumber)
}

export const navigateTo = () => {
    tabManager.changeTab('tab-display')
}

const toggleButtonStatus = new ToggleButton(
    buttonStatusActive,
    buttonStatusInactive,
    () => {
        postStatusMessage(true)
        postPassage()
    },
    () => {
        postStatusMessage(false)
    },
)

setIdle()

bc.statusSubject.subscribe(updateStatusButton)

translationSubject.subscribe(v => translation = v)
translationSubject.subscribe(updateBookName)

chapterNumberSubject.subscribe(v => chapterNumber = v)
chapterNumberSubject.subscribe(updateChapterNumber)

versesSubject.subscribe(v => verses = v)

verseNumberSubject.subscribe(v => verseNumber = v)
verseNumberSubject.subscribe(updateVerseNumber)
verseNumberSubject.subscribe(updatePassage)
verseNumberSubject.subscribe(updatePrevVerseButton)
verseNumberSubject.subscribe(updateNextVerseButton)
verseNumberSubject.subscribe(postPassage)

hasPopup.popup()
