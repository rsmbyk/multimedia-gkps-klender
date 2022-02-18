import * as toast from '../../common/toasts.js'

const modal = $('#modal-delete-bookmark-item')

const bookmarkItemName = modal.find('#bookmark-item-name')
const bookmarkName = modal.find('#bookmark-name')

const sendDeleteRequest = (bookmarkItem, onSuccess, onError) => {
    $.ajax({
        url: `/api/bookmarks/songs/items/${bookmarkItem.id}`,
        method: 'DELETE',
        success: response => {
            console.log(response)
            if (typeof (onSuccess) === "function") onSuccess(response)
            modal.modal('hide')
            toast.success('Item deleted successfully', 'bottom attached')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            if (typeof (onError) === "function") onError(responseJSON)
            toast.error('Delete item failed', 'bottom attached')
        },
    })
}

export const open = (bookmark, bookmarkItem, onSuccess, onError) => {
    modal.modal({
        allowMultiple: true,
        closable: false,
        centered: true,
        onApprove : () => {
            sendDeleteRequest(bookmarkItem, onSuccess, onError)
            return false
        },
    })

    const { song_info: { book_number, title }} = bookmarkItem

    bookmarkItemName.text(book_number ? book_number : title)

    let bookmarkDisplayName = bookmark.name

    if (bookmark.date !== null) {
        bookmarkDisplayName += ` (${new Date(bookmark.date).toLocaleString('en-us', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        })})`
    }

    bookmarkName.text(bookmarkDisplayName)

    modal.modal('show')
}
