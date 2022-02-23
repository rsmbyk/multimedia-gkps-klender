import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-verse')

const number = modal.find('#modal-delete-verse-number')
const songTitle = modal.find('#modal-delete-verse-song-title')

const sendDeleteRequest = (verse, onSuccess) => {
    $.ajax({
        url: `/api/songs/verses/${verse.id}`,
        method: 'DELETE',
        success: response => {
            console.log(response)
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Verse deleted successfully')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete verse failed')
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
