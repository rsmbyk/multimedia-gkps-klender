const { BehaviorSubject } = rxjs

const BookmarkManager = (bookmarkStorage) => {
    const activeBookmark = new BehaviorSubject(bookmarkStorage.loadBookmark())
    const activeBookmarkItems = new BehaviorSubject(bookmarkStorage.loadBookmarkItems())

    const activateBookmark = (bookmark) => {
        bookmarkStorage.saveBookmark(bookmark.id)
        activeBookmark.next(bookmark.id)

        axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}`)
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
