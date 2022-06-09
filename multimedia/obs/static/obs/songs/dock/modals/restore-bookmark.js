import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-restore-bookmark')

const bookmarkName = modal.find('#modal-restore-bookmark-bookmark-name')
const bookmarkDate = modal.find('#modal-restore-bookmark-bookmark-date')

const buttonRestore = modal.find('#modal-restore-bookmark-button-restore')
const buttonCancel = modal.find('#modal-restore-bookmark-button-cancel')

const showLoader = () => {
    buttonRestore.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonRestore.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendRestoreRequest = (bookmark, onSuccess) => {
    $.ajax({
        url: `/api/bookmarks/songs/bookmarks/${bookmark.id}`,
        method: 'PATCH',
        data: {
            is_active: true,
        },
        success: response => {
            console.log(response)
            if (onSuccess instanceof Function) onSuccess(response)
            modal.modal('hide')
            toasts.success('Bookmark restored', 'bottom center')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Restore failed', 'bottom center')
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
            sendRestoreRequest(bookmark, onSuccess)
            return false
        },
    })
}

export const open = (bookmark, onSuccess) => {
    updateBookmarkInfo(bookmark)
    updateModalConfig(bookmark, onSuccess)
    modal.modal('show')
}
