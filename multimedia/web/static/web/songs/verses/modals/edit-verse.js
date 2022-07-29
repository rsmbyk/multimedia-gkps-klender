const { BehaviorSubject, skipWhile } = rxjs

import * as PreviewManager from '../PreviewManager.js'

const modal = $('#modal-edit-verse')
const modalHeader = $('#modal-edit-verse-header')

const form = $('#form-edit-verse')

const errorMessages = form.find('.ui.error.message')
const numberErrorMessage = form.find('#form-edit-verse-error-message-number')
const lyricErrorMessage = form.find('#form-edit-verse-error-message-lyric')
const nonFieldErrorMessage = form.find('#form-edit-verse-error-message-non-field')

const buttonCreate = modal.find('#modal-edit-verse-button-create')
const buttonSave = modal.find('#modal-edit-verse-button-save')
const buttonCancel = modal.find('#modal-edit-verse-button-cancel')

let requestFunction

const songSubject = new BehaviorSubject().pipe(skipWhile(song => song === undefined))
const verseSubject = new BehaviorSubject().pipe(skipWhile(verse => verse === undefined))
const verseNumberSubject = new BehaviorSubject().pipe(skipWhile(verseNumber => verseNumber === undefined))
const onSuccessSubject = new BehaviorSubject().pipe(skipWhile(onSuccess => onSuccess === undefined))

form.form({
    fields: {
        lyric: {
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
        PreviewManager.openModalPreview(values.lyric)
    },
    onInvalid: function() {
        const values = form.form('get values')
        PreviewManager.openModalPreview(values.lyric)
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

    if (responseJSON.number !== undefined)
        numberErrorMessage.text(responseJSON.number.join('\n'))
    if (responseJSON.lyric !== undefined)
        lyricErrorMessage.text(responseJSON.lyric.join('\n'))
    if (responseJSON.non_field_errors !== undefined)
        nonFieldErrorMessage.text(responseJSON.non_field_errors.join('\n'))
}

const sendCreateRequest = (formData, onSuccess) => {
    $.ajax({
        url: '/api/songs/verses',
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
        url: `/api/songs/verses/${formData.id}`,
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
        const { id, songId, number, lyric } = form.form('get values')

        const formData = {
            id: id,
            song: songId,
            number: number,
            lyric: lyric,
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

function updateModalPreview(verse) {
    PreviewManager.openModalPreview(verse?.lyric ?? '', true)
}

const updateFormValues = verse => {
    if (verse !== null) {
        form.form('set values', {
            id: verse.id,
            lyric: verse.lyric,
        })
    }

    hideLoader()
}

const updateFormSongIDValue = song => {
    form.form('set value', 'songId', song.id)
}

const updateFormVerseNumberValue = verseNumber => {
    form.form('set value', 'number', verseNumber)
}

const updateActionButtons = verse => {
    if (verse === null) {
        buttonSave.hide()
        buttonCreate.show()
    }
    else {
        buttonCreate.hide()
        buttonSave.show()
    }
}

const updateRequestFunction = verse => {
    if (verse === null) requestFunction = sendCreateRequest
    else requestFunction = sendEditRequest
}

const updateModalHeader = verse => {
    modalHeader.text(verse === null ? 'Create Lyric' : 'Edit Lyric')
}

export const open = (verse, song, verseNumber, onSuccess) => {
    showLoader()
    modal.modal('show')
    songSubject.next(song)
    verseSubject.next(verse)
    verseNumberSubject.next(verseNumber)
    onSuccessSubject.next(onSuccess)
}

verseSubject.subscribe(updateRequestFunction)
verseSubject.subscribe(updateActionButtons)
verseSubject.subscribe(updateFormValues)
verseSubject.subscribe(updateModalHeader)
verseSubject.subscribe(updateModalPreview)

songSubject.subscribe(updateFormSongIDValue)

verseNumberSubject.subscribe(updateFormVerseNumberValue)

onSuccessSubject.subscribe(updateModal)
