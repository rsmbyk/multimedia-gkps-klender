const { BehaviorSubject } = rxjs
import * as songDetailModal from '../modals/song-detail.js'
import * as deleteBookmarkItemModal from '../modals/delete-bookmark-item.js'
import * as bookmarkManager from '../../common/bookmark-manager.js'
import * as doms from '../../../../../helpers/doms.js'

const modal = $('#modal-bookmark-detail').modal({
    closable: false,
    allowMultiple: true,
})

const bookmarkName     = modal.find('#bookmark-name')
const bookmarkDate     = modal.find('#bookmark-date')
const bookmarkItemList = modal.find('#bookmark-item-list')

const placeholderBookmarkInfo = modal.find('#modal-bookmark-detail-placeholder-bookmark-info')
const placeholderBookmarkItemList = modal.find('#modal-bookmark-detail-placeholder-bookmark-item-list')

let bookmark
let bookmarkItems

const bookmarkSubject = new BehaviorSubject()
const bookmarkItemsSubject = new BehaviorSubject()

const displayPlaceholder = () => {
    bookmarkName.hide()
    bookmarkDate.hide()
    bookmarkItemList.hide()

    placeholderBookmarkInfo.show()
    placeholderBookmarkItemList.show()
}

const hideBookmarkInfoPlaceholder = () => {
    bookmarkName.show()
    bookmarkDate.show()

    placeholderBookmarkInfo.hide()
}

const hideBookmarkItemListPlaceholder = () => {
    bookmarkItemList.show()

    placeholderBookmarkItemList.hide()
}

const retrieveBookmark = ({ id }) => {
    return axios.get(`/api/bookmarks/songs/bookmarks/${id}`)
        .then(({ data: bookmark }) => bookmarkSubject.next(bookmark))
        .catch(console.log)
}

const retrieveBookmarkItems = bookmark => {
    if (bookmark === undefined)
        return

    return axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}&omit=verse_info`)
        .then(({ data: bookmarkItems }) => bookmarkItemsSubject.next(bookmarkItems))
        .catch(console.log)
}

const updateBookmarkInfo = bookmark => {
    if (bookmark === undefined)
        return

    hideBookmarkInfoPlaceholder()

    bookmarkName.text(bookmark.name)

    if (bookmark.date !== null) bookmarkDate.text(bookmark.date)
    else bookmarkDate.text('-')

    bookmarkDate.css('visibility', bookmark.date === null ? 'hidden' : 'visible')
}

const updateBookmarkItemList = bookmarkItems => {
    if (bookmarkItems === undefined)
        return

    const createBookmarkItem = (bookmarkItem) => {
        const item = doms.createDOMFromJSON({
            tag: 'div',
            classList: ['item'],
            children: [
                {
                    tag: 'div',
                    classList: ['right', 'floated', 'content'],
                    children: [
                        {
                            tag: 'div',
                            classList: ['ui', 'mini', 'basic', 'red', 'icon', 'button', 'btnDelete'],
                            children: [
                                {
                                    tag: 'i',
                                    classList: ['trash', 'icon'],
                                },
                            ],
                        },
                    ],
                },
                {
                    tag: 'div',
                    classList: ['middle', 'aligned', 'content'],
                },
            ],
        })

        const buttonDelete = item.find('.btnDelete')
        buttonDelete.click(() => {
            deleteBookmarkItemModal.open(
                bookmark,
                bookmarkItem,
                function(e) {
                    console.log(e)
                    retrieveBookmarkItems(bookmark)
                    if (bookmark.id === bookmarkManager.bookmark.id)
                        bookmarkManager.refreshBookmarkItems()
                },
            )
        })

        const content = item.find('.content:not(.right.floated)')

        const { song_info: { book_number, title }, verse } = bookmarkItem
        const itemDisplayName = book_number ? `${book_number} : ${verse}` : title
        content.text(itemDisplayName)

        item.click(e => {
            if (e.target === e.currentTarget || e.target === content[0])
                // only open song-detail-modal if clicking on
                // bookmark's content or background
                songDetailModal.open(bookmarkItem.song)
        })

        return item
    }

    hideBookmarkItemListPlaceholder()

    bookmarkItemList.empty()
    bookmarkItemList.append(...bookmarkItems.map(createBookmarkItem))
}

export const open = bookmark => {
    displayPlaceholder()
    retrieveBookmark(bookmark)
    modal.modal('show')
}

bookmarkSubject.subscribe(value => bookmark = value)
bookmarkSubject.subscribe(retrieveBookmarkItems)
bookmarkSubject.subscribe(updateBookmarkInfo)

bookmarkItemsSubject.subscribe(value => bookmarkItems = value)
bookmarkItemsSubject.subscribe(updateBookmarkItemList)
