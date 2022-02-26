import { BehaviorSubject } from '/static/helpers/rx.js'
import * as doms from '/static/helpers/doms.js'
import * as mutations from '/static/helpers/mutations.js'

import * as bookmarkManager from '../../common/bookmark-manager.js'

import * as songDetailModal from '../modals/song-detail.js'
import * as deleteBookmarkItemModal from '../modals/delete-bookmark-item.js'

const modal = $('#modal-bookmark-detail').modal({
    closable: false,
    allowMultiple: true,
})

const bookmarkItemList = modal.find('#modal-bookmark-detail-bookmark-item-list')

const bookmarkName = modal.find('#modal-bookmark-detail-bookmark-name')
const bookmarkDate = modal.find('#modal-bookmark-detail-bookmark-date')

const placeholderBookmarkInfo = modal.find('#modal-bookmark-detail-placeholder-bookmark-info')
const placeholderBookmarkItemList = modal.find('#modal-bookmark-detail-placeholder-bookmark-item-list')
const containerBookmarkItemList = modal.find('#modal-bookmark-detail-container-bookmark-item-list')
const viewEmpty = modal.find('#modal-bookmark-detail-view-empty')
const viewError = modal.find('#modal-bookmark-detail-view-error')

let bookmark

const bookmarkSubject = new BehaviorSubject()
const bookmarkItemsSubject = new BehaviorSubject()

mutations.observeFlexModal(modal[0])

const displayBookmarkItemListPlaceholder = () => {
    containerBookmarkItemList.hide()
    viewError.hide()
    viewEmpty.hide()
    placeholderBookmarkItemList.show()
}

const displayBookmarkInfoPlaceholder = () => {
    bookmarkName.hide()
    bookmarkDate.hide()
    placeholderBookmarkInfo.show()
}

const displayBookmarkInfo = () => {
    placeholderBookmarkInfo.hide()
    bookmarkName.show()
    bookmarkDate.show()
}

const displayBookmarkItemList = () => {
    placeholderBookmarkItemList.hide()
    containerBookmarkItemList.show()
}

const displayEmptyView = () => {
    placeholderBookmarkItemList.hide()
    viewEmpty.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderBookmarkItemList.hide()
    viewError.show()
}

const updateBookmarkInfo = bookmark => {
    bookmarkName.text(bookmark.name)

    if (bookmark.date !== null) {
        const date = new Date(bookmark.date)
        const dateText = `${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`
        bookmarkDate.text(dateText)
    }
    else bookmarkDate.text('-')

    bookmarkDate.css('visibility', bookmark.date === null ? 'hidden' : 'visible')

    displayBookmarkInfo()
}

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
            () => {
                retrieveBookmarkItems(bookmark)
                if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id)
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

const updateBookmarkItemList = bookmarkItems => {
    bookmarkItemList.empty()
    bookmarkItemList.append(...bookmarkItems.map(createBookmarkItem))

    if (bookmarkItems.length === 0) displayEmptyView()
    else displayBookmarkItemList()
}

const retrieveBookmark = ({ id }) => {
    axios.get(`/api/bookmarks/songs/bookmarks/${id}`)
        .then(({ data: bookmark }) => bookmarkSubject.next(bookmark))
        .catch(displayErrorView)
}

const retrieveBookmarkItems = bookmark => {
    displayBookmarkItemListPlaceholder()

    axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}&omit=verse_info`)
        .then(({ data: bookmarkItems }) => bookmarkItemsSubject.next(bookmarkItems))
        .catch(displayErrorView)
}

export const open = bookmark => {
    displayBookmarkItemListPlaceholder()
    displayBookmarkInfoPlaceholder()
    modal.modal('show')
    retrieveBookmark(bookmark)
    retrieveBookmarkItems(bookmark)
}

bookmarkSubject.subscribe(value => bookmark = value)
bookmarkSubject.subscribe(retrieveBookmarkItems)
bookmarkSubject.subscribe(updateBookmarkInfo)

bookmarkItemsSubject.subscribe(updateBookmarkItemList)
