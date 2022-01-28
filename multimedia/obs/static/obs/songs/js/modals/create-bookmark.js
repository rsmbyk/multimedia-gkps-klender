const CreateBookmarkModal = () => {
    const modalCreateBookmark = $('#modal-create-bookmark')
    const formCreateBookmark = $('#form-create-bookmark')

    const onCreateBookmarkSuccessful = (response) => {
        modalCreateBookmark.modal('hide')
    }

    const submitForm = (onBookmarkCreatedCallback) => {
        formCreateBookmark.removeClass('error')
        formCreateBookmark.find('.ui.error.message').empty()

        if (formCreateBookmark.form('is valid')) {
            const values = formCreateBookmark.form('get values')

            const val = {
                name: values.name.trim(),
                date: `${values.date.getFullYear()}-${values.date.getMonth()+1}-${values.date.getDate()}`,
            }

            $.post('/api/bookmarks/songs/bookmarks', val, (response) => {
                onBookmarkCreatedCallback()
                onCreateBookmarkSuccessful(response)
            }, 'json')
                .fail((response) => {
                    formCreateBookmark.addClass('error')
                    formCreateBookmark.find('.ui.error.message').text(JSON.stringify(response.responseJSON))
                })
        }
        else
            formCreateBookmark.form('validate form')
    }

    const open = () => {
        modalCreateBookmark.modal('show')
    }

    const init = (onBookmarkCreatedCallback) => {
        modalCreateBookmark.modal({
            closable: false,
            onHide: function() {
                formCreateBookmark.form('clear')
            },
            onApprove : function() {
                submitForm(onBookmarkCreatedCallback)
                return false
            },
        })

        const today = new Date(Date.now())

        formCreateBookmark.find('.ui.calendar').calendar({
            type: 'date',
            selectAdjacentDays: true,
            firstDayOfWeek: 1,
            disabledDaysOfWeek: [1, 2, 3, 4, 5],
            today: true,
            eventDates: [
                {
                    date: new Date(today.setDate(today.getDate() + ((7 - today.getDay()) % 7))),
                },
            ],
            popupOptions: {
                observeChanges: false,
            },
        })

        formCreateBookmark.form({
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
                    ]
                },
                date: 'empty',
            },
            inline: true,
            on: 'blur',
        })
    }
    
    return {
        init,
        open,
    }
}
