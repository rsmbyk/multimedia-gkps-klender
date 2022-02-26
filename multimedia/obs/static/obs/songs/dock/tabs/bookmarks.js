import { BehaviorSubject } from '/static/helpers/rx.js'
import * as doms from '/static/helpers/doms.js'

import * as bookmarkManager from '../../common/bookmark-manager.js'

import * as bookmarkDetailModal from '../modals/bookmark-detail.js'
import * as createBookmarkModal from '../modals/create-bookmark.js'
import * as deleteBookmarkModal from '../modals/delete-bookmark.js'

const bookmarkList = $('#bookmarks-bookmark-list')

const calendar = $('#bookmarks-calendar')
const calendarText = $('#bookmarks-calendar-text')
const buttonFilterDate = $('#bookmarks-button-filter-date')
const buttonFilterGeneral = $('#bookmarks-button-filter-general')
const buttonCreateBookmark = $('#bookmarks-button-create-bookmark')

const placeholderBookmarkList = $('#bookmarks-placeholder-bookmark-list')
const containerBookmarkList = $('#bookmarks-container-bookmark-list')
const viewError = $('#bookmarks-view-error')
const viewEmpty = $('#bookmarks-view-empty')

let date

const bookmarksSubject = new BehaviorSubject()
const dateSubject = new BehaviorSubject(new Date())

// initially hide the general filter button
buttonFilterGeneral.hide()

calendar.calendar({
    initialDate: new Date(),
    type: 'month',
    today: true,
    onChange: date => dateSubject.next(new Date(date.getTime())),
})

buttonFilterDate.click(() => {
    showLoader()
    calendar.addClass('disabled')
    buttonFilterDate.hide()
    calendar.hide()
    buttonFilterGeneral.show()
    dateSubject.next(null)
})

buttonFilterGeneral.click(() => {
    showLoader()
    calendar.removeClass('disabled')
    buttonFilterDate.show()
    calendar.show()
    buttonFilterGeneral.hide()
    dateSubject.next(new Date(calendar.calendar('get date').getTime()))
})

buttonCreateBookmark.click(() => {
    createBookmarkModal.open(response => {
        if (response.date === null && date === null) {
            retrieveGeneralBookmarks()
        } else {
            const selectedDate = new Date(date)
            const responseDate = new Date(response.date)

            if (selectedDate.getMonth() === responseDate.getMonth() && selectedDate.getFullYear() === responseDate.getFullYear()) {
                triggerRetrieveBookmarks(selectedDate)
            }
        }
    })
})

const showLoader = () => {
    calendar.find('.ui.button').addClass('disabled')
    buttonFilterGeneral.addClass('loading disabled')
    buttonFilterDate.addClass('loading disabled')
    buttonCreateBookmark.addClass('disabled')
}

const hideLoader = () => {
    calendar.find('.ui.button').removeClass('disabled')
    buttonFilterGeneral.removeClass('loading disabled')
    buttonFilterDate.removeClass('loading disabled')
    buttonCreateBookmark.removeClass('disabled')
}

const showControlButtonsLoader = () => {
    bookmarkList.find('.btnActivate').addClass('disabled')
    bookmarkList.find('.btnEdit').addClass('disabled')
    bookmarkList.find('.btnDelete').addClass('disabled')
}

const hideControlButtonsLoader = () => {
    bookmarkList.find('.btnActivate').removeClass('disabled')
    bookmarkList.find('.btnEdit').removeClass('disabled')
    bookmarkList.find('.btnDelete').removeClass('disabled')
}

const displayPlaceholder = () => {
    containerBookmarkList.hide()
    viewEmpty.hide()
    viewError.hide()
    placeholderBookmarkList.show()
}

const displayBookmarkList = () => {
    placeholderBookmarkList.hide()
    containerBookmarkList.show()
}

const displayEmptyView = () => {
    placeholderBookmarkList.hide()
    viewEmpty.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderBookmarkList.hide()
    viewError.show()
}

