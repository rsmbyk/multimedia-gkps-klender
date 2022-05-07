import * as tatibManager from '../common/tatib-manager.js'

const modal = $('#modal-paste')

const form = $('#modal-paste-form')

const buttonPaste = $('#modal-paste-button-paste')
const buttonCancel = $('#modal-paste-button-cancel')

const showLoader = () => {
    form.addClass('loading')
    buttonPaste.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    form.removeClass('loading')
    buttonPaste.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const displayText = () => {
    form.removeClass('error')

    if (form.form('is valid')) {
        const { text } = form.form('get values')

        showLoader()
        tatibManager.activateSingleTatibItem(text)
        modal.modal('hide')
    }
    else {
        form.form('validate form')
    }
}

const checkQuickPasteInTatibManager = () => {
    if (tatibManager.tatib !== null && tatibManager.tatib.name === '$QUICK_PASTE$')
        form.form('set value', 'text', tatibManager.tatibItems[0].text)
}

export const open = () => {
    checkQuickPasteInTatibManager()
    hideLoader()
    modal.modal('show')
}

modal.modal({
    closable: false,
    onHide: function() {
        form.form('clear')
    },
    onApprove: function() {
        displayText()
        return false
    },
})

form.form({
    fields: {
        text: ['empty'],
    },
    inline: true,
    on: 'change',
})
