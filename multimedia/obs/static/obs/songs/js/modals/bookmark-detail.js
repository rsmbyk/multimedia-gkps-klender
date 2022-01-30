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

                const content = $(item).find('.content:not(.right.floated)')
                axios.get(`/api/songs/songs/${bookmarkItem.song}`)
                    .then((songResult) => {
                        axios.get(`/api/songs/books/${songResult.data.book}`)
                        .then((bookResult) => {
                            let contentText
                            if (bookResult.data.is_hymn_book)
                                contentText = `${bookResult.data.short_name} ${songResult.data.number}${songResult.data.sub_number} : ${bookmarkItem.verse}`
                            else
                                contentText = `${songResult.data.title}`

                            content.text(contentText)

                            buttonDelete.click(() => {
                                deleteBookmarkItemModal.open(
                                    bookmark,
                                    bookmarkItem,
                                    contentText,
                                    () => retrieveBookmarkItems(bookmark),
                                    console.log,
                                )
                            })
                        })
                    })

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
            axios.get(`/api/bookmarks/songs/items?bookmark=${bookmark.id}`)
                .then(result => updateBookmarkInfo(bookmark, result.data))
        }

        axios.get(`/api/bookmarks/songs/bookmarks/${bookmarkId}`)
            .then((result) => retrieveBookmarkItems(result.data))
    }

    return {
        open,
    }
}
