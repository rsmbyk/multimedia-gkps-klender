import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-book')

const name = modal.find('#modal-delete-book-name')

const buttonDelete = modal.find('#modal-delete-book-button-delete')
const buttonCancel = modal.find('#modal-delete-book-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (book, onSuccess) => {
    $.ajax({
        url: `/api/songs/books/${book.id}`,
        method: 'DELETE',
        success: response => {
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Book deleted', 'bottom left')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete book failed', 'bottom left')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateBookInfo = book => {
    name.text(book.name)
}

const updateModalConfig = (book, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove: () => {
            showLoader()
            sendDeleteRequest(book, onSuccess)
            return false
        }
    })
}

export const open = (book, onSuccess) => {
    updateBookInfo(book)
    updateModalConfig(book, onSuccess)
    modal.modal('show')
}
