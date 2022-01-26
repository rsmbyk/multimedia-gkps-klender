const BookmarksTab = () => {
    const createBookmarkItem = (bookmark, _) => {
        const date = new Date(bookmark.date)
        const item = createDOMFromJSON({
            tag: 'div',
            classList: ['middle', 'aligned', 'item'],
            children: [
                {
                    tag: 'div',
                    classList: ['right', 'floated', 'middle', 'aligned', 'content'],
                    children: [
                        {
                            tag: 'div',
                            classList: ['ui', 'inverted', 'basic', 'mini', 'buttons', 'btnActivate'],
                            children: [
                                {
                                    tag: 'div',
                                    classList: ['ui', 'button'],
                                    innerText: 'Activate',
                                },
                                {
                                    tag: 'div',
                                    classList: ['ui', 'floating', 'dropdown', 'icon', 'button'],
                                    children: [
                                        {
                                            tag: 'i',
                                            classList: ['dropdown', 'icon'],
                                        },
                                        {
                                            tag: 'div',
                                            classList: ['menu'],
                                            children: [
                                                {
                                                    tag: 'div',
                                                    classList: ['item'],
                                                    children: [
                                                        {
                                                            tag: 'i',
                                                            classList: ['edit', 'icon'],
                                                            innerText: 'Edit',
                                                        },
                                                    ],
                                                },
                                                {
                                                    tag: 'div',
                                                    classList: ['item'],
                                                    children: [
                                                        {
                                                            tag: 'i',
                                                            classList: ['delete', 'icon'],
                                                            innerText: 'Delete',
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    tag: 'i',
                    classList: ['inverted', 'small', 'check', 'circle', 'middle', 'aligned', 'green', 'icon', 'icoCheck'],
                },
                {
                    tag: 'div',
                    classList: ['content'],
                    children: [
                        {
                            tag: 'div',
                            classList: ['header'],
                            innerText: bookmark.name,
                        },
                        {
                            tag: 'div',
                            classList: ['description'],
                            innerText: `${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`,
                        },
                    ],
                },
            ],
        })

        $(item).hover(() => {
            if (bookmark.id === 1) $(item).find('.icoCheck').show()
            $(item).find('.btnActivate').show()
        }, () => {
            if (bookmark.id !== 1) $(item).find('.icoCheck').hide()
            $(item).find('.btnActivate').hide()
        })

        if (bookmark.id !== 1) $(item).find('.icoCheck').hide()
        $(item).find('.btnActivate').hide()

        return item
    }

    const updateBookmarkList = (bookmarks) => {
        const bookmarkList = $('#bookmark-list')
        bookmarkList.empty()
        bookmarkList.append(...bookmarks.map(createBookmarkItem))
    }

    const retrieveBookmarks = (date) => {
        axios.get(`/api/bookmarks/songs/bookmarks?month=${date.getMonth()+1}&year=${date.getFullYear()}`)
            .then((response) => updateBookmarkList(response.data))
            .catch(console.log)

        $('#button-filter-text').text(date.toLocaleString('en-us', {month:'short', year:'numeric'}))
    }

    const init = () => {
        $('#button-create-bookmark').click(() => {
            $('#modal-create-bookmark').modal('show')
        })

        const today = new Date(Date.now())
        retrieveBookmarks(today)
    }

    return {
        init
    }
}
