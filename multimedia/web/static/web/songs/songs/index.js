const { BehaviorSubject, skipWhile } = rxjs

import * as doms from '/static/helpers/doms.js'

import * as editSongModal from './modals/edit-song.js'
import * as deleteSongModal from './modals/delete-song.js'

const songList = $('#song-list')

const search = $('#search-song')

const bookName = $('#book-name')
const bookLang = $('#book-lang')

const buttonAddSong = $('#btn-add-song')

const breadcrumb = $('#breadcrumb')
const breadcrumbBook = $('#breadcrumb-book')

const placeholderBookInfo = $('#placeholder-book-info')
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
    buttonAddSong.addClass('loading disabled')
    search.addClass('loading disabled')
}

const hideLoader = () => {
    buttonAddSong.removeClass('loading disabled')
    search.removeClass('loading disabled')
}

const displayBookInfoPlaceholder = () => {
    breadcrumb.hide()
    bookName.hide()
    bookLang.hide()
    placeholderBookInfo.show()
}

const displayPlaceholder = () => {
    containerSongList.hide()
    viewError.hide()
    viewEmpty.hide()
    placeholderSongList.show()
}

const displayBookInfo = () => {
    placeholderBookInfo.hide()
    bookName.show()
    bookLang.show()
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

const updateBreadcrumb = book => {
    breadcrumbBook.text(book.name)

    breadcrumb.show()
}

const updateBookInfo = book => {
    bookName.text(book.name)
    bookLang.text(book.lang === 1 ? 'Simalungun' : 'Indonesia')

    displayBookInfo()
}

const updateAddSongButton = book => {
    if (book.is_hymn_book) buttonAddSong.hide()
    else buttonAddSong.show()
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
        onSelect: result => {
            $(`#song-${result.id}`)[0].scrollIntoView()
        }
    })
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

const retrieveSongs = () => {
    showLoader()
    displayPlaceholder()

    axios.get(`/api/songs/songs?book=${bookId}`)
        .then(({ data: songs }) => songsSubject.next(songs))
        .catch(displayErrorView)
}

const retrieveBook = () => {
    showLoader()
    displayBookInfoPlaceholder()
    displayPlaceholder()

    axios.get(`/api/songs/books/${bookId}`)
        .then(({ data: book }) => {
            bookSubject.next(book)
            retrieveSongs()
        })
        .catch(displayErrorView)
}

bookSubject.subscribe(value => book = value)
bookSubject.subscribe(updateBreadcrumb)
bookSubject.subscribe(updateBookInfo)
bookSubject.subscribe(updateAddSongButton)

songsSubject.subscribe(updateSearch)
songsSubject.subscribe(updateSongList)

retrieveBook()
