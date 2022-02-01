const BookmarkStorage = () => {
    const LOCAL_STORAGE_KEY_BOOKMARK = 'BOOKMARK'
    const LOCAL_STORAGE_KEY_BOOKMARK_ITEMS = 'BOOKMARK_ITEMS'

    const saveBookmark = (bookmark) => {
        localStorage.setItem(LOCAL_STORAGE_KEY_BOOKMARK, JSON.stringify(bookmark))
    }

    const loadBookmark = () => {
        return parseInt(localStorage.getItem(LOCAL_STORAGE_KEY_BOOKMARK))
    }

    const removeBookmark = () => {
        localStorage.removeItem(LOCAL_STORAGE_KEY_BOOKMARK)
    }

    const saveBookmarkItems = (bookmarkItems) => {
        localStorage.setItem(LOCAL_STORAGE_KEY_BOOKMARK_ITEMS, JSON.stringify(bookmarkItems))
    }

    const loadBookmarkItems = () => {
        return localStorage.getItem(LOCAL_STORAGE_KEY_BOOKMARK_ITEMS)
    }

    const removeBookmarkItems = () => {
        localStorage.removeItem(LOCAL_STORAGE_KEY_BOOKMARK_ITEMS)
    }

    return {
        saveBookmark,
        loadBookmark,
        removeBookmark,
        saveBookmarkItems,
        loadBookmarkItems,
        removeBookmarkItems,
    }
}
