const { BehaviorSubject } = rxjs

const BookmarkManager = (bookmarkStorage) => {
    let bookmark
    let bookmarkItems

    const activeBookmark = new BehaviorSubject(bookmarkStorage.loadBookmark())
    const activeBookmarkItems = new BehaviorSubject(bookmarkStorage.loadBookmarkItems())

    activeBookmark.subscribe(value => bookmark = value)
    activeBookmarkItems.subscribe(value => bookmarkItems = value)

    const activateBookmark = (bookmark) => {
        if (bookmark.hasOwnProperty('id'))
            bookmark = bookmark.id

        bookmarkStorage.saveBookmark(bookmark)
        activeBookmark.next(bookmark)

        axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark}`)
            .then(result => activateBookmarkItems(result.data))
    }

    const activateBookmarkItems = (bookmarkItems) => {
        bookmarkStorage.saveBookmarkItems(bookmarkItems)
        activeBookmarkItems.next(bookmarkItems)
    }

    const deactivate = () => {
        bookmarkStorage.removeBookmark()
        bookmarkStorage.removeBookmarkItems()
        activeBookmark.next(null)
        activeBookmarkItems.next(null)
    }

    return {
        activateBookmark,
        activateBookmarkItems,
        deactivate,
        activeBookmark,
        activeBookmarkItems,
    }
}
