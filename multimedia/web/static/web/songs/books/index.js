const { BehaviorSubject, skipWhile } = rxjs

import * as doms from '/static/helpers/doms.js'

import * as editBookModal from './modals/edit-book.js'
import * as deleteBookModal from './modals/delete-book.js'

const bookList = $('#book-list')

const buttonAddBook = $('#btn-add-book')

const placeholderBookList = $('#placeholder-book-list')
const containerBookList = $('#container-book-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

const booksSubject = new BehaviorSubject().pipe(skipWhile(books => books === undefined))

buttonAddBook.click(() => editBookModal.open(null, retrieveBooks))

const showLoader = () => {
    buttonAddBook.addClass('loading disabled')
}

const hideLoader = () => {
    buttonAddBook.removeClass('loading disabled')
}

const displayPlaceholder = () => {
    placeholderBookList.show()
    containerBookList.hide()
    viewError.hide()
    viewEmpty.hide()
}

const displayBookList = () => {
    placeholderBookList.hide()
    containerBookList.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderBookList.hide()
    viewError.show()
}

const displayEmptyView = () => {
    placeholderBookList.hide()
    viewEmpty.show()
}

const createBookListItem = book => {
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
                        innerText: book.name,
                    },
                    {
                        tag: 'div',
                        classList: ['description'],
                        innerText: book.lang === 1 ? 'Simalungun' : 'Indonesia',
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

    item.hover(() => {
        if (book.is_hymn_book === false) extra.show()
    }, () => {
        extra.hide()
    })

    item.click(e => {
        if (buttonEdit[0].contains(e.target) || buttonDelete[0].contains(e.target))
            return false

        // open book-detail unless clicking the action buttons.
        // clicking on the extra content will still trigger the
        // click.
        window.location = `books/${book.id}`
    })

    buttonEdit.click(() => {
        editBookModal.open(book, retrieveBooks)
    })

    buttonDelete.click(() => {
        deleteBookModal.open(book, retrieveBooks)
    })

    extra.hide()

    return item
}

const updateBookList = books => {
    bookList.empty()
    bookList.append(...books.map(createBookListItem))

    hideLoader()

    if (books.length === 0) displayEmptyView()
    else displayBookList()
}

const retrieveBooks = () => {
    showLoader()
    displayPlaceholder()

    axios.get('/api/songs/books')
        .then(({ data: books }) => booksSubject.next(books))
        .catch(displayErrorView)
}

booksSubject.subscribe(updateBookList)

retrieveBooks()
