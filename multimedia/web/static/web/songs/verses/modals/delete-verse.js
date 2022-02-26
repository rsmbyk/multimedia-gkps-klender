import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-verse')

const number = modal.find('#modal-delete-verse-number')
const songTitle = modal.find('#modal-delete-verse-song-title')

const buttonDelete = modal.find('#modal-delete-verse-button-delete')
const buttonCancel = modal.find('#modal-delete-verse-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (verse, onSuccess) => {
    $.ajax({
        url: `/api/songs/verses/${verse.id}`,
        method: 'DELETE',
        success: response => {
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Verse deleted', 'bottom left')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete verse failed', 'bottom left')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateVerseNumber = verse => {
    number.text(verse.number)
}

const updateSongTitle = song => {
    songTitle.text(song.title)
}

const updateModalConfig = (verse, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove: () => {
            showLoader()
            sendDeleteRequest(verse, onSuccess)
            return false
        }
    })
}

export const open = (verse, song, onSuccess) => {
    updateVerseNumber(verse)
    updateSongTitle(song)
    updateModalConfig(verse, onSuccess)
    modal.modal('show')
}
