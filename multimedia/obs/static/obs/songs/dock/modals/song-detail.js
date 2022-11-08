const { map, scan } = rxjs

import '/static/helpers/arrays.js'
import { ToggleButton, ManualToggleButton } from '/static/helpers/buttons.js'
import { BehaviorSubject } from '/static/helpers/rx.js'
import * as dateUtil from '/static/helpers/date-util.js'
import * as doms from '/static/helpers/doms.js'
import * as mutations from '/static/helpers/mutations.js'
import * as toasts from '/static/helpers/toasts.js'
import * as tabManager from '/static/helpers/tab-manager.js'

import * as bookmarkManager from '../common/bookmark-manager.js'

const modal = $('#modal-song-detail').modal({
    closable: false,
    allowMultiple: true,
})

const verseList = $('#modal-song-detail-verse-list')

const songTitle = $('#modal-song-detail-song-title')
const songBookNumber = $('#modal-song-detail-song-book-number')

const buttonSave = $('#modal-song-detail-button-save')
const buttonDelete = $('#modal-song-detail-button-delete')
const buttonDisplay = $('#modal-song-detail-button-display')

const placeholderSongInfo = $('#modal-song-detail-placeholder-song-info')
const placeholderVerseList = $('#modal-song-detail-placeholder-verse-list')
const containerVerseList = $('#modal-song-detail-container-verse-list')
const viewEmpty = $('#modal-song-detail-view-empty')
const viewError = $('#modal-song-detail-view-error')

const actionToggleButton = new ManualToggleButton(buttonSave, buttonDelete)

let songTitlePopupTimer

let bookmarkItemId
let bookmarkedVerses
let selectedVerses

let bookmark
let song
let book
let verses

let onSave

const onSaveSubject = new BehaviorSubject()
const bookmarkSubject = new BehaviorSubject()
const songSubject = new BehaviorSubject()
const bookSubject = new BehaviorSubject()
const versesSubject = new BehaviorSubject()

const selectedVersesSubject = new BehaviorSubject([])
    .pipe(
        scan((selection, nextValue) => {
            /**
             * manipulate `selectedVerses` based on
             * value of `nextValue` passed to subject:
             * - array => return as is
             * - 0 => reset
             * - positive => add to selection
             * - negative => remove from selection
             */
            if (nextValue.constructor === Array) return nextValue
            if (nextValue === 0) return []
            if (nextValue > 0) return selection.concat(nextValue)
            return selection.filter(x => x !== -nextValue)
        }),
        map(selection => {
            return selection.sort()
        }),
    )

buttonSave.click(() => {
    showLoader()

    if (bookmarkedVerses.length === 0)
        sendCreateBookmarkItemRequest()
    else
        sendEditBookmarkItemRequest()
})

buttonDelete.click(() => {
    showLoader()
    sendDeleteBookmarkItemRequest()
})

buttonDisplay.click(() => {
    bookmarkManager.activateSingleBookmarkItem(book, song, verses)
    modal.modal('hide all')
    tabManager.changeTab('tab-display')
})

mutations.observeFlexModal(modal[0])

const showLoader = () => {
    buttonSave.addClass('loading disabled')
    buttonDelete.addClass('loading disabled')
    buttonDisplay.addClass('disabled')

    verseList.find('.btnAddToBookmark').addClass('disabled')
    verseList.find('.btnBookmarked').addClass('disabled')
}

const hideLoader = () => {
    buttonSave.removeClass('loading disabled')
    buttonDelete.removeClass('loading disabled')
    buttonDisplay.removeClass('disabled')

    verseList.find('.btnAddToBookmark').removeClass('disabled')
    verseList.find('.btnBookmarked').removeClass('disabled')
}

const displayPlaceholders = () => {
    songTitle.hide()
    songBookNumber.hide()
    containerVerseList.hide()
    viewEmpty.hide()
    viewError.hide()
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
    verseList.parent().show()
}

const displayEmptyView = () => {
    placeholderVerseList.hide()
    viewEmpty.show()
}

const displayErrorView = (e) => {
    console.log(e)
    placeholderVerseList.hide()
    viewError.show()
}

