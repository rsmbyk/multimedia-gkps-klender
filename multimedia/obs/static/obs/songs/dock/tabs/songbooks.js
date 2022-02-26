const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'
import { DropdownStateValue } from '/static/helpers/state-value.js'
import * as toasts from '/static/helpers/toasts.js'

import * as songDetailModal from '../modals/song-detail.js'

const LOCAL_STORAGE_KEY_DROPDOWN_BOOKS = 'OBS_SONGS_DOCK_SONGBOOKS_DROPDOWN_BOOKS'
const LOCAL_STORAGE_KEY_DROPDOWN_SONGS = 'OBS_SONGS_DOCK_SONGBOOKS_DROPDOWN_SONGS'

const dropdownBooks = $('#songbooks-dropdown-books')
const dropdownSongs = $('#songbooks-dropdown-songs')

const buttonOpenSong = $('#songbooks-button-open-song')

const booksSubject = new BehaviorSubject()
const songsSubject = new BehaviorSubject()
const selectedBookIdSubject = new BehaviorSubject().pipe(distinctUntilChanged())
const selectedSongIdSubject = new BehaviorSubject()

const booksStateValue = new DropdownStateValue(LOCAL_STORAGE_KEY_DROPDOWN_BOOKS, dropdownBooks)
const songsStateValue = new DropdownStateValue(LOCAL_STORAGE_KEY_DROPDOWN_SONGS, dropdownSongs)

dropdownBooks
    .dropdown('setting', 'fullTextSearch', true)
    .dropdown('setting', 'match', 'text')
    .dropdown('setting', 'forceSelection', false)

dropdownSongs
    .dropdown('setting', 'fullTextSearch', true)
    .dropdown('setting', 'match', 'text')
    .dropdown('setting', 'forceSelection', false)

buttonOpenSong.click(() => {
    songDetailModal.open(songsStateValue.currentValue)
})

const showBooksLoader = () => {
    dropdownBooks
        .addClass('loading disabled')
        .dropdown('set text', 'Loading')
    dropdownSongs.addClass('disabled').removeClass('loading')
    buttonOpenSong.addClass('disabled')
}

const showSongsLoader = () => {
    dropdownSongs
        .addClass('loading disabled')
        .dropdown('set text', 'Loading')
    dropdownBooks.addClass('disabled').removeClass('loading')
    buttonOpenSong.addClass('disabled')
}

const hideLoader = () => {
    dropdownBooks.removeClass('loading disabled')
    dropdownSongs.removeClass('loading disabled')
}

const displayBooksErrorView = () => {
    dropdownBooks
        .removeClass('loading disabled')
        .dropdown('set text', 'Error')
}

const displaySongsErrorView = () => {
    dropdownBooks.removeClass('disabled')
    dropdownSongs
        .removeClass('loading')
        .dropdown('set text', 'Error')
}

const activateOpenSongButton = () => {
    buttonOpenSong.removeClass('disabled')
}

const createSongsDropdownMenuItem = song => {
    return {
        value: song.id,
        name: song.book.is_hymn_book ? `${song.number}${song.sub_number}. ${song.title}` : song.title,
    }
}

const updateSongsDropdown = songs => {
    dropdownSongs.dropdown('change values', songs.map(createSongsDropdownMenuItem))
    songsStateValue.init(songId => selectedSongIdSubject.next(songId), false)

    hideLoader()

    if (songs.length === 0) {
        dropdownSongs
            .dropdown('set text', 'No songs')
            .addClass('disabled')
        buttonOpenSong.addClass('disabled')
    }
}

const retrieveSongs = selectedBookId => {
    showSongsLoader()

    axios.get(`/api/songs/songs?book=${selectedBookId}`)
         .then(({ data: songs }) => songsSubject.next(songs))
         .catch(e => {
             console.log(e)
             toasts.error('Failed to load song list', 'top center')
             displaySongsErrorView()
         })
}

const createBooksDropdownMenuItem = book => {
    return {
        value: book.id,
        name: book.name,
        icon: book.lang === 2 ? 'id' : 'language',
        iconClass: book.lang === 2 ? 'flag' : 'icon',
    }
}

const updateBooksDropdown = books => {
    dropdownBooks.dropdown('change values', books.map(createBooksDropdownMenuItem))
    booksStateValue.init(bookId => selectedBookIdSubject.next(bookId), true)
}

const retrieveBooks = () => {
    showBooksLoader()

    axios.get('/api/songs/books')
         .then(({ data: books }) => booksSubject.next(books))
         .catch(e => {
             console.log(e)
             toasts.error('Failed to load book list', 'top center')
             displayBooksErrorView()
         })
}

booksSubject.subscribe(updateBooksDropdown)

songsSubject.subscribe(updateSongsDropdown)

selectedBookIdSubject.subscribe(retrieveSongs)

selectedSongIdSubject.subscribe(activateOpenSongButton)

retrieveBooks()
