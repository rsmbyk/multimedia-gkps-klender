import { BehaviorSubject } from '/static/helpers/rx.js'
import * as doms from '/static/helpers/doms.js'
import * as mutations from '/static/helpers/mutations.js'
import * as toasts from '/static/helpers/toasts.js'

import * as bookmarkManager from '../common/bookmark-manager.js'

import * as songDetailModal from '../modals/song-detail.js'
import * as deleteBookmarkItemModal from '../modals/delete-bookmark-item.js'

const modal = $('#modal-bookmark-detail').modal({
    closable: false,
    allowMultiple: true,
    onHidden: () => {
        itemsOrderSubject.next(null)
    },
})

const bookmarkItemList = modal.find('#modal-bookmark-detail-bookmark-item-list')

const bookmarkName = modal.find('#modal-bookmark-detail-bookmark-name')
const bookmarkDate = modal.find('#modal-bookmark-detail-bookmark-date')

const buttonReorder = modal.find('#modal-bookmark-detail-button-reorder')
const buttonSave = modal.find('#modal-bookmark-detail-button-save')
const buttonDiscard = modal.find('#modal-bookmark-detail-button-discard')

const placeholderBookmarkInfo = modal.find('#modal-bookmark-detail-placeholder-bookmark-info')
const placeholderBookmarkItemList = modal.find('#modal-bookmark-detail-placeholder-bookmark-item-list')
const containerBookmarkItemList = modal.find('#modal-bookmark-detail-container-bookmark-item-list')
const viewEmpty = modal.find('#modal-bookmark-detail-view-empty')
const viewError = modal.find('#modal-bookmark-detail-view-error')

let bookmark
let bookmarkItems
let itemsOrder

const bookmarkSubject = new BehaviorSubject()
const bookmarkItemsSubject = new BehaviorSubject()
const itemsOrderSubject = new BehaviorSubject(null)

mutations.observeFlexModal(modal[0])

buttonReorder.click(() => {
    itemsOrderSubject.next(bookmarkItems)
})

buttonDiscard.click(() => {
    itemsOrderSubject.next(null)
})

const buildReorderRequestData = () => {
    return {
        items: itemsOrder.map((item, index) => {
            return {
                item: item.id,
                order_number: index + 1,
            }
        })
    }
}

buttonSave.click(() => {
    displayLoader()

    axios.post('/api/bookmarks/songs/items/reorder', buildReorderRequestData())
        .then(({ data }) => {
            itemsOrderSubject.next(null)
            retrieveBookmarkItems(bookmark)
            if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id)
                bookmarkManager.refreshBookmarkItems()
        })
        .catch(handleErrors)
        .finally(hideLoader)
})

const displayLoader = () => {
    buttonSave.addClass('loading disabled')
    buttonDiscard.addClass('disabled')
    bookmarkItemList.find('.btnUp').addClass('disabled')
    bookmarkItemList.find('.btnDown').addClass('disabled')
}

const hideLoader = () => {
    buttonSave.removeClass('loading disabled')
    buttonDiscard.removeClass('disabled')
    bookmarkItemList.find('.btnUp').removeClass('disabled')
    bookmarkItemList.find('.btnDown').removeClass('disabled')
}

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
    if (itemsOrder === null && bookmark.is_active) buttonReorder.show()
    else buttonReorder.hide()
}

const displayEmptyView = () => {
    placeholderBookmarkItemList.hide()
    viewEmpty.show()
    buttonReorder.hide()
}

const displayErrorView = e => {
    console.log(e)
    placeholderBookmarkItemList.hide()
    viewError.show()
    buttonReorder.hide()
}

