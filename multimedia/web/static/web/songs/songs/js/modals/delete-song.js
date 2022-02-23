import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-song')

const title = modal.find('#modal-delete-song-title')
const bookName = modal.find('#modal-delete-song-book-name')

const buttonDelete = modal.find('#modal-delete-song-button-delete')
const buttonCancel = modal.find('#modal-delete-song-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (song, onSuccess) => {
    $.ajax({
        url: `/api/songs/songs/${song.id}`,
        method: 'DELETE',
        success: response => {
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Song deleted', 'bottom left')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete song failed', 'bottom left')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateSongInfo = song => {
    title.text(song.title)
    bookName.text(song.book.name)
}

const updateModalConfig = (song, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove: () => {
            showLoader()
            sendDeleteRequest(song, onSuccess)
            return false
        }
    })
}

export const open = (song, onSuccess) => {
    updateSongInfo(song)
    updateModalConfig(song, onSuccess)
    modal.modal('show')
}
