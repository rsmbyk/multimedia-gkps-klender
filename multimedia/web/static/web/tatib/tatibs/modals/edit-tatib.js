import { BehaviorSubject } from '/static/helpers/rx.js'

const modal = $('#modal-edit-tatib')
const modalHeader = modal.find('#modal-edit-tatib-header')

const form = $('#modal-edit-tatib-form')

const formDateField = $('#modal-edit-tatib-form-date').parent().parent()

const formDateCalendar = form.find('.ui.calendar')
const formDateCheckbox = form.find('.ui.checkbox')

const errorMessages = form.find('.ui.error.message')
const nameErrorMessage = form.find('#modal-edit-tatib-form-error-message-name')
const dateErrorMessage = form.find('#modal-edit-tatib-form-error-message-date')
const nonFieldErrorMessage = form.find('#modal-edit-tatib-form-error-message-non-field')

const buttonCreate = modal.find('#modal-edit-tatib-button-create')
const buttonSave = modal.find('#modal-edit-tatib-button-save')
const buttonCancel = modal.find('#modal-edit-tatib-button-cancel')

let requestFunction

const tatibSubject = new BehaviorSubject()
const onSuccessSubject = new BehaviorSubject()

const getNextSundayDate = () => {
    const today = new Date(Date.now())
    return new Date(today.setDate(today.getDate() + ((7 - today.getDay()) % 7)))
}

formDateCalendar.calendar({
    type: 'date',
    selectAdjacentDays: true,
    firstDayOfWeek: 1,
    today: true,
    eventDates: [
        {
            date: getNextSundayDate(),
        },
    ],
    popupOptions: {
        observeChanges: false,
    },
    onChange: date => {
        if (date === null) {
            form.form('set value', 'date', '')
        } else {
            form.form('set value', 'date', `${date.getDate()} ${date.toLocaleString('en-us', {
                month: 'long',
                year: 'numeric'
            })}`)
        }
    }
})

form.form({
    fields: {
        name: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: 'maxLength[64]',
                },
                {
                    type: 'regExp[/^$|[a-z0-9 \(\)\-\:\&\|]$/i]',
                    prompt: '{name} can only contain alphanumeric, spaces, parentheses and these symbols: & : - |',
                },
            ],
        },
        date: {
            depends: 'noDate',
            rules: [
                {
                    type: 'empty',
                },
            ],
        },
    },
    inline: true,
    on: 'change',
})

formDateCheckbox.checkbox().first().checkbox({
    onChecked: function() {
        formDateField.removeClass('disabled')
        formDateCalendar.show()
    },
    onUnchecked: function() {
        formDateField.addClass('disabled')
        formDateCalendar.hide()
        form.form('set value', 'date', '')
        form.form('validate field', 'date')
    },
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

    if (responseJSON.name !== undefined)
        nameErrorMessage.text(responseJSON.name.join('\n'))
    if (responseJSON.date !== undefined)
        dateErrorMessage.text(responseJSON.date.join('\n'))
    if (responseJSON.non_field_errors !== undefined)
        nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
}

const sendCreateRequest = (formData, onSuccess) => {
    $.ajax({
        url: '/api/tatib/tatibs',
        method: 'POST',
        data: formData,
        success: response => {
            console.log(response)
            modal.modal('hide')
            if (onSuccess instanceof Function) onSuccess(response)
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
        url: `/api/tatib/tatibs/${formData.id}`,
        method: 'PATCH',
        data: formData,
        success: response => {
            console.log(response)
            modal.modal('hide')
            if (typeof onSuccess === "function") onSuccess(response)
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
        const { id, name, noDate } = form.form('get values')
        const date = formDateCalendar.calendar('get date')

        const formData = {
            id: id,
            name: name.trim(),
            date: noDate ? `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}` : null,
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
        onHide: function() {
            form.form('clear')
            formDateCheckbox.checkbox('set checked')
            formDateCalendar.calendar('clear')
            formDateCalendar.removeClass('disabled')
        },
        onApprove: function() {
            submitForm(onSuccess)
            return false
        },
    })
}

const updateModalHeader = tatib => {
    modalHeader.text(tatib === null ? 'Create Tata Ibadah' : 'Edit Tata Ibadah')
}

const updateActionButtons = tatib => {
    if (tatib === null) {
        buttonSave.hide()
        buttonCreate.show()
    }
    else {
        buttonCreate.hide()
        buttonSave.show()
    }
}

const updateTatibFormValues = tatib => {
    if (tatib !== null) {
        if (tatib.date === null) formDateCalendar.calendar('clear')
        else formDateCalendar.calendar('set date', new Date(tatib.date))

        form.form('set values', {
            id: tatib.id,
            name: tatib.name,
            noDate: tatib.date !== null,
        })
    }

    hideLoader()
}

const updateRequestFunction = tatib => {
    if (tatib === null) requestFunction = sendCreateRequest
    else requestFunction = sendEditRequest
}

export const open = (tatib, onSuccess) => {
    showLoader()
    modal.modal('show')
    onSuccessSubject.next(onSuccess)
    tatibSubject.next(tatib)
}

tatibSubject.subscribe(updateRequestFunction)
tatibSubject.subscribe(updateActionButtons)
tatibSubject.subscribe(updateModalHeader)
tatibSubject.subscribe(updateTatibFormValues)

onSuccessSubject.subscribe(updateModal)
