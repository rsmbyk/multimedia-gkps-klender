import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-book')

const name = modal.find('#modal-delete-book-name')
const lang = modal.find('#modal-delete-book-lang')

const sendDeleteRequest = (book, onSuccess) => {
    $.ajax({
        url: `/api/songs/books/${book.id}`,
        method: 'DELETE',
        success: response => {
            console.log(response)
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Book deleted successfully')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete book failed')
        },
    })
}

const updateBookInfo = book => {
    name.text(book.name)
    lang.text(book.lang === 1 ? 'Simalungun' : 'Indonesia')
}

const updateModalConfig = (book, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove: () => {
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
