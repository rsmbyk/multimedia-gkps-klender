const { BehaviorSubject, skipWhile } = rxjs

const modal = $('#modal-edit-book')

const form = $('#form-edit-book')
const dropdownLang = $('#form-edit-book-lang-dropdown')

const errorMessages = form.find('.ui.error.message')
const nameErrorMessage = form.find('#modal-edit-book-error-message-name')
const nonFieldErrorMessage = form.find('#modal-edit-book-error-message-non-field')

const buttonCreate = modal.find('#modal-edit-book-button-create')
const buttonSave = modal.find('#modal-edit-book-button-save')

let requestFunction

const bookSubject = new BehaviorSubject().pipe(skipWhile(book => book === undefined))
const onSuccessSubject = new BehaviorSubject().pipe(skipWhile(onSuccess => onSuccess === undefined))

dropdownLang.dropdown()

form.form({
    fields: {
        name: {
            rules: [
                {
                    type: 'empty',
                },
                {
                    type: 'maxLength[32]',
                },
                {
                    type: 'regExp[/^[a-z0-9 ]+$/i]',
                    prompt: '{name} can only contains alphanumeric and spaces.',
                },
            ],
        },
        lang: 'empty',
    },
    inline: true,
    on: 'blur',
})

const showLoader = () => {
    form.addClass('loading')
}

const hideLoader = () => {
    form.removeClass('loading')
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

const submitForm = onSuccess => {
    form.removeClass('error')
    errorMessages.empty()

    if (form.form('is valid')) {
        const { id, name, lang } = form.form('get values')

        const formData = {
            id: id,
            name: name.trim(),
            lang: lang,
        }

        console.log(formData)
        requestFunction(formData, onSuccess)
    }
}

const sendCreateBookRequest = (formData, onSuccess) => {
    $.ajax({
        url: '/api/songs/books',
        method: 'POST',
        data: formData,
        success: response => {
            console.log(response)
            modal.modal('hide')
            if (typeof onSuccess === "function") onSuccess(response)
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            form.addClass('error')

            if (responseJSON.name !== undefined)
                nameErrorMessage.text(responseJSON.name.join('\n'))
            if (responseJSON.non_field_errors !== undefined)
                nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
        },
    })
}

const sendEditBookRequest = (formData, onSuccess) => {
    $.ajax({
        url: `/api/songs/books/${formData.id}`,
        method: 'PUT',
        data: formData,
        success: response => {
            console.log(response)
            modal.modal('hide')
            if (typeof onSuccess === "function") onSuccess(response)
        },
        error: ({ responseJSON }) => {
            console.log(responseJSON)
            form.addClass('error')

            if (responseJSON.name !== undefined)
                nameErrorMessage.text(responseJSON.name.join('\n'))
            if (responseJSON.non_field_errors !== undefined)
                nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
        },
    })
}

const updateBookFormValues = book => {
    if (book !== null) {
        form.form('set values', {
            id: book.id,
            name: book.name,
            lang: book.lang,
        })
    }

    hideLoader()
}

const updateActionButtons = book => {
    console.log(book)
    if (book === null) {
        buttonSave.hide()
        buttonCreate.show()
    }
    else {
        buttonCreate.hide()
        buttonSave.show()
    }
}

const updateRequestFunction = book => {
    if (book === null) requestFunction = sendCreateBookRequest
    else requestFunction = sendEditBookRequest
}

export const open = (book, onSuccess) => {
    showLoader()
    modal.modal('show')
    onSuccessSubject.next(onSuccess)
    bookSubject.next(book)
}

bookSubject.subscribe(updateRequestFunction)
bookSubject.subscribe(updateActionButtons)
bookSubject.subscribe(updateBookFormValues)

onSuccessSubject.subscribe(updateModal)
