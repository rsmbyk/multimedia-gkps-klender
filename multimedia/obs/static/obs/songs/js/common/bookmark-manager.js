const { BehaviorSubject } = rxjs
import *  as bookmarkStorage from './bookmark-storage.js'

export let bookmark
export let bookmarkItems

export const bookmarkSubject = new BehaviorSubject(bookmarkStorage.loadBookmark())
export const bookmarkItemsSubject = new BehaviorSubject(bookmarkStorage.loadBookmarkItems())

export const activateBookmark = bookmark => {
    bookmarkStorage.saveBookmark(bookmark)
    bookmarkSubject.next(bookmark)
}

export const refreshBookmarkItems = () => {
    if (bookmark === null)
        return

    axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}`)
        .then(({ data: bookmarkItems }) => activateBookmarkItems(bookmarkItems))
}

const activateBookmarkItems = bookmarkItems => {
    bookmarkStorage.saveBookmarkItems(bookmarkItems)
    bookmarkItemsSubject.next(bookmarkItems)
}

export const activateSingleBookmarkItem = (book, song, verses) => {
    deactivate()
    activateBookmarkItems([{
        song_info: {
            book_number: book.is_hymn_book ? `${book.short_name} ${song.number}` : null,
            title: song.title,
        },
        verse_info: verses,
    }])
}

export const deactivate = () => {
    bookmarkStorage.removeBookmark()
    bookmarkStorage.removeBookmarkItems()
    bookmarkSubject.next(null)
    bookmarkItemsSubject.next(null)
}

bookmarkSubject.subscribe(value => bookmark = value)
bookmarkSubject.subscribe(refreshBookmarkItems)

bookmarkItemsSubject.subscribe(value => bookmarkItems = value)
