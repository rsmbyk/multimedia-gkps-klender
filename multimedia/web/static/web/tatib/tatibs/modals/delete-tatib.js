import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-tatib')

const name = modal.find('#modal-delete-tatib-name')
const date = modal.find('#modal-delete-tatib-date')

const buttonDelete = modal.find('#modal-delete-tatib-button-delete')
const buttonCancel = modal.find('#modal-delete-tatib-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (tatib, onSuccess) => {
    $.ajax({
        url: `/api/tatib/tatibs/${tatib.id}`,
        method: 'DELETE',
        success: response => {
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Tata ibadah deleted', 'bottom left')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete tata ibadah failed', 'bottom left')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateTatibInfo = tatib => {
    const tatibDate = new Date(tatib.date)

    name.text(tatib.name)
    date.text(`${tatibDate.getDate()} ${tatibDate.toLocaleString('en-us', {
        month: 'long',
        year: 'numeric'
    })}`)
}

const updateModalConfig = (tatib, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove: () => {
            showLoader()
            sendDeleteRequest(tatib, onSuccess)
            return false
        }
    })
}

export const open = (tatib, onSuccess) => {
    updateTatibInfo(tatib)
    updateModalConfig(tatib, onSuccess)
    modal.modal('show')
}
