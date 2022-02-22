const { BehaviorSubject, skipWhile } = rxjs
import * as doms from '/static/helpers/doms.js'
import * as editSongModal from '/static/web/songs/songs/js/modals/edit-song.js'
import * as deleteSongModal from '/static/web/songs/songs/js/modals/delete-song.js'

const search = $('#search-song')

const breadcrumbBook = $('#breadcrumb-book')
const bookName = $('#book-name')
const bookLang = $('#book-lang')
const buttonAddSong = $('#btn-add-song')

const songList = $('#song-list')

const placeholderBookName = $('#placeholder-book-name')
const placeholderSongList = $('#placeholder-song-list')
const containerSongList = $('#container-song-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

let book

const bookSubject = new BehaviorSubject().pipe(skipWhile(book => book === undefined))
const songsSubject = new BehaviorSubject().pipe(skipWhile(songs => songs === undefined))

buttonAddSong.click(() => {
    editSongModal.open(null, book, retrieveSongs)
})

const showLoader = () => {
    buttonAddSong.addClass('disabled')
    search.addClass('loading disabled')
}

const hideLoader = () => {
    buttonAddSong.removeClass('disabled')
    search.removeClass('loading disabled')
}

const displayPlaceholder = () => {
    viewError.hide()
    viewEmpty.hide()
    bookName.hide()
    containerSongList.hide()
    placeholderBookName.show()
    placeholderSongList.show()
}

const displayBookName = () => {
    placeholderBookName.hide()
    bookName.show()
}

const displaySongList = () => {
    placeholderSongList.hide()
    containerSongList.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderSongList.hide()
    viewError.show()
}

const displayEmptyView = () => {
    placeholderSongList.hide()
    viewEmpty.show()
}

const updateBookInfo = book => {
    bookName.text(book.name)
    bookLang.text(book.lang === 1 ? 'Simalungun' : 'Indonesia')
    displayBookName()
}

const updateBreadcrumb = book => {
    breadcrumbBook.text(book.name)
}

const createSongListItem = song => {
    const item = doms.createDOMFromJSON({
        tag: 'div',
        classList: ['item'],
        children: [
            {
                tag: 'div',
                classList: ['content'],
                children: [
                    {
                        tag: 'div',
                        classList: ['header'],
                        innerText: song.book.is_hymn_book ? `${song.number}${song.sub_number}. ${song.title}` : song.title,
                    },
                ],
            },
            {
                tag: 'div',
                classList: ['extra'],
                children: [
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'buttons'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'icon', 'button', 'btnEdit'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['pen', 'icon'],
                                    },
                                ],
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'red', 'icon', 'button', 'btnDelete'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['trash', 'icon'],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    })

    const extra = item.find('.extra')
    const buttonEdit = item.find('.btnEdit')
    const buttonDelete = item.find('.btnDelete')

    item.attr('id', `song-${song.id}`)

    item.hover(() => {
        if (song.book.is_hymn_book === false) extra.show()
    }, () => {
        extra.hide()
    })

    item.click(e => {
        if (buttonEdit[0].contains(e.target) || buttonDelete[0].contains(e.target))
            return false

        // open book-detail unless clicking the action buttons.
        // clicking on the extra content will still trigger the
        // click.
        window.location = `/songs/songs/${song.id}`
    })

    buttonEdit.click(() => {
        editSongModal.open(song, book, retrieveSongs)
    })

    buttonDelete.click(() => {
        deleteSongModal.open(song, retrieveSongs)
    })

    extra.hide()
    
    return item
}

const updateSongList = songs => {
    songList.empty()
    songList.append(...songs.map(createSongListItem))

    hideLoader()

    if (songs.length === 0) displayEmptyView()
    else displaySongList()
}

const joinSongBookNumber = song => {
    // by default, semantic-ui will search title and/or description fields.
    return {
        id: song.id,
        title: book.is_hymn_book ? `${song.number}${song.sub_number}. ${song.title}` : song.title
    }
}

const updateSearch = songs => {
    search.search({
        source: songs.map(joinSongBookNumber),
        fullTextSearch: true,
        minCharacters: 3,
        onSelect: (result, response) => {
            $(`#song-${result.id}`)[0].scrollIntoView()
        }
    })
}

const retrieveSongs = () => {
    showLoader()
    displayPlaceholder()

    Promise.all([axios.get(`/api/songs/books/${bookId}`), axios.get(`/api/songs/songs?book=${bookId}`)])
        .then(([{ data: book }, { data: songs }]) => {
            bookSubject.next(book)
            songsSubject.next(songs)
        })
        .catch(displayErrorView)
}

bookSubject.subscribe(value => book = value)
bookSubject.subscribe(updateBookInfo)
bookSubject.subscribe(updateBreadcrumb)

songsSubject.subscribe(updateSongList)
songsSubject.subscribe(updateSearch)

retrieveSongs()
