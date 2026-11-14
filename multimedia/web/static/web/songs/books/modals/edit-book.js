const { BehaviorSubject, skipWhile } = rxjs

const modal = $('#modal-edit-book')
const modalHeader = $('#modal-edit-book-header')

const form = $('#form-edit-book')

const errorMessages = form.find('.ui.error.message')
const nameErrorMessage = form.find('#form-edit-book-error-message-name')
const nonFieldErrorMessage = form.find('#form-edit-book-error-message-non-field')

const buttonCreate = modal.find('#modal-edit-book-button-create')
const buttonSave = modal.find('#modal-edit-book-button-save')
const buttonCancel = modal.find('#modal-edit-book-button-cancel')

let requestFunction

const bookSubject = new BehaviorSubject().pipe(skipWhile(book => book === undefined))
const onSuccessSubject = new BehaviorSubject().pipe(skipWhile(onSuccess => onSuccess === undefined))

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
                    type: 'regExp[/^[a-z0-9 _\'\"\/\.\?\,\(\)\&\+\:\!\*\-]+$/i]',
                    prompt: '{name} can contain alphanumeric, spaces and these symbols only: , . / ? : \' \" ! & * ( ) - _ +',
                },
            ],
        },
    },
    inline: true,
    on: 'change',
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
    if (responseJSON.non_field_errors !== undefined)
        nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
}

const sendCreateRequest = (formData, onSuccess) => {
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
            updateFormErrorMessages(responseJSON)
        },
        complete: () => {
            hideLoader()
        },
    })
}

const sendEditRequest = (formData, onSuccess) => {
    $.ajax({
        url: `/api/songs/books/${formData.id}`,
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
        const { id, name } = form.form('get values')

        const formData = {
            id: id,
            name: name.trim(),
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

const updateBookFormValues = book => {
    if (book !== null) {
        form.form('set values', {
            id: book.id,
            name: book.name,
        })
    }

    hideLoader()
}

const updateActionButtons = book => {
    if (book === null) {
        buttonSave.hide()
        buttonCreate.show()
    }
    else {
        buttonCreate.hide()
        buttonSave.show()
    }
}

const updateModalHeader = book => {
    modalHeader.text(book === null ? 'Create Book' : 'Edit Book')
}

const updateRequestFunction = book => {
    if (book === null) requestFunction = sendCreateRequest
    else requestFunction = sendEditRequest
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
bookSubject.subscribe(updateModalHeader)

onSuccessSubject.subscribe(updateModal)
