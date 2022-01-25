const SongDetailModal = () => {
    const songDetailModal = $('#modal-song-detail')
    songDetailModal.modal('setting', 'closable', false)

    const openSong = (songId) => {
        const updateSongInfo = (song, book, verses) => {
            const createButton = (text, icon, color, value) => {
                const button = document.createElement('button')
                button.classList.add('ui', color, 'tiny', 'button')
                button.setAttribute('value', value)

                const buttonIcon = document.createElement('i')
                buttonIcon.classList.add(...icon, 'icon')

                const buttonText = document.createElement('span')
                buttonText.classList.add('text')
                buttonText.innerText = text

                button.append(buttonIcon, buttonText)
                return button
            }

            const createVerseItem = (verse) => {
                const item = document.createElement('div')
                item.classList.add('item')

                const content = document.createElement('div')
                content.classList.add('content')
                item.append(content)

                const description = document.createElement('div')
                description.classList.add('description')
                description.innerText = verse.lyric
                content.append(description)

                const extra = document.createElement('div')
                extra.classList.add('extra')
                content.append(extra)

                const btnBookmarkInactive = createButton('Bookmark', ['bookmark', 'outline'], 'basic', verse.id)
                const btnBookmarkActive = createButton('Bookmarked', ['bookmark'], 'teal', verse.id)
                const bookmarkToggleButton = new ToggleButton(btnBookmarkActive, btnBookmarkInactive)
                bookmarkToggleButton.hide()

                const btnDisplay = createButton('Display', ['desktop'], 'primary', verse.id)
                btnDisplay.classList.add('right', 'floated')
                $(btnDisplay).hide()

                extra.append(btnBookmarkInactive, btnBookmarkActive, btnDisplay)

                $(item).hover(() => {
                    bookmarkToggleButton.show()
                    $(btnDisplay).show()
                }, () => {
                    if (!bookmarkToggleButton.isActive) bookmarkToggleButton.hide()
                    $(btnDisplay).hide()
                })

                return item
            }

            $('#modal-song-detail-header').text(song.title)
            $('#modal-song-detail-subheader').text(book.name)

            const verseList = $('#modal-song-detail-verse-list')
            verseList.empty()
            verses.forEach((verse) => verseList.append(createVerseItem(verse)))

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
        openSong
    }
}
