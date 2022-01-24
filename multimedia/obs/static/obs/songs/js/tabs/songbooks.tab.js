const SongBooksTab = () => {
    const songbooksStateValue = new DropdownStateValue(
        'SONGBOOKS_STATE_VALUE',
        '#dropdown-songbooks',
        LOCAL_STORAGE_KEY_SONGBOOK,
    )

    const songsStateValue = new SearchDropdownStateValue(
        'SONGS_STATE_VALUE',
        '#dropdown-songs',
        '#submenu-songs',
        LOCAL_STORAGE_KEY_SONG,
    )

    const createMenuSongItem = (song, _) => {
        const item = document.createElement('div')
        item.classList.add('item')
        item.setAttribute('data-value', song.id)
        item.innerText = song.title
        return item
    }

    const repopulateSongsDropdown = (songs) => {
        const items = songs.data
            .map(createMenuSongItem)

        songsStateValue.init(items, console.log, false)

        $('#button-open-song').removeClass('disabled')
    }

    const loadSongsDropdown = (bookId) => {
        axios.get(`/api/songs/songs?book=${bookId}`)
             .then(repopulateSongsDropdown)
    }

    const loadBooks = (songDetailModal) => {
        songbooksStateValue.init(null, loadSongsDropdown, true)

        $('#button-open-song').click(() => {
            songDetailModal.openSong(songsStateValue.selectedValue)
        })
    }

    return {
        loadBooks
    }
}
