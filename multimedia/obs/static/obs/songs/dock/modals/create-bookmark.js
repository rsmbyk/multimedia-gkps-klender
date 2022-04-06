const modal = $('#modal-create-bookmark')

const form  = $('#modal-create-bookmark-form')

const formDateCalendar = form.find('.ui.calendar')
const formDateCheckbox = form.find('.ui.checkbox')

const errorMessages = form.find('.ui.error.message')
const nameErrorMessage = form.find('#modal-create-bookmark-form-error-message-name')
const dateErrorMessage = form.find('#modal-create-bookmark-form-error-message-date')
const nonFieldErrorMessage = form.find('#modal-create-bookmark-form-error-message-non-field')

const buttonCreate = modal.find('#modal-create-bookmark-button-create')

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
})

form.form({
    fields: {
        name: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: 'maxLength[20]',
                },
                {
                    type: 'regExp[/^[a-z0-9 ()]+$/i]',
                    prompt: '{name} can only contains alphanumeric, spaces and parentheses.',
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
        formDateCalendar.removeClass('disabled')
    },
    onUnchecked: function() {
        formDateCalendar.calendar('clear')
        formDateCalendar.addClass('disabled')
        form.form('validate field', 'date')
    },
})

const showLoader = () => {
    buttonCreate.addClass('loading disabled')
}

const hideLoader = () => {
    buttonCreate.removeClass('loading disabled')
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
        url: '/api/bookmarks/songs/bookmarks',
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

const submitForm = onSuccess => {
    form.removeClass('error')
    errorMessages.empty()

    if (form.form('is valid')) {
        const { name, date, noDate } = form.form('get values')

        const formData = {
            name: name.trim(),
            date: noDate ? `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}` : null,
        }

        console.log(formData)
        showLoader()
        sendCreateRequest(formData, onSuccess)
    }
    else {
        form.form('validate form')
    }
}

export const open = onSuccess => {
    modal.modal({
        closable: false,
        onHide: function() {
            form.form('clear')
            formDateCheckbox.checkbox('set checked')
            formDateCalendar.removeClass('disabled')
        },
        onApprove: function() {
            submitForm(onSuccess)
            return false
        },
    })
    modal.modal('show')
}
