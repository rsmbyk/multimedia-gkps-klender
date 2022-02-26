import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-bookmark')

const bookmarkName = modal.find('#modal-delete-bookmark-bookmark-name')
const bookmarkDate = modal.find('#modal-delete-bookmark-bookmark-date')

const buttonDelete = modal.find('#modal-delete-bookmark-button-delete')
const buttonCancel = modal.find('#modal-delete-bookmark-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (bookmark, onSuccess) => {
    $.ajax({
        url: `/api/bookmarks/songs/bookmarks/${bookmark.id}`,
        method: 'PATCH',
        data: {
            is_active: false,
        },
        success: response => {
            console.log(response)
            if (onSuccess instanceof Function) onSuccess(response)
            modal.modal('hide')
            toasts.success('Bookmark deleted', 'bottom center')
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

const updateBookmarkInfo = bookmark => {
    bookmarkName.text(bookmark.name)

    bookmarkDate.text(new Date(bookmark.date).toLocaleString('en-us', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    }))
}

const updateModalConfig = (bookmark, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove : () => {
            showLoader()
            sendDeleteRequest(bookmark, onSuccess)
            return false
        },
    })
}

export const open = (bookmark, onSuccess) => {
    updateBookmarkInfo(bookmark)
    updateModalConfig(bookmark, onSuccess)
    modal.modal('show')
}
