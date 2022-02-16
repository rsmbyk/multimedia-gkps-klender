import * as toast from '../../common/toasts.js';

const modal = $('#modal-delete-bookmark')

const bookmarkName = modal.find('.content #bookmark-name')
const bookmarkDate = modal.find('.content #bookmark-date')

const sendDeleteRequest = (bookmark, onSuccess, onError) => {
    $.ajax({
        url: `/api/bookmarks/songs/bookmarks/${bookmark.id}`,
        method: 'PATCH',
        data: {
            is_active: false,
        },
        success: response => {
            console.log(response)
            if (typeof (onSuccess) === "function") onSuccess(response)
            modal.modal('hide')
            toast.success('Bookmark deleted successfully')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            if (typeof (onError) === "function") onError(responseJSON)
            toast.error('Delete bookmark failed')
        },
    })
}

export const open = (bookmark, onSuccess, onError) => {
    modal.modal({
        closable: false,
        onApprove : () => {
            sendDeleteRequest(bookmark, onSuccess, onError)
            return false
        },
    })

    bookmarkName.text(bookmark.name)

    bookmarkDate.text(new Date(bookmark.date).toLocaleString('en-us', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    }))

    modal.modal('show')
}
