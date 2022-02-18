const LS_KEY_BOOKMARK = 'BOOKMARK'
const LS_KEY_BOOKMARK_ITEMS = 'BOOKMARK_ITEMS'

export const saveBookmark = bookmark => {
    console.log(bookmark)
    localStorage.setItem(LS_KEY_BOOKMARK, JSON.stringify(bookmark))
}

export const loadBookmark = () => {
    return JSON.parse(localStorage.getItem(LS_KEY_BOOKMARK))
}

export const removeBookmark = () => {
    localStorage.removeItem(LS_KEY_BOOKMARK)
}

export const saveBookmarkItems = bookmarkItems => {
    console.log(bookmarkItems)
    localStorage.setItem(LS_KEY_BOOKMARK_ITEMS, JSON.stringify(bookmarkItems))
}

export const loadBookmarkItems = () => {
    return JSON.parse(localStorage.getItem(LS_KEY_BOOKMARK_ITEMS))
}

export const removeBookmarkItems = () => {
    localStorage.removeItem(LS_KEY_BOOKMARK_ITEMS)
}