const handleErrors = e => {
    if (e.response) {
        console.log(e.response.data)
        toasts.error('Reorder bookmark failed')
    } else if (e.request) {
        console.log(e.request)
        toasts.error('Network error')
    } else {
        console.log(e)
        toasts.error('Something went wrong. Please refresh the page.')
    }
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

const onItemsOrderChanged = itemsOrder => {
    if (itemsOrder !== null) {
        updateBookmarkItemList(itemsOrder)
        modal.modal('setting', 'closeIcon', false)
    } else if (bookmarkItems !== undefined) {
        updateBookmarkItemList(bookmarkItems)
        modal.modal('setting', 'closeIcon', true)
    }
}

const updateReorderSaveButton = itemsOrder => {
    if (itemsOrder === null || itemsOrder.equals(bookmarkItems)) {
        buttonSave.hide()
    } else {
        buttonSave.show()
    }
}

const updateReorderButtonsVisibility = itemsOrder => {
    if (itemsOrder !== null) {
        buttonReorder.hide()
        buttonDiscard.show()
    } else {
        buttonReorder.show()
        buttonDiscard.hide()
        buttonSave.hide()
    }
}

const updateBookmarkItemListSelectionMode = itemsOrder => {
    if (itemsOrder !== null) {
        bookmarkItemList.removeClass('selection')
    } else {
        bookmarkItemList.addClass('selection')
    }
}

const swapItem = (i1, i2) => {
    const newItemsOrder = itemsOrder.concat()
    const temp = newItemsOrder[i1]
    newItemsOrder[i1] = newItemsOrder[i2]
    newItemsOrder[i2] = temp
    return newItemsOrder
}

const moveItemUp = index => {
    if (index > 0)
        itemsOrderSubject.next(swapItem(index, index-1))
}

const moveItemDown = index => {
    if (index < bookmarkItems.length - 1)
        itemsOrderSubject.next(swapItem(index, index+1))
}

const createBookmarkItem = (bookmarkItem, index) => {
    const { song_info: { book_number, title, is_untitled }, verse } = bookmarkItem
    const songTitle = title + (is_untitled ? ' *' : '')
    const songBookNumber = book_number !== null ? `${book_number} : ${verse}` : '-'

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
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'tiny', 'icon', 'button', 'btnUp'],
                        children: [
                            {
                                tag: 'i',
                                classList: ['angle', 'up', 'icon'],
                            },
                        ],
                    },
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'tiny', 'icon', 'button', 'btnDown'],
                        children: [
                            {
                                tag: 'i',
                                classList: ['angle', 'down', 'icon'],
                            },
                        ],
                    },
                ],
            },
            {
                tag: 'div',
                classList: ['content'],
                children: [
                    {
                        tag: 'div',
                        classList: ['header'],
                        innerText: songTitle,
                    },
                    {
                        tag: 'div',
                        classList: ['description'],
                        innerText: songBookNumber,
                    },
                ],
            },
        ],
    })

    const buttonUp = item.find('.btnUp')
    const buttonDown = item.find('.btnDown')

    buttonUp.click(() => {
        moveItemUp(index)
    })

    buttonDown.click(() => {
        moveItemDown(index)
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

    if (itemsOrder === null) {
        buttonDelete.show()
        buttonUp.hide()
        buttonDown.hide()
    } else {
        buttonDelete.hide()
        buttonUp.show()
        buttonDown.show()
    }
    
    if (!bookmark.is_active) {
        buttonDelete.hide()
    }

    item.click(e => {
        if (buttonDelete[0].contains(e.target) || itemsOrder !== null)
            return false

        // only open song-detail-modal if clicking on
        // bookmark's content or background (anywhere
        // outside the delete button)
        if (bookmark.is_active) {
            songDetailModal.open(bookmarkItem.song, bookmarkItem, bookmark, () => retrieveBookmarkItems(bookmark))
        } else {
            songDetailModal.open(bookmarkItem.song, null, null, () => retrieveBookmarkItems(bookmark))
        }
    })

    if (itemsOrder !== null && itemsOrder[index].id !== bookmarkItems[index].id) {
        buttonUp.addClass('secondary')
        buttonDown.addClass('secondary')
    }

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

    axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}`)
        .then(({ data: bookmarkItems }) => bookmarkItemsSubject.next(bookmarkItems))
        .catch(displayErrorView)
}

export const open = bookmark => {
    displayBookmarkItemListPlaceholder()
    displayBookmarkInfoPlaceholder()
    buttonReorder.hide()
    hideLoader()
    modal.modal('show')
    retrieveBookmark(bookmark)
    retrieveBookmarkItems(bookmark)
}

bookmarkSubject.subscribe(value => bookmark = value)
bookmarkSubject.subscribe(retrieveBookmarkItems)
bookmarkSubject.subscribe(updateBookmarkInfo)

bookmarkItemsSubject.subscribe(value => bookmarkItems = value)
bookmarkItemsSubject.subscribe(updateBookmarkItemList)

itemsOrderSubject.subscribe(value => itemsOrder = value)
itemsOrderSubject.subscribe(onItemsOrderChanged)
itemsOrderSubject.subscribe(updateReorderButtonsVisibility)
itemsOrderSubject.subscribe(updateBookmarkItemListSelectionMode)
itemsOrderSubject.subscribe(updateReorderSaveButton)
