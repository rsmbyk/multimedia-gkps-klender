const { BehaviorSubject, distinctUntilChanged } = rxjs
import * as doms from '../../../../../helpers/doms.js'
import * as songDetailModal from '../modals/song-detail.js'

const LOCAL_STORAGE_KEY_BOOKS = 'DROPDOWN_BOOKS'
const LOCAL_STORAGE_KEY_SONGS = 'DROPDOWN_SONGS'

const dropdownBooks  = $('#dropdown-books')
const dropdownSongs  = $('#dropdown-songs')
const buttonOpenSong = $('#button-open-song')

let books
let songs
let selectedBookId
let selectedSongId

const booksSubject          = new BehaviorSubject()
const songsSubject          = new BehaviorSubject()
const selectedBookIdSubject = new BehaviorSubject().pipe(distinctUntilChanged())
const selectedSongIdSubject = new BehaviorSubject()

const booksStateValue = new DropdownStateValue(
    'BOOKS_STATE_VALUE',
    '#dropdown-books',
    LOCAL_STORAGE_KEY_BOOKS,
)

const songsStateValue = new DropdownStateValue(
    'SONGS_STATE_VALUE',
    '#dropdown-songs',
    LOCAL_STORAGE_KEY_SONGS,
)

buttonOpenSong.click(() => {
    songDetailModal.open(songsStateValue.selectedValue)
})

const activateOpenSongButton = selectedSongId => {
    if (selectedSongId === undefined)
        return

    buttonOpenSong.removeClass('disabled')
}

const repopulateSongsDropdown = songs => {
    if (songs === undefined)
        return

    const createMenuSongItem = song => {
        const item = doms.createDOMFromJSON({
            tag: 'div',
            classList: ['item'],
            innerText: song.book.is_hymn_book ? `${song.number}${song.sub_number}. ${song.title}` : song.title,
        })

        item.attr('data-value', song.id)
        return item
    }

    dropdownSongs.find('.menu').empty()
    dropdownSongs.find('.menu').append(...songs.map(createMenuSongItem))

    songsStateValue.init(null, songId => selectedSongIdSubject.next(songId), false)

    if (songs.length === 0) {
        dropdownSongs.addClass('disabled')
        buttonOpenSong.addClass('disabled')
    }
    else {
        dropdownSongs.removeClass('disabled')
        buttonOpenSong.removeClass('disabled')
    }
}

const retrieveSongs = selectedBookId => {
    if (selectedBookId === undefined)
        return

    axios.get(`/api/songs/songs?book=${selectedBookId}`)
         .then(({ data: songs }) => songsSubject.next(songs))
}

const populateBooksDropdown = books => {
    if (books === undefined)
        return

    const createMenuBookItem = book => {
        const item = doms.createDOMFromJSON({
            tag: 'div',
            classList: ['item'],
            children: [
                {
                    tag: 'i',
                    classList: book.lang === 2 ? ['id', 'flag'] : ['language', 'icon'],
                    innerText: '',
                },
                // {
                //     tag: 'span',
                //     classList: ['description'],
                //     innerText: book.lang === 2 ? 'Indonesia' : 'Simalungun',
                // },
                {
                    tag: 'span',
                    classList: ['text'],
                    innerText: book.name,
                },
            ],
        })

        item.attr('data-value', book.id)
        return item
    }

    dropdownBooks.find('.menu').empty()
    dropdownBooks.find('.menu').append(...books.map(createMenuBookItem))
    booksStateValue.init(null, bookId => selectedBookIdSubject.next(bookId), true)
}

const retrieveBooks = () => {
    axios.get('/api/songs/books')
         .then(({ data: books }) => booksSubject.next(books))
}

booksSubject.subscribe(v => books = v)
booksSubject.subscribe(populateBooksDropdown)

songsSubject.subscribe(v => songs = v)
songsSubject.subscribe(repopulateSongsDropdown)

selectedBookIdSubject.subscribe(v => selectedBookId = v)
selectedBookIdSubject.subscribe(retrieveSongs)

selectedSongIdSubject.subscribe(v => selectedSongId = v)
selectedSongIdSubject.subscribe(activateOpenSongButton)

retrieveBooks()
