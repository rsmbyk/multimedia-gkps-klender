const BookmarkStorage = () => {
    const LOCAL_STORAGE_KEY_BOOKMARK = 'BOOKMARK'
    const LOCAL_STORAGE_KEY_BOOKMARK_ITEMS = 'BOOKMARK_ITEMS'

    const saveBookmark = (bookmark) => {
        localStorage.setItem(LOCAL_STORAGE_KEY_BOOKMARK, JSON.stringify(bookmark))
    }

    const loadBookmark = () => {
        let val = localStorage.getItem(LOCAL_STORAGE_KEY_BOOKMARK)
        if (val !== null) val = parseInt(val)
        return val
    }

    const removeBookmark = () => {
        localStorage.removeItem(LOCAL_STORAGE_KEY_BOOKMARK)
    }

    const saveBookmarkItems = (bookmarkItems) => {
        localStorage.setItem(LOCAL_STORAGE_KEY_BOOKMARK_ITEMS, JSON.stringify(bookmarkItems))
    }

    const loadBookmarkItems = () => {
        return JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY_BOOKMARK_ITEMS))
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
