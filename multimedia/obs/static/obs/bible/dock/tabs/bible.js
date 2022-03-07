const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'
import { DropdownStateValue } from '/static/helpers/state-value.js'
import * as toasts from '/static/helpers/toasts.js'

import * as browseTab from './browse.js'

const LOCAL_STORAGE_KEY_DROPDOWN_VERSIONS = 'OBS_SONGS_DOCK_BIBLE_DROPDOWN_VERSIONS'
const LOCAL_STORAGE_KEY_DROPDOWN_BOOKS = 'OBS_SONGS_DOCK_BIBLE_DROPDOWN_BOOKS'
const LOCAL_STORAGE_KEY_DROPDOWN_CHAPTERS = 'OBS_SONGS_DOCK_BIBLE_DROPDOWN_CHAPTERS'

const dropdownVersions = $('#bible-dropdown-versions')
const dropdownBooks = $('#bible-dropdown-books')
const dropdownChapters = $('#bible-dropdown-chapters')

const buttonOpenVerse = $('#bible-button-open-verse')

let books
let translations

const versionsSubject = new BehaviorSubject()
const booksSubject = new BehaviorSubject()
const translationsSubject = new BehaviorSubject()
const selectedVersionIdSubject = new BehaviorSubject().pipe(distinctUntilChanged())
const selectedBookIdSubject = new BehaviorSubject().pipe(distinctUntilChanged())
const selectedChapterNumberSubject = new BehaviorSubject().pipe()

const stateValueVersions = new DropdownStateValue(LOCAL_STORAGE_KEY_DROPDOWN_VERSIONS, dropdownVersions)
const stateValueBooks = new DropdownStateValue(LOCAL_STORAGE_KEY_DROPDOWN_BOOKS, dropdownBooks)
const stateValueChapters = new DropdownStateValue(LOCAL_STORAGE_KEY_DROPDOWN_CHAPTERS, dropdownChapters)

dropdownVersions
    .dropdown('setting', 'fullTextSearch', true)
    .dropdown('setting', 'match', 'text')
    .dropdown('setting', 'forceSelection', false)

dropdownBooks
    .dropdown('setting', 'fullTextSearch', true)
    .dropdown('setting', 'match', 'text')
    .dropdown('setting', 'forceSelection', false)

dropdownChapters
    .dropdown('setting', 'fullTextSearch', true)
    .dropdown('setting', 'match', 'text')
    .dropdown('setting', 'forceSelection', false)

buttonOpenVerse.click(() => {
    const translation = translations.find(e => e.book.name === stateValueBooks.currentValue)
    browseTab.open(translation, stateValueChapters.currentValue)
    browseTab.navigateTo()
})

const showVersionsLoader = () => {
    dropdownVersions
        .addClass('loading disabled')
        .dropdown('set text', 'loading')
    dropdownBooks.addClass('disabled').removeClass('loading')
    dropdownChapters.addClass('disabled').removeClass('loading')
    buttonOpenVerse.addClass('disabled')
}

const showBooksLoader = () => {
    dropdownBooks
        .addClass('loading disabled')
        .dropdown('set text', 'loading')
    dropdownVersions.addClass('disabled').removeClass('loading')
    buttonOpenVerse.addClass('disabled')
}

const showChaptersLoader = () => {
    dropdownChapters
        .addClass('loading disabled')
        .dropdown('set text', 'loading')
    dropdownVersions.addClass('disabled').removeClass('loading')
    buttonOpenVerse.addClass('disabled')
}

const hideLoader = () => {
    dropdownVersions.removeClass('loading disabled')
    dropdownBooks.removeClass('loading disabled')
    dropdownChapters.removeClass('loading disabled')
}

const displayVersionsErrorView = (e) => {
    console.log(e)
    toasts.error('Failed to load version list', 'top center')

    dropdownVersions
        .removeClass('loading disabled')
        .dropdown('set text', 'Error')
}

const displayBooksErrorView = () => {
    console.log(e)
    toasts.error('Failed to load book list', 'top center')

    dropdownVersions.removeClass('disabled')
    dropdownBooks
        .removeClass('loading')
        .dropdown('set text', 'Error')
    dropdownChapters
        .removeClass('loading')
        .dropdown('set text', 'Error')
}

const activateOpenVerseButton = () => {
    buttonOpenVerse.removeClass('disabled')
}

const createChaptersDropdownItem = (_, i) => {
    return {
        value: i+1,
        name: i+1,
        selected: (i+1).toString() === stateValueChapters.currentValue
    }
}

const updateChaptersDropdown = selectedBookId => {
    const selectedBook = books.find(e => e.name === selectedBookId)

    if (selectedBook === undefined)
        return

    const values = Array.from({length: selectedBook.number_of_chapters}, createChaptersDropdownItem)
    dropdownChapters.dropdown('change values', values)
    stateValueChapters.init(chapterNumber => selectedChapterNumberSubject.next(chapterNumber), true)

    hideLoader()
}

const createBooksDropdownHeader = (testament, icon) => {
    return {
        name: testament,
        type: 'header',
        icon: icon,
        iconClass: 'icon',
    }
}

const createBooksDropdownItem = translation => {
    return {
        value: translation.book.name,
        name: translation.translation,
        selected: translation.book.name === stateValueBooks.currentValue
    }
}

const updateBooksDropdown = translations => {
    const values = [
        createBooksDropdownHeader('Perjanjian Lama', 'fruit-apple'),
        ...translations.filter(e => e.book.testament === 'old').map(createBooksDropdownItem),
        createBooksDropdownHeader('Perjanjian Baru', 'cross'),
        ...translations.filter(e => e.book.testament === 'new').map(createBooksDropdownItem),
    ]
    dropdownBooks.dropdown('change values', values)
    stateValueBooks.init(bookId => selectedBookIdSubject.next(bookId), true)
}

const retrieveTranslations = selectedVersionId => {
    showBooksLoader()
    showChaptersLoader()

    axios.get(`/api/bible/translations?version=${selectedVersionId}&omit=version`)
        .then(({ data: translations }) => translationsSubject.next(translations))
        .catch(displayBooksErrorView)
}

const createVersionsDropdownItem = version => {
    return {
        value: version.id,
        name: version.lang.name,
        description: version.abbreviation,
        icon: version.lang.id === 2 ? 'id' : 'language',
        iconClass: version.lang.id === 2 ? 'flag' : 'icon',
    }
}

const updateVersionsDropdown = versions => {
    dropdownVersions.dropdown('change values', versions.map(createVersionsDropdownItem))
    stateValueVersions.init(versionId => selectedVersionIdSubject.next(versionId), true)
}

const retrieveVersions = () => {
    showVersionsLoader()

    Promise.all([axios.get('/api/bible/versions'), axios.get('/api/bible/books')])
        .then(([{ data: versions }, { data: books }]) => {
            versionsSubject.next(versions)
            booksSubject.next(books)
        })
        .catch(displayVersionsErrorView)
}

versionsSubject.subscribe(updateVersionsDropdown)

booksSubject.subscribe(v => books = v)

translationsSubject.subscribe(v => translations = v)
translationsSubject.subscribe(updateBooksDropdown)

selectedVersionIdSubject.subscribe(retrieveTranslations)

selectedBookIdSubject.subscribe(updateChaptersDropdown)

selectedChapterNumberSubject.subscribe(activateOpenVerseButton)

retrieveVersions()