const sendCreateBookmarkItemRequest = () => {
    $.ajax({
        url: '/api/bookmarks/songs/items',
        method: 'POST',
        data: {
            bookmark: bookmark.id,
            song: song.id,
            verse: JSON.stringify(selectedVerses).slice(1, -1),
        },
        success: response => {
            console.log(response)
            if (onSave instanceof Function) {
                onSave()
            }

            if (bookmarkManager.bookmark.id === bookmark.id) {
                bookmarkManager.refreshBookmarkItems()
            }

            modal.modal('hide')
        },
        error: e => {
            console.log(e)
            toasts.error('Failed to add to bookmark')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const sendEditBookmarkItemRequest = () => {
    $.ajax({
        url: `/api/bookmarks/songs/items/${bookmarkItemId}`,
        method: 'PATCH',
        data: {
            verse: JSON.stringify(selectedVerses).slice(1, -1),
        },
        success: response => {
            console.log(response)
            if (onSave instanceof Function) {
                onSave()
            }

            if (bookmarkManager.bookmark.id === bookmark.id) {
                bookmarkManager.refreshBookmarkItems()
            }

            modal.modal('hide')
        },
        error: e => {
            console.log(e)
            toasts.error('Failed to save changes')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const sendDeleteBookmarkItemRequest = () => {
    $.ajax({
        url: `/api/bookmarks/songs/items/${bookmarkItemId}`,
        method: 'DELETE',
        success: (response) => {
            console.log(response)
            bookmarkManager.refreshBookmarkItems()
            modal.modal('hide')
        },

        error: e => {
            console.log(e)
            toasts.error('Failed to remove from bookmark')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateBookInfo = book => {
    songBookNumber.text(book.is_hymn_book ? `${book.short_name} ${song.number}${song.sub_number}` : book.name)
    displaySongInfo()
}

const updateSongInfo = song => {
    songTitle.text(song.title + (song.is_untitled ? ' *' : ''))
}

const updateActionButtons = selectedVerses => {
    if (bookmark === null) {
        actionToggleButton.setInactive()
        actionToggleButton.hide()
    }
    else if (selectedVerses.equals(bookmarkedVerses)) {
        actionToggleButton.setActive()
        actionToggleButton.hide()
    }
    else if (selectedVerses.length === 0) {
        actionToggleButton.setInactive()
        actionToggleButton.show()
    }
    else {
        actionToggleButton.setActive()
        actionToggleButton.show()
    }
}

const updateDisplayButton = verses => {
    if (verses.length === 0) buttonDisplay.hide()
    else buttonDisplay.show()
}

const updateBookmarkItem = (bookmarkItem) => {
    if (!bookmarkItem) {
        bookmarkItemId = null
        bookmarkedVerses = []
        selectedVersesSubject.next(0)
    } else {
        console.log(bookmarkItem)
        bookmarkItemId = bookmarkItem.id
        bookmarkedVerses = bookmarkItem.verse_info.map(v => v.number)
        selectedVersesSubject.next(bookmarkedVerses)
    }
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
                    {
                        tag: 'div',
                        classList: ['extra'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'right', 'floated', 'tiny', 'basic', 'button', 'btnAddToBookmark'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['bookmark', 'outline', 'icon'],
                                    },
                                    {
                                        tag: 'span',
                                        classList: ['text'],
                                        innerText: 'Add to Bookmark',
                                    }
                                ]
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'right', 'floated', 'tiny', 'teal', 'button', 'btnBookmarked'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['bookmark', 'icon'],
                                    },
                                    {
                                        tag: 'span',
                                        classList: ['text'],
                                        innerText: 'Bookmarked',
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    })

    const buttonAddToBookmark = item.find('.btnAddToBookmark')
    const buttonBookmarked = item.find('.btnBookmarked')
    const bookmarkToggleButton = new ToggleButton(buttonBookmarked, buttonAddToBookmark)

    if (bookmark !== null) {
        buttonAddToBookmark
            .attr('data-title', bookmark.name)
            .attr('data-content', dateUtil.formatLongDate(bookmark.date))
            .attr('data-position', 'left center')
            .attr('data-variation', 'mini')
            .popup()

        buttonBookmarked
            .attr('data-title', bookmark.name)
            .attr('data-content', dateUtil.formatLongDate(bookmark.date))
            .attr('data-position', 'left center')
            .attr('data-variation', 'mini inverted')
            .popup()
    }

    buttonAddToBookmark.click(() => selectedVersesSubject.next(verse.number))
    buttonBookmarked.click(() => selectedVersesSubject.next(-verse.number))

    if (bookmarkedVerses.includes(verse.number)) {
        bookmarkToggleButton.setActive()
        bookmarkToggleButton.show()
    }
    else {
        bookmarkToggleButton.setInactive()
        bookmarkToggleButton.hide()
    }

    item.hover(() => {
        if (bookmark !== null) bookmarkToggleButton.show()
    }, () => {
        if (!bookmarkToggleButton.isActive) bookmarkToggleButton.hide()
    })

    return item
}

const updateVerseList = verses => {
    verseList.empty()
    verseList.append(...verses.map(createVerseListItem))

    hideLoader()

    if (verses.length === 0) displayEmptyView()
    else displayVerseList()
}

const retrieveAdditionalSongInfo = ({ book, id }) => {
    axios.get(`/api/songs/books/${book.id}`)
        .then(({ data: book }) => bookSubject.next(book))
        .catch(displayErrorView)

    axios.get(`/api/songs/verses?song=${id}`)
        .then(({ data: verses }) => versesSubject.next(verses))
        .catch(displayErrorView)
}

const retrieveSong = songId => {
    axios.get(`/api/songs/songs/${songId}`)
        .then(({ data: song }) => songSubject.next(song))
        .catch(displayErrorView)
}

export const open = (songId, bookmarkItem, bookmark, onSave) => {
    buttonSave.hide()
    buttonDelete.hide()
    showLoader()
    displayPlaceholders()
    modal.modal('show')
    retrieveSong(songId)
    onSaveSubject.next(onSave)
    bookmarkSubject.next(bookmark || bookmarkManager.bookmark)
    updateBookmarkItem(bookmarkItem)
}

songTitle.click(() => {
    navigator.clipboard.writeText(song.title)
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

onSaveSubject.subscribe(value => onSave = value)

bookmarkSubject.subscribe(value => bookmark = value)

songSubject.subscribe(value => song = value)
songSubject.subscribe(retrieveAdditionalSongInfo)
songSubject.subscribe(updateSongInfo)

bookSubject.subscribe(value => book = value)
bookSubject.subscribe(updateBookInfo)

versesSubject.subscribe(value => verses = value)
versesSubject.subscribe(updateVerseList)
versesSubject.subscribe(updateDisplayButton)

selectedVersesSubject.subscribe(value => selectedVerses = value)
selectedVersesSubject.subscribe(updateActionButtons)
