const { map, scan, BehaviorSubject } = rxjs
import * as bookmarkManager from '../../common/bookmark-manager.js'
import * as tabManager from '../../common/tab-manager.js'
import * as doms from '../../../../../helpers/doms.js'
import * as toasts from '../../common/toasts.js'

const modal = $('#modal-song-detail').modal({
    closable: false,
    allowMultiple: true,
})

const header        = $('#modal-song-detail-header')
const subheader     = $('#modal-song-detail-subheader')
const verseList     = $('#modal-song-detail-verse-list')
const buttonSave    = $('#modal-song-detail-btn-save')
const buttonDelete  = $('#modal-song-detail-btn-delete')
const buttonDisplay = $('#modal-song-detail-btn-display')

const placeholderSongInfo = $('#modal-song-detail-placeholder-song-info')
const placeholderVerseList = $('#modal-song-detail-placeholder-verse-list')

const actionToggleButton = new ManualToggleButton(buttonSave, buttonDelete)

let selectedVerses
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
        map(selection => selection.sort())
    )

let bookmarkItemId
let bookmarkedVerses

let song
let book
let verses

const songSubject = new BehaviorSubject()
const bookSubject = new BehaviorSubject()
const versesSubject = new BehaviorSubject()

const evaluateActionButtonState = selectedVerses => {
    if (selectedVerses === undefined)
        return

    if (bookmarkManager.bookmark === null) {
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

buttonSave.click(() => {
    if (bookmarkedVerses.length === 0)
        sendCreateBookmarkItemRequest()
    else
        sendEditBookmarkItemRequest()
})

buttonDelete.click(() => {
    sendDeleteBookmarkItemRequest()
})

buttonDisplay.click(() => {
    bookmarkManager.activateSingleBookmarkItem(book, song, verses)
    modal.modal('hide all')
    tabManager.changeTab('tab-display')
})

const displayPlaceholders = () => {
    header.hide()
    subheader.hide()
    verseList.hide()

    placeholderSongInfo.show()
    placeholderVerseList.show()
}

const hideSongInfoPlaceholder = () => {
    header.show()
    subheader.show()

    placeholderSongInfo.hide()
}

const hideVerseListPlaceholder = () => {
    verseList.show()

    placeholderVerseList.hide()
}

const displayLoader = () => {
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

const sendCreateBookmarkItemRequest = () => {
    displayLoader()

    $.ajax({
        url: '/api/bookmarks/songs/items',
        method: 'POST',
        data: {
            bookmark: bookmarkManager.bookmark.id,
            song: song.id,
            verse: JSON.stringify(selectedVerses).slice(1, -1),
        },
        success: response => {
            console.log(response)
            bookmarkManager.refreshBookmarkItems()
            modal.modal('hide')
        },
        error: e => {
            console.log(e)
            toasts.error('Failed to add to bookmark')
            hideLoader()
        },
    })
}

const sendEditBookmarkItemRequest = () => {
    displayLoader()

    $.ajax({
        url: `/api/bookmarks/songs/items/${bookmarkItemId}`,
        method: 'PATCH',
        data: {
            verse: JSON.stringify(selectedVerses).slice(1, -1),
        },
        success: response => {
            console.log(response)
            bookmarkManager.refreshBookmarkItems()
            modal.modal('hide')
        },
        error: e => {
            console.log(e)
            toasts.error('Failed to save changes')
            hideLoader()
        },
    })
}

const sendDeleteBookmarkItemRequest = () => {
    displayLoader()

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
            hideLoader()
        },
    })
}

const updateBookInfo = book => {
    if (book === undefined)
        return

    hideSongInfoPlaceholder()
    subheader.text(book.is_hymn_book ? `${book.short_name} ${song.number}${song.sub_number}` : book.name)
}

const updateSongInfo = song => {
    if (song === undefined)
        return

    header.text(song.title)
}

const updateVerseList = verses => {
    if (verses === undefined)
        return

    const createVerseItem = (verse) => {
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

        buttonAddToBookmark.click(() => selectedVersesSubject.next(verse.number))
        buttonBookmarked.click(() => selectedVersesSubject.next(-verse.number))

        const bookmarkToggleButton = new ToggleButton(buttonBookmarked, buttonAddToBookmark)

        if (bookmarkedVerses.includes(verse.number)) {
            bookmarkToggleButton.setActive()
            bookmarkToggleButton.show()
        }
        else {
            bookmarkToggleButton.setInactive()
            bookmarkToggleButton.hide()
        }

        item.hover(() => {
            if (bookmarkManager.bookmark !== null) bookmarkToggleButton.show()
        }, () => {
            if (!bookmarkToggleButton.isActive) bookmarkToggleButton.hide()
        })

        return item
    }

    bookmarkItemId = null
    bookmarkedVerses = []
    selectedVersesSubject.next(0)

    if (bookmarkManager.bookmark !== null && bookmarkManager.bookmarkItems !== null) {
        const songItem = bookmarkManager.bookmarkItems.filter(item => item.song === song.id)
        if (songItem.length === 1) {
            // the opened song is included in the active bookmark
            bookmarkItemId = songItem[0].id
            bookmarkedVerses = songItem[0].verse_info.map(v => v.number)
            selectedVersesSubject.next(bookmarkedVerses)
        }
    }

    hideLoader()
    hideVerseListPlaceholder()
    verseList.empty()
    verseList.append(...verses.map(createVerseItem))
}

const retrieveAdditionalSongInfo = song => {
    if (song === undefined)
        return

    const { book, id } = song

    axios.get(`/api/songs/books/${book.id}`)
        .then(({ data: book }) => bookSubject.next(book))

    axios.get(`/api/songs/verses?song=${id}`)
        .then(({ data: verses }) => versesSubject.next(verses))
}

const retrieveSong = songId => {
    axios.get(`/api/songs/songs/${songId}`)
        .then(({ data: song }) => songSubject.next(song))
}

export const open = songId => {
    retrieveSong(songId)
    buttonSave.hide()
    buttonDelete.hide()
    displayLoader()
    displayPlaceholders()
    modal.modal('show')
}

songSubject.subscribe(value => song = value)
songSubject.subscribe(retrieveAdditionalSongInfo)
songSubject.subscribe(updateSongInfo)

bookSubject.subscribe(value => book = value)
bookSubject.subscribe(updateBookInfo)

versesSubject.subscribe(value => verses = value)
versesSubject.subscribe(updateVerseList)

selectedVersesSubject.subscribe(value => selectedVerses = value)
selectedVersesSubject.subscribe(evaluateActionButtonState)
