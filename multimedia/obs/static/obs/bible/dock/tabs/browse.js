const { map } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js';

import * as doms from '/static/helpers/doms.js'
import * as tabManager from '/static/helpers/tab-manager.js'

import * as displayTab from './display.js'

const hasPopup = $('#tab-browse .hasPopup')

const verseList = $('#browse-verse-list')

const chapterInfo = $('#browse-chapter-info')
const headerBookName = $('#browse-book-name')
const headerChapterNumber = $('#browse-chapter-number')

const buttonPrevChapter = $('#browse-button-prev-chapter')
const buttonNextChapter = $('#browse-button-next-chapter')

const placeholderChapterInfo = $('#browse-placeholder-chapter-info')
const placeholderVerseList = $('#browse-placeholder-verse-list')
const containerVerseList = $('#browse-container-verse-list')
const viewInitial = $('#browse-view-initial')
const viewError = $('#browse-view-error')

let translation
let chapterNumber
let verses

const translationSubject = new BehaviorSubject()
const chapterNumberSubject = new BehaviorSubject().pipe(map(v => parseInt(v)))
const versesSubject = new BehaviorSubject()

buttonPrevChapter.click(() => {
    open(translation, chapterNumber - 1)
})

buttonNextChapter.click(() => {
    open(translation, chapterNumber + 1)
})

const showLoader = () => {
    buttonPrevChapter.addClass('disabled')
    buttonNextChapter.addClass('disabled')
}

const hideLoader = () => {
    buttonPrevChapter.removeClass('disabled')
    buttonNextChapter.removeClass('disabled')
}

const displayPlaceholders = () => {
    containerVerseList.hide()
    viewInitial.hide()
    viewError.hide()
    placeholderVerseList.show()
}

const displayChapterInfo = () => {
    placeholderChapterInfo.hide()
    chapterInfo.show()
}

const displayVerseList = () => {
    placeholderVerseList.hide()
    containerVerseList.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderVerseList.hide()
    viewError.show()
}

const updatePrevChapterButton = () => {
    if (chapterNumber === 1) buttonPrevChapter.addClass('disabled')
    else buttonPrevChapter.removeClass('disabled')
}

const updateNextChapterButton = () => {
    if (chapterNumber === translation.book.number_of_chapters) buttonNextChapter.addClass('disabled')
    else buttonNextChapter.removeClass('disabled')
}

const updateBookName = translation => {
    headerBookName.text(translation.translation)
}

const updateChapterNumber = chapterNumber => {
    headerChapterNumber.text(chapterNumber)
    displayChapterInfo()
}

const createVerseListItem = verse => {
    const item = doms.createDOMFromJSON({
        tag: 'div',
        classList: ['item'],
        children: [
            {
                tag: 'div',
                classList: ['ui', 'very', 'compact', 'grid'],
                children: [
                    {
                        tag: 'div',
                        classList: ['left', 'aligned', 'two', 'wide', 'column'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'tiny', 'header'],
                                children: [
                                    {
                                        tag: 'div',
                                        classList: ['sub', 'header'],
                                        innerText: `${verse.verse}.`,
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        tag: 'div',
                        classList: ['right', 'aligned', 'fourteen', 'wide', 'column'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'tiny', 'header'],
                                children: [
                                    {
                                        tag: 'div',
                                        classList: ['sub', 'header'],
                                        innerText: verse.title,
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        tag: 'div',
                        classList: ['sixteen', 'wide', 'column'],
                        children: [
                            {
                                tag: 'span',
                                classList: ['text'],
                                innerText: verse.text,
                            },
                        ],
                    },
                ],
            },
        ],
    })

    item.click(() => {
        displayTab.display(translation, chapterNumber, verses, verse.verse)
        displayTab.navigateTo()
    })

    return item
}

const updateVerseList = verses => {
    verseList.empty()
    verseList.append(...verses.map(createVerseListItem))

    hideLoader()
    updatePrevChapterButton()
    updateNextChapterButton()
    displayVerseList()
}

const retrieveVerses = (translation, chapterNumber) => {
    showLoader()
    displayPlaceholders()

    axios.get(`/api/bible/verses?book_translation=${translation.id}&chapter=${chapterNumber}&omit=id,book_translation,chapter`)
        .then(({ data: verses }) => versesSubject.next(verses))
        .catch(displayErrorView)
}

export const open = (translation, chapterNumber, verses) => {
    translationSubject.next(translation)
    chapterNumberSubject.next(chapterNumber)

    if (verses === undefined) retrieveVerses(translation, chapterNumber)
    else versesSubject.next(verses)
}

export const navigateTo = () => {
    tabManager.changeTab('tab-browse')
}

translationSubject.subscribe(v => translation = v)
translationSubject.subscribe(updateBookName)

chapterNumberSubject.subscribe(v => chapterNumber = v)
chapterNumberSubject.subscribe(updateChapterNumber)
chapterNumberSubject.subscribe(updatePrevChapterButton)
chapterNumberSubject.subscribe(updateNextChapterButton)

versesSubject.subscribe(v => verses = v)
versesSubject.subscribe(updateVerseList)

hasPopup.popup()

viewInitial.popup({
    target: '#tab-menu-bible'
})
