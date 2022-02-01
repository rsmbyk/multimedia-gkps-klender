const BookmarksTab = (bookmarkManager, createBookmarkModal, deleteBookmarkModal, bookmarkDetailModal) => {
    const currentDate = new Date()
    let activeBookmark = undefined

    bookmarkManager.activeBookmark.subscribe(value => {
        activeBookmark = value
    })

    const filterDateButton = $('#button-filter-calendar')
    filterDateButton.calendar({
        type: 'month',
        today: true,
        onChange: (date) => {
            currentDate.setTime(date.getTime())
            refresh()
        },
    })

    const createBookmarkItem = (bookmark, _) => {
        const date = new Date(bookmark.date)
        const item = createDOMFromJSON({
            tag: 'div',
            classList: ['middle', 'aligned', 'item'],
            children: [
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
                {
                    tag: 'div',
                    classList: ['extra'],
                    children: [
                        {
                            tag: 'div',
                            classList: ['ui', 'right', 'floated', 'tiny', 'buttons'],
                            children: [
                                {
                                    tag: 'div',
                                    classList: ['ui', 'inverted', 'basic', 'button', 'btnActivate'],
                                    innerText: 'Activate'
                                },
                                {
                                    tag: 'div',
                                    classList: ['ui', 'inverted', 'icon', 'button', 'btnEdit'],
                                    children: [
                                        {
                                            tag: 'i',
                                            classList: ['pen', 'icon'],
                                        },
                                    ]
                                },
                                {
                                    tag: 'div',
                                    classList: ['ui', 'inverted', 'red', 'icon', 'button', 'btnDelete'],
                                    children: [
                                        {
                                            tag: 'i',
                                            classList: ['trash', 'icon'],
                                        },
                                    ]
                                },
                            ]
                        },
                    ],
                },
            ],
        })

        const iconCheck = $(item).find('.icoCheck')
        const extraButtons = $(item).find('.extra > .ui.buttons')
        const buttonActivate = extraButtons.find('.btnActivate')
        const buttonEdit = extraButtons.find('.btnEdit')
        const buttonDelete = extraButtons.find('.btnDelete')

        $(item).hover(() => {
            if (bookmark.id === activeBookmark) iconCheck.show()
            extraButtons.show()
        }, () => {
            if (bookmark.id !== activeBookmark) iconCheck.hide()
            extraButtons.hide()
        })

        if (bookmark.id === activeBookmark) buttonActivate.hide()
        else iconCheck.hide()
        extraButtons.hide()

        buttonActivate.click(() => {
            $('#bookmark-list .btnActivate').show()
            buttonActivate.hide()
            $('#bookmark-list .icoCheck').hide()
            iconCheck.show()
            bookmarkManager.activateBookmark(bookmark)
        })

        buttonEdit.click(() => {
            bookmarkDetailModal.open(bookmark.id)
        })

        buttonDelete.click(() => {
            deleteBookmarkModal.open(bookmark, refresh, () => console.log('error'))
            bookmarkManager.deactivate()
        })

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

    const refresh = () => {
        retrieveBookmarks(currentDate)
    }

    const init = () => {
        $('#button-create-bookmark').click(() => {
            createBookmarkModal.open()
        })

        refresh()
    }

    return {
        init,
        refresh,
    }
}
