import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-bookmark-item')

const bookmarkItemName = modal.find('#modal-delete-bookmark-item-bookmark-item-name')
const bookmarkName = modal.find('#modal-delete-bookmark-item-bookmark-name')

const buttonDelete = modal.find('#modal-delete-bookmark-item-button-delete')
const buttonCancel = modal.find('#modal-delete-bookmark-item-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (bookmarkItem, onSuccess) => {
    $.ajax({
        url: `/api/bookmarks/songs/items/${bookmarkItem.id}`,
        method: 'DELETE',
        success: response => {
            console.log(response)
            if (onSuccess instanceof Function) onSuccess(response)
            modal.modal('hide')
            toasts.success('Item deleted', 'bottom center')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete failed', 'bottom center')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateModalConfig = (bookmarkItem, onSuccess) => {
    modal.modal({
        allowMultiple: true,
        closable: false,
        onApprove : () => {
            showLoader()
            sendDeleteRequest(bookmarkItem, onSuccess)
            return false
        },
    })
}

const updateBookmarkInfo = bookmark => {
    let bookmarkDisplayName = bookmark.name

    if (bookmark.date !== null) {
        const date = new Date(bookmark.date)
        bookmarkDisplayName += ` (${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})})`
    }

    bookmarkName.text(bookmarkDisplayName)
}

const updateBookmarkItemInfo = bookmarkItem => {
    const { song_info: { book_number, title } } = bookmarkItem
    bookmarkItemName.text(book_number ? book_number : title)
}

export const open = (bookmark, bookmarkItem, onSuccess) => {
    updateModalConfig(bookmarkItem, onSuccess)
    updateBookmarkInfo(bookmark)
    updateBookmarkItemInfo(bookmarkItem)
    modal.modal('show')
}
