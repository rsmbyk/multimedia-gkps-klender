const BookmarkDetailModal = (deleteBookmarkItemModal) => {
    const modal = $('#modal-bookmark-detail').modal({
        closable: false,
        allowMultiple: true,
    })

    const open = (bookmarkId) => {
        const updateBookmarkInfo = (bookmark, items) => {
            const createBookmarkItem = (bookmarkItem, _) => {
                const item = createDOMFromJSON({
                    tag: 'div',
                    classList: ['item'],
                    children: [
                        {
                            tag: 'div',
                            classList: ['right', 'floated', 'content'],
                            children: [
                                {
                                    tag: 'div',
                                    classList: ['ui', 'tiny', 'basic', 'red', 'icon', 'button', 'btnDelete'],
                                    children: [
                                        {
                                            tag: 'i',
                                            classList: ['trash', 'icon'],
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            tag: 'div',
                            classList: ['content'],
                        },
                    ],
                })

                const buttonDelete = $(item).find('.btnDelete')
                buttonDelete.click(() => {
                    deleteBookmarkItemModal.open(
                        bookmark,
                        bookmarkItem,
                        bookmarkItem.song_info.book_number,
                        () => retrieveBookmarkItems(bookmark),
                        console.log,
                    )
                })

                const content = $(item).find('.content:not(.right.floated)')
                content.text(`${bookmarkItem.song_info.book_number} : ${bookmarkItem.verse}`)

                return item
            }

            $('#modal-bookmark-detail-header').text(bookmark.name)
            $('#modal-bookmark-detail-subheader').text(bookmark.date)

            const bookmarkItemList = $('#modal-bookmark-detail-item-list')
            bookmarkItemList.empty()
            bookmarkItemList.append(...items.map(createBookmarkItem))

            modal.modal('show')
        }

        const retrieveBookmarkItems = (bookmark) => {
            axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}&omit=verse_info`)
                .then(result => updateBookmarkInfo(bookmark, result.data))
        }

        axios.get(`/api/bookmarks/songs/bookmarks/${bookmarkId}`)
            .then((result) => retrieveBookmarkItems(result.data))
    }

    return {
        open,
    }
}