const hideCheckIcons = bookmark => {
    if (bookmark === null)
        bookmarkList.find('.icoCheck').hide()
}

const updateFilterButtonText = date => {
    if (date !== null)
        calendarText.text(date.toLocaleString('en-us', {month:'short', year:'numeric'}))
}

const createBookmarkListItem = bookmark => {
    const bookmarkDate = new Date(bookmark.date)
    const dateText = bookmark.date === null ? '' : `${bookmarkDate.getDate()} ${bookmarkDate.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`

    const item = doms.createDOMFromJSON({
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
                        innerText: dateText,
                    },
                ],
            },
            {
                tag: 'div',
                classList: ['extra'],
                children: [
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'mini', 'buttons'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'basic', 'button', 'btnActivate'],
                                innerText: 'Activate',
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'icon', 'button', 'btnEdit'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['pen', 'icon'],
                                    },
                                ],
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'red', 'icon', 'button', 'btnDelete'],
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

    const iconCheck = item.find('.icoCheck')
    const extra = item.find('.extra')
    const buttonActivate = item.find('.btnActivate')
    const buttonEdit = item.find('.btnEdit')
    const buttonDelete = item.find('.btnDelete')

    item.hover(() => {
        if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id) {
            iconCheck.show()
            buttonActivate.hide()
        }
        else {
            iconCheck.hide()
            buttonActivate.show()
        }

        extra.show()
    }, () => {
        if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id) {
            iconCheck.show()
            buttonActivate.hide()
        }
        else {
            iconCheck.hide()
            buttonActivate.show()
        }

        extra.hide()
    })

    if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id)
        buttonActivate.hide()
    else
        iconCheck.hide()

    extra.hide()

    buttonActivate.click(() => {
        showControlButtonsLoader()
        bookmarkList.find('.btnActivate').show()
        buttonActivate.hide()
        bookmarkList.find('.icoCheck').hide()
        iconCheck.show()
        bookmarkManager.activateBookmark(bookmark)
    })

    buttonEdit.click(() => {
        bookmarkDetailModal.open(bookmark)
    })

    buttonDelete.click(() => {
        deleteBookmarkModal.open(bookmark, () => {
            if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id)
                bookmarkManager.deactivate()

            triggerRetrieveBookmarks(date)
        })
    })

    return item
}

const updateBookmarkList = bookmarks => {
    bookmarkList.empty()
    bookmarkList.append(...bookmarks.map(createBookmarkListItem))
    bookmarkList.parent().parent().scrollTop(0)

    hideLoader()

    if (bookmarks.length === 0) displayEmptyView()
    else displayBookmarkList()
}

const retrieveGeneralBookmarks = () => {
    retrieveBookmarks('/api/bookmarks/songs/bookmarks?is_active=true&has_date=false&ordering=name')
}

const retrieveDatedBookmarks = date => {
    const requestUrl = `/api/bookmarks/songs/bookmarks?is_active=true&month=${date.getMonth()+1}&year=${date.getFullYear()}`
    retrieveBookmarks(requestUrl)
}

const triggerRetrieveBookmarks = date => {
    if (date === null) retrieveGeneralBookmarks()
    else retrieveDatedBookmarks(date)
}

const retrieveBookmarks = requestUrl => {
    showLoader()
    displayPlaceholder()

    axios.get(requestUrl)
        .then(({ data: bookmarks }) => bookmarksSubject.next(bookmarks))
        .catch(e => {
            console.log(e)
            displayErrorView()
            hideLoader()
        })
}

bookmarkManager.bookmarkSubject.subscribe(hideCheckIcons)
bookmarkManager.bookmarkItemsSubject.subscribe(hideControlButtonsLoader)

bookmarksSubject.subscribe(updateBookmarkList)

dateSubject.subscribe(value => date = value)
dateSubject.subscribe(triggerRetrieveBookmarks)
dateSubject.subscribe(updateFilterButtonText)
