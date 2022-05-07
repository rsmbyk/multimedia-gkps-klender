import * as toasts from '/static/helpers/toasts.js'

const modal = $('#modal-delete-item')

const buttonDelete = modal.find('#modal-delete-item-button-delete')
const buttonCancel = modal.find('#modal-delete-item-button-cancel')

const showLoader = () => {
    buttonDelete.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonDelete.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const sendDeleteRequest = (item, onSuccess) => {
    $.ajax({
        url: `/api/tatib/items/${item.id}`,
        method: 'DELETE',
        success: response => {
            if (typeof onSuccess === "function") onSuccess(response)
            modal.modal('hide')
            toasts.success('Item deleted', 'bottom left')
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            toasts.error('Delete item failed', 'bottom left')
        },
        complete: () => {
            hideLoader()
        },
    })
}

const updateModalConfig = (item, onSuccess) => {
    modal.modal({
        closable: false,
        onApprove: () => {
            showLoader()
            sendDeleteRequest(item, onSuccess)
            return false
        }
    })
}

export const open = (tatibItem, onSuccess) => {
    updateModalConfig(tatibItem, onSuccess)
    modal.modal('show')
}
