const { BehaviorSubject, skipWhile } = rxjs

import * as doms from '/static/helpers/doms.js'

import * as editVerseModal from './modals/edit-verse.js'
import * as deleteVerseModal from './modals/delete-verse.js'

import * as PreviewManager from './PreviewManager.js'

const hasPopup = $('.hasPopup')

const verseList = $('#verse-list')

const songTitle = $('#song-title')
const songUntitled = $('#song-untitled')
const songBookNumber = $('#song-book-number')

const buttonAddVerse = $('#btn-add-verse')

const breadcrumb = $('#breadcrumb')
const breadcrumbBook = $('#breadcrumb-book')
const breadcrumbSong = $('#breadcrumb-song')

const placeholderSongInfo = $('#placeholder-song-info')
const placeholderVerseList = $('#placeholder-verse-list')
const containerVerseList = $('#container-verse-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

let song
let verses

const songSubject = new BehaviorSubject().pipe(skipWhile(song => song === undefined))
const versesSubject = new BehaviorSubject().pipe(skipWhile(verses => verses === undefined))

buttonAddVerse.click(() => {
    PreviewManager.closePreview()
    editVerseModal.open(null, song, verses.length + 1, retrieveVerses)
})

const showLoader = () => {
    buttonAddVerse.addClass('loading disabled')
}

const hideLoader = () => {
    buttonAddVerse.removeClass('loading disabled')
}

const displaySongInfoPlaceholder = () => {
    breadcrumb.hide()
    songTitle.hide()
    songBookNumber.hide()
    placeholderSongInfo.show()
}

const displayPlaceholder = () => {
    containerVerseList.hide()
    viewError.hide()
    viewEmpty.hide()
    placeholderVerseList.show()
}

const displaySongInfo = () => {
    placeholderSongInfo.hide()
    songTitle.show()
    songBookNumber.show()
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

const displayEmptyView = () => {
    placeholderVerseList.hide()
    viewEmpty.show()
}

const updateBreadcrumb = song => {
    breadcrumbBook.text(song.book.name)
    breadcrumbSong.text(song.book.is_hymn_book ? `${song.number}${song.sub_number}. ${song.title}` : song.title)

    breadcrumb.show()
}

const updateSongInfo = song => {
    songTitle.text(song.title)
    songBookNumber.text(song.book.is_hymn_book ? `${song.book.short_name} ${song.number}${song.sub_number}` : song.book.name)

    if (song.is_untitled) songUntitled.show()
    else songUntitled.hide()

    displaySongInfo()
}

const updateAddVerseButton = song => {
    if (song.book.is_hymn_book) buttonAddVerse.hide()
    else buttonAddVerse.show()
}

const createVerseListItem = verse => {
    const item = doms.createDOMFromJSON({
        tag: 'div',
        classList: ['item'],
        children: [
            {
                tag: 'div',
                classList: ['content'],
                children: [
                    {
                        tag: 'div',
                        classList: ['description'],
                        innerText: verse.lyric,
                    },
                ],
            },
            {
                tag: 'div',
                classList: ['extra'],
                children: [
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'buttons'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'secondary', 'icon', 'button', 'btnPreview'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['eye', 'icon'],
                                    },
                                ],
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'icon', 'button', 'btnEdit'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['pen', 'icon'],
                                    },
                                ],
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'red', 'icon', 'button', 'btnDelete'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['trash', 'icon'],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    })

    const extra = item.find('.extra')
    const buttonPreview = item.find('.btnPreview')
    const buttonEdit = item.find('.btnEdit')
    const buttonDelete = item.find('.btnDelete')

    item.hover(() => {
        if (song.book.is_hymn_book === false) extra.show()
        if (verse.number === verses.length) buttonDelete.show()
    }, () => {
        extra.hide()
        buttonDelete.hide()
    })

    buttonPreview.click(() => {
        PreviewManager.buildLyrics(verse.lyric)
    })

    buttonEdit.click(() => {
        PreviewManager.closePreview()
        editVerseModal.open(verse, song, verse.number, retrieveVerses)
    })

    buttonDelete.click(() => {
        PreviewManager.closePreview()
        deleteVerseModal.open(verse, song, retrieveVerses)
    })

    extra.hide()
    buttonDelete.hide()

    return item
}

const updateVerseList = verses => {
    verseList.empty()
    verseList.append(...verses.map(createVerseListItem))

    hideLoader()

    if (verses.length === 0) displayEmptyView()
    else displayVerseList()
}

const retrieveVerses = () => {
    showLoader()
    displayPlaceholder()

    axios.get(`/api/songs/verses?song=${songId}`)
        .then(({ data: verses }) => versesSubject.next(verses))
        .catch(displayErrorView)
}

const retrieveSong = () => {
    showLoader()
    displaySongInfoPlaceholder()
    displayPlaceholder()

    axios.get(`/api/songs/songs/${songId}`)
        .then(({ data: song }) => {
            songSubject.next(song)
            retrieveVerses()
        })
        .catch(displayErrorView)
}

songSubject.subscribe(value => song = value)
songSubject.subscribe(updateBreadcrumb)
songSubject.subscribe(updateSongInfo)
songSubject.subscribe(updateAddVerseButton)

versesSubject.subscribe(value => verses = value)
versesSubject.subscribe(updateVerseList)

hasPopup.popup()
retrieveSong()
