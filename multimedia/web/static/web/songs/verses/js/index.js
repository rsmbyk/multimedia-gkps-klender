const { BehaviorSubject, skipWhile } = rxjs

import * as doms from '/static/helpers/doms.js'
import * as editVerseModal from '/static/web/songs/verses/js/modals/edit-verse.js'
import * as deleteVerseModal from '/static/web/songs/verses/js/modals/delete-verse.js'

const verseList = $('#verse-list')

const breadcrumbBook = $('#breadcrumb-book')
const breadcrumbSong = $('#breadcrumb-song')

const songTitle = $('#song-title')
const songBookNumber = $('#song-book-number')

const buttonAddVerse = $('#btn-add-verse')

const placeholderSongInfo = $('#placeholder-song-info')
const placeholderVerseList = $('#placeholder-verse-list')
const containerVerseList = $('#container-verse-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

let song
let verses

const songSubject = new BehaviorSubject().pipe(skipWhile(song => song === undefined))
const versesSubject = new BehaviorSubject().pipe(skipWhile(verses => verses === undefined))

buttonAddVerse.click(() => editVerseModal.open(null, song, verses.length + 1, retrieveVerses))

const showLoader = () => {
    buttonAddVerse.addClass('disabled')
}

const hideLoader = () => {
    buttonAddVerse.removeClass('disabled')
}

const displayPlaceholder = () => {
    songTitle.hide()
    songBookNumber.hide()
    containerVerseList.hide()

    viewError.hide()
    viewEmpty.hide()

    placeholderSongInfo.show()
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
    const buttonEdit = item.find('.btnEdit')
    const buttonDelete = item.find('.btnDelete')

    item.hover(() => {
        if (song.book.is_hymn_book === false) extra.show()
        if (verse.number === verses.length) buttonDelete.show()
    }, () => {
        extra.hide()
        buttonDelete.hide()
    })

    buttonEdit.click(() => {
        editVerseModal.open(verse, song, verse.number, retrieveVerses)
    })

    buttonDelete.click(() => {
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

const updateBreadcrumb = song => {
    breadcrumbBook.text(song.book.name)
    breadcrumbBook.attr('href', `/songs/books/${song.book.id}`)

    breadcrumbSong.text(song.book.is_hymn_book ? `${song.number}${song.sub_number}. ${song.title}` : song.title)
}

const updateSongInfo = song => {
    songTitle.text(song.title)
    songBookNumber.text(song.book.is_hymn_book ? `${song.book.short_name} ${song.number}${song.sub_number}` : song.book.name)

    displaySongInfo()
}

const updateAddVerseButton = song => {
    if (song.book.is_hymn_book) buttonAddVerse.hide()
    else buttonAddVerse.show()
}

const retrieveVerses = () => {
    showLoader()
    displayPlaceholder()

    Promise.all([axios.get(`/api/songs/songs/${songId}`), axios.get(`/api/songs/verses?song=${songId}`)])
        .then(([{ data: song }, { data: verses }]) => {
            songSubject.next(song)
            versesSubject.next(verses)
        })
        .catch(displayErrorView)
}

songSubject.subscribe(value => song = value)
songSubject.subscribe(updateSongInfo)
songSubject.subscribe(updateBreadcrumb)
songSubject.subscribe(updateAddVerseButton)

versesSubject.subscribe(value => verses = value)
versesSubject.subscribe(updateVerseList)

retrieveVerses()
