const { merge, map, scan } = rxjs

const SongDetailModal = (bookmarkManager) => {
    const songDetailModal = $('#modal-song-detail')

    let activeBookmark
    bookmarkManager.activeBookmark.subscribe(value => activeBookmark = value)

    let activeBookmarkItems
    bookmarkManager.activeBookmarkItems.subscribe(value => activeBookmarkItems = value)

    let savedVerseSelection = null

    const verseSelection = new BehaviorSubject([])
        .pipe(
            scan((selection, next) => {
                if (next.constructor === Array) return next
                if (next === 0) return []
                if (next > 0) return selection.concat(next)
                return selection.filter(x => x !== -next)
            }),
            map(selection => selection.sort())
        )

    let bookmarkedVerses
    verseSelection.subscribe(value => bookmarkedVerses = value)

    let mBook = null
    let mSong = null
    let mVerses = null
    let bookmarkItemId = null

    const header = $('#modal-song-detail-header')
    const subheader = $('#modal-song-detail-subheader')
    const verseList = $('#modal-song-detail-verse-list')
    const buttonSave = $('#modal-song-detail-btn-save')
    const buttonDelete = $('#modal-song-detail-btn-delete')
    const buttonDisplay = $('#modal-song-detail-btn-display')

    const actionToggleButton = new ManualToggleButton(buttonSave, buttonDelete)

    const evaluateActionButtonState = () => {
        if (activeBookmark === null) {
            actionToggleButton.setInactive()
            actionToggleButton.hide()
        }
        else if (bookmarkedVerses.equals(savedVerseSelection)) {
            actionToggleButton.setActive()
            actionToggleButton.hide()
        }
        else if (bookmarkedVerses.length === 0) {
            actionToggleButton.setInactive()
            actionToggleButton.show()
        }
        else {
            actionToggleButton.setActive()
            actionToggleButton.show()
        }
    }

    verseSelection.subscribe(evaluateActionButtonState)

    buttonSave.click(() => {
        if (savedVerseSelection.length === 0)
            sendCreateBookmarkItemRequest()
        else
            sendEditBookmarkItemRequest()
    })

    buttonDelete.click(() => {
        sendDeleteBookmarkItemRequest()
    })

    buttonDisplay.click(() => {
        let book_number
        if (mBook.is_hymn_book) book_number = `${mBook.short_name} ${mSong.number}`
        else book_number = null

        bookmarkManager.deactivate()
        bookmarkManager.activateBookmarkItems([{
            song_info: {
                book_number: book_number,
                title: mSong.title,
            },
            verse_info: mVerses,
        }])

        songDetailModal.modal('hide')
    })

    const sendCreateBookmarkItemRequest = () => {
        $.ajax({
            url: '/api/bookmarks/songs/items',
            method: 'POST',
            data: {
                bookmark: activeBookmark,
                song: mSong.id,
                verse: JSON.stringify(bookmarkedVerses).slice(1, -1),
            },
            success: () => {
                bookmarkManager.activateBookmark(activeBookmark)
                songDetailModal.modal('hide')
            },
            error: () => {

            },
        })
    }

    const sendEditBookmarkItemRequest = () => {
        $.ajax({
            url: `/api/bookmarks/songs/items/${bookmarkItemId}`,
            method: 'PATCH',
            data: {
                verse: JSON.stringify(bookmarkedVerses).slice(1, -1),
            },
            success: () => {
                bookmarkManager.activateBookmark(activeBookmark)
                songDetailModal.modal('hide')
            },
            error: console.log,
        })
    }

    const sendDeleteBookmarkItemRequest = () => {
        $.ajax({
            url: `/api/bookmarks/songs/items/${bookmarkItemId}`,
            method: 'DELETE',
            success: () => {
                bookmarkManager.activateBookmark(activeBookmark)
                songDetailModal.modal('hide')
            },
            error: () => {

            },
        })
    }

    const openSong = (songId) => {
        const updateSongInfo = (song, book, verses) => {
            const createVerseItem = (verse) => {
                const item = createDOMFromJSON({
                    tag: 'div',
                    classList: ['item'],
                    children: [
                        {
                            tag: 'div',
                            classList: ['content'],
                            children: [
                                {
                                    tag: 'div',
                                    classList: ['description'],
                                    innerText: verse.lyric,
                                },
                                {
                                    tag: 'div',
                                    classList: ['extra'],
                                    children: [
                                        {
                                            tag: 'div',
                                            classList: ['ui', 'right', 'floated', 'tiny', 'basic', 'button', 'btnAddToBookmark'],
                                            children: [
                                                {
                                                    tag: 'i',
                                                    classList: ['bookmark', 'outline', 'icon'],
                                                },
                                                {
                                                    tag: 'span',
                                                    classList: ['text'],
                                                    innerText: 'Add to Bookmark',
                                                }
                                            ]
                                        },
                                        {
                                            tag: 'div',
                                            classList: ['ui', 'right', 'floated', 'tiny', 'teal', 'button', 'btnBookmarked'],
                                            children: [
                                                {
                                                    tag: 'i',
                                                    classList: ['bookmark', 'icon'],
                                                },
                                                {
                                                    tag: 'span',
                                                    classList: ['text'],
                                                    innerText: 'Bookmarked',
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                })

                const buttonAddToBookmark = $(item).find('.btnAddToBookmark')
                const buttonBookmarked = $(item).find('.btnBookmarked')

                buttonAddToBookmark.click(() => verseSelection.next(verse.number))
                buttonBookmarked.click(() => verseSelection.next(-verse.number))

                const bookmarkToggleButton = new ToggleButton(buttonBookmarked, buttonAddToBookmark)

                if (savedVerseSelection.includes(verse.number)) {
                    bookmarkToggleButton.setActive()
                    bookmarkToggleButton.show()
                }
                else {
                    bookmarkToggleButton.setInactive()
                    bookmarkToggleButton.hide()
                }

                $(item).hover(() => {
                    if (activeBookmark !== null) bookmarkToggleButton.show()
                }, () => {
                    if (!bookmarkToggleButton.isActive) bookmarkToggleButton.hide()
                })

                return item
            }

            bookmarkItemId = null
            savedVerseSelection = []
            verseSelection.next(0)

            if (activeBookmark !== null && activeBookmarkItems !== null) {
                const songItem = activeBookmarkItems.filter(item => item.song === song.id)
                if (songItem.length === 1) {
                    bookmarkItemId = songItem[0].id
                    savedVerseSelection = songItem[0].verse_info.map(v => v.number)
                    verseSelection.next(savedVerseSelection)
                }
            }

            mSong = song
            mBook = book
            mVerses = verses

            header.text(song.title)
            subheader.text(book.name)

            verseList.empty()
            verses.forEach((verse) => verseList.append(createVerseItem(verse)))

            if (activeBookmark === null) buttonSave.css('visibility', 'hidden')
            else buttonSave.css('visibility', 'visible')

            songDetailModal.modal('show')
        }

        const retrieveSongInfo = (song) => {
            const promises = [
                axios.get(`/api/songs/books/${song.data.book}`),
                axios.get(`/api/songs/verses?song=${song.data.id}`),
            ]

            Promise.all(promises)
                .then((results) => updateSongInfo(song.data, results[0].data, results[1].data))
        }

        axios.get(`/api/songs/songs/${songId}`)
            .then(retrieveSongInfo)
    }

    return {
        openSong,
    }
}
