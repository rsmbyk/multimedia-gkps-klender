import { BehaviorSubject } from '/static/helpers/rx.js'

import * as PreviewManager from '../PreviewManager.js'

const modal = $('#modal-edit-item')
const modalHeader = $('#modal-edit-item-header')

const form = $('#modal-edit-item-form')

const errorMessages = form.find('.ui.error.message')
const titleErrorMessage = form.find('#form-edit-item-error-message-title')
const textErrorMessage = form.find('#form-edit-item-error-message-text')
const nonFieldErrorMessage = form.find('#form-edit-item-error-message-non-field')

const buttonCreate = modal.find('#modal-edit-item-button-create')
const buttonSave = modal.find('#modal-edit-item-button-save')
const buttonCancel = modal.find('#modal-edit-item-button-cancel')

let requestFunction
let insertAfter

const tatibSubject = new BehaviorSubject()
const tatibItemSubject = new BehaviorSubject()
const onSuccessSubject = new BehaviorSubject()
const insertAfterSubject = new BehaviorSubject()

form.form({
    fields: {
        title: {
            rules: [
                {
                    type: 'maxLength[64]',
                },
            ],
        },
        text: {
            rules: [
                {
                    type: 'empty',
                },
            ],
        },
    },
    inline: true,
    on: 'change',
    onValid: function() {
        const values = form.form('get values')
        PreviewManager.openModalPreview(values.title, values.text)
    },
    onInvalid: function() {
        const values = form.form('get values')
        PreviewManager.openModalPreview(values.title, values.text)
    }
})

const showLoader = () => {
    buttonCreate.addClass('loading disabled')
    buttonSave.addClass('loading disabled')
    buttonCancel.addClass('disabled')
}

const hideLoader = () => {
    buttonCreate.removeClass('loading disabled')
    buttonSave.removeClass('loading disabled')
    buttonCancel.removeClass('disabled')
}

const updateFormErrorMessages = responseJSON => {
    if (responseJSON === undefined)
        responseJSON = {non_field_errors: ['Network Error']}

    form.addClass('error')

    if (responseJSON.title !== undefined)
        titleErrorMessage.text(responseJSON.title.join('\n'))
    if (responseJSON.text !== undefined)
        textErrorMessage.text(responseJSON.number.join('\n'))
    if (responseJSON.non_field_errors !== undefined)
        nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
}

const sendCreateRequest = (formData, onSuccess) => {
    $.ajax({
        url: '/api/tatib/items',
        method: 'POST',
        data: formData,
        success: response => {
            console.log(response)
            modal.modal('hide')
            if (typeof onSuccess === 'function') onSuccess(response.order_number)
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            updateFormErrorMessages(responseJSON)
        },
        complete: () => {
            hideLoader()
        },
    })
}

const sendEditRequest = (formData, onSuccess) => {
    $.ajax({
        url: `/api/tatib/items/${formData.id}`,
        method: 'PATCH',
        data: formData,
        success: response => {
            console.log(response)
            modal.modal('hide')
            if (typeof onSuccess === 'function') onSuccess(response.order_number)
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            updateFormErrorMessages(responseJSON)
        },
        complete: () => {
            hideLoader()
        },
    })
}

const submitForm = onSuccess => {
    form.removeClass('error')
    errorMessages.empty()

    if (form.form('is valid')) {
        const { id, tatibId, title, text } = form.form('get values')

        const formData = {
            id: id,
            tatib: tatibId,
            item_type: 0,
            title: title,
            text: text,
            insert_after: insertAfter,
        }

        console.log(formData)
        showLoader()
        requestFunction(formData, onSuccess)
    }
    else {
        form.form('validate form')
    }
}

const updateModal = onSuccess => {
    modal.modal({
        closable: false,
        onHide: () => {
            form.form('clear')
        },
        onApprove: () => {
            submitForm(onSuccess)
            return false
        },
    })
}

const updateFormTatibIdValue = tatib => {
    form.form('set value', 'tatibId', tatib.id)
}

const updateRequestFunction = tatibItem => {
    requestFunction = tatibItem === null ? sendCreateRequest : sendEditRequest
}

const updateActionButtons = tatibItem => {
    if (tatibItem === null) {
        buttonSave.hide()
        buttonCreate.show()
    }
    else {
        buttonCreate.hide()
        buttonSave.show()
    }
}

const updateModalHeader = tatibItem => {
    modalHeader.text(tatibItem === null ? 'Create Item' : 'Edit Item')
}

function updateModalPreview(tatibItem) {
    PreviewManager.openModalPreview(tatibItem?.title ?? '', tatibItem?.text ?? '')
}

const updateFormValues = tatibItem => {
    if (tatibItem !== null) {
        form.form('set values', {
            id: tatibItem.id,
            title: tatibItem.title,
            text: tatibItem.text,
        })
    }

    hideLoader()
}

export const open = (tatibItem, tatib, onSuccess, insertAfter=null) => {
    showLoader()
    modal.modal('show')
    tatibSubject.next(tatib)
    tatibItemSubject.next(tatibItem)
    onSuccessSubject.next(onSuccess)
    insertAfterSubject.next(insertAfter)
}

tatibSubject.subscribe(updateFormTatibIdValue)

tatibItemSubject.subscribe(updateRequestFunction)
tatibItemSubject.subscribe(updateActionButtons)
tatibItemSubject.subscribe(updateModalHeader)
tatibItemSubject.subscribe(updateFormValues)
tatibItemSubject.subscribe(updateModalPreview)

onSuccessSubject.subscribe(updateModal)

insertAfterSubject.subscribe(value => insertAfter = value)
