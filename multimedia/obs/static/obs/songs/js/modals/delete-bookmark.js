const DeleteBookmarkModal = () => {
    const modal = $('#modal-delete-bookmark')

    const sendDeleteRequest = (bookmark, onSuccess, onError) => {
        $.ajax({
            url: `/api/bookmarks/songs/bookmarks/${bookmark.id}`,
            method: 'PATCH',
            data: {
                is_active: false,
            },
            success: () => {
                onSuccess()
                modal.modal('hide')
                $('body').toast({
                    class: 'success centered',
                    message: 'Bookmark deleted successfully',
                    position: 'top attached',
                })
            },
            error: (a) => {
                console.log(a)
                onError()
                $('body').toast({
                    class: 'error centered',
                    message: 'Delete failed',
                    position: 'top attached',
                })
            },
        })
    }

    const open = (bookmark, onSuccess, onError) => {
        modal.modal({
            closable: false,
            onApprove : () => {
                sendDeleteRequest(bookmark, onSuccess, onError)
                return false
            },
        })

        modal.find('.content .bookmarkName').text(bookmark.name)

        const date = new Date(bookmark.date)
        modal.find('.content .bookmarkDate').text(date.toLocaleString('en-us', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        }))
        modal.modal('show')
    }

    return {
        open,
    }
}
