const modal = $('#modal-create-bookmark')
const form  = $('#form-create-bookmark')

const nameErrorMessage     = form.find('#name-error-message')
const dateErrorMessage     = form.find('#date-error-message')
const nonFieldErrorMessage = form.find('#non-field-error-message')
const errorMessages        = form.find('.ui.error.message')

const formDateCalendar = form.find('.ui.calendar')
const formDateCheckbox = form.find('.ui.checkbox')

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

const submitForm = onSuccess => {
    form.removeClass('error')
    errorMessages.empty()

    if (form.form('is valid')) {
        const { name, date, noDate } = form.form('get values')

        const formData = {
            name: name.trim(),
            date: noDate ? `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}` : null,
        }

        $.ajax({
            url: '/api/bookmarks/songs/bookmarks',
            method: 'POST',
            data: formData,
            success: response => {
                console.log(response)
                if (typeof (onSuccess) === "function") onSuccess(response)
                modal.modal('hide')
            },
            error: ({ responseJSON }) => {
                console.log(responseJSON)
                form.addClass('error')

                if (responseJSON.name !== undefined)
                    nameErrorMessage.text(responseJSON.name.join('\n'))
                if (responseJSON.date !== undefined)
                    dateErrorMessage.text(responseJSON.date.join('\n'))
                if (responseJSON.non_field_errors !== undefined)
                    nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
            },
        })
    }
    else {
        form.form('validate form')
    }
}

const getNextSundayDate = () => {
    const today = new Date(Date.now())
    return new Date(today.setDate(today.getDate() + ((7 - today.getDay()) % 7)))
}

formDateCalendar.calendar({
    type: 'date',
    selectAdjacentDays: true,
    firstDayOfWeek: 1,
    disabledDaysOfWeek: [1, 2, 3, 4, 5],
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
                    type: 'regExp[/^[a-z0-9 ]+$/i]',
                    prompt: '{name} can only contains alphanumeric and spaces.',
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
    on: 'blur',
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
