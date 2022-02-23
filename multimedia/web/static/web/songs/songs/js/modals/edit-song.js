const { BehaviorSubject, skipWhile } = rxjs

const modal = $('#modal-edit-song')
const modalHeader = $('#modal-edit-song-header')

const form = $('#form-edit-song')

const errorMessages = form.find('.ui.error.message')
const titleErrorMessage = form.find('#form-edit-song-error-message-title')
const nonFieldErrorMessage = form.find('#form-edit-song-error-message-non-field')

const buttonCreate = modal.find('#modal-edit-song-button-create')
const buttonSave = modal.find('#modal-edit-song-button-save')
const buttonCancel = modal.find('#modal-edit-song-button-cancel')

let requestFunction

const songSubject = new BehaviorSubject().pipe(skipWhile(song => song === undefined))
const bookSubject = new BehaviorSubject().pipe(skipWhile(book => book === undefined))
const onSuccessSubject = new BehaviorSubject().pipe(skipWhile(onSuccess => onSuccess === undefined))

form.form({
    fields: {
        title: {
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

    if (responseJSON.title !== undefined)
        titleErrorMessage.text(responseJSON.title.join('\n'))
    if (responseJSON.non_field_errors !== undefined)
        nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
}

const sendCreateRequest = (formData, onSuccess) => {
    $.ajax({
        url: '/api/songs/songs',
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
        url: `/api/songs/songs/${formData.id}`,
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
        const { id, bookId, title } = form.form('get values')

        const formData = {
            id: id,
            book_id: bookId,
            title: title.trim(),
            number: null,
            sub_number: '',
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

const updateSongFormValues = song => {
    if (song !== null) {
        form.form('set values', {
            id: song.id,
            title: song.title,
        })
    }

    hideLoader()
}

const updateSongFormBookIDValue = book => {
    form.form('set value', 'bookId', book.id)
}

const updateActionButtons = song => {
    if (song === null) {
        buttonSave.hide()
        buttonCreate.show()
    }
    else {
        buttonCreate.hide()
        buttonSave.show()
    }
}

const updateRequestFunction = song => {
    if (song === null) requestFunction = sendCreateRequest
    else requestFunction = sendEditRequest
}

const updateModalHeader = song => {
    modalHeader.text(song === null ? 'Create Song' : 'Edit Song')
}

export const open = (song, book, onSuccess) => {
    showLoader()
    modal.modal('show')
    songSubject.next(song)
    bookSubject.next(book)
    onSuccessSubject.next(onSuccess)
}

songSubject.subscribe(updateRequestFunction)
songSubject.subscribe(updateActionButtons)
songSubject.subscribe(updateSongFormValues)
songSubject.subscribe(updateModalHeader)

bookSubject.subscribe(updateSongFormBookIDValue)

onSuccessSubject.subscribe(updateModal)
