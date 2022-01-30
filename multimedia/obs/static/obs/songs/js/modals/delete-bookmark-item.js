const DeleteBookmarkItemModal = () => {
    const modal = $('#modal-delete-bookmark-item')

    const sendDeleteRequest = (bookmarkItem, onSuccess, onError) => {
        $.ajax({
            url: `/api/bookmarks/songs/items/${bookmarkItem.id}`,
            method: 'DELETE',
            success: (response) => {
                onSuccess(response)
                modal.modal('hide')
                $('body').toast({
                    class: 'success centered',
                    message: 'Item deleted successfully',
                    position: 'top attached',
                })
            },
            error: (error) => {
                onError(error)
                $('body').toast({
                    class: 'error centered',
                    message: 'Delete failed',
                    position: 'top attached',
                })
            },
        })
    }

    const open = (bookmark, bookmarkItem, bookmarkItemDisplayName, onSuccess, onError) => {
        modal.modal({
            allowMultiple: true,
            closable: false,
            centered: true,
            onApprove : () => {
                sendDeleteRequest(bookmarkItem, onSuccess, onError)
                return false
            },
        })

        modal.find('.content .bookmarkItemName').text(bookmarkItemDisplayName)

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
