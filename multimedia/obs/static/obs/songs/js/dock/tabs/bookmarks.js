const { BehaviorSubject } = rxjs
import * as doms from '../../../../../helpers/doms.js'
import * as bookmarkManager from '../../common/bookmark-manager.js'
import * as bookmarkDetailModal from '../modals/bookmark-detail.js'
import * as createBookmarkModal from '../modals/create-bookmark.js'
import * as deleteBookmarkModal from '../modals/delete-bookmark.js'

const bookmarkList         = $('#bookmark-list')
const buttonCreateBookmark = $('#button-create-bookmark')
const buttonFilterCalendar = $('#button-filter-calendar')
const buttonFilterDate     = $('#button-filter-date')
const buttonFilterGeneral  = $('#button-filter-general')
const buttonFilterText     = $('#button-filter-text')

const placeholderBookmarkList = $('#bookmarks-placeholder-bookmark-list')
const viewError = $('#bookmarks-view-error')
const viewEmpty = $('#bookmarks-view-empty')

let bookmarks
let currentDate
let generalBookmark

const bookmarksSubject = new BehaviorSubject()
const currentDateSubject = new BehaviorSubject(new Date())
const generalBookmarkSubject = new BehaviorSubject(false)

// initially hide the general filter button
buttonFilterGeneral.hide()

buttonFilterCalendar.calendar({
    type: 'month',
    today: true,
    onChange: date => {
        currentDateSubject.next(new Date(date.getTime()))
        refresh()
    },
})

buttonFilterDate.click(() => {
    generalBookmarkSubject.next(true)
    buttonFilterCalendar.addClass('disabled')
    buttonFilterDate.hide()
    buttonFilterCalendar.hide()
    buttonFilterGeneral.show()
})

buttonFilterGeneral.click(() => {
    generalBookmarkSubject.next(false)
    buttonFilterCalendar.removeClass('disabled')
    buttonFilterDate.show()
    buttonFilterCalendar.show()
    buttonFilterGeneral.hide()
})

buttonCreateBookmark.click(() => {
    createBookmarkModal.open(retrieveBookmarks)
})

const displayBookmarksView = () => {
    bookmarkList.parent().show()
}

const displayEmptyView = () => {
    viewEmpty.show()
}

const displayErrorView = () => {
    viewError.show()
}

const displayLoader = () => {
    bookmarkList.parent().hide()
    viewEmpty.hide()
    viewError.hide()
    placeholderBookmarkList.show()

    buttonCreateBookmark.addClass('disabled')

    buttonFilterDate.addClass('loading disabled')
    buttonFilterGeneral.addClass('loading disabled')
    buttonFilterCalendar.find('.button').addClass('disabled')
}

const hideLoader = () => {
    placeholderBookmarkList.hide()

    buttonCreateBookmark.removeClass('disabled')

    buttonFilterDate.removeClass('loading disabled')
    buttonFilterGeneral.removeClass('loading disabled')
    buttonFilterCalendar.find('.button').removeClass('disabled')
}

const displayControlButtonLoader = () => {
    bookmarkList.find('.btnActivate').addClass('disabled')
    bookmarkList.find('.btnEdit').addClass('disabled')
    bookmarkList.find('.btnDelete').addClass('disabled')
}

const hideControlButtonLoader = () => {
    bookmarkList.find('.btnActivate').removeClass('disabled')
    bookmarkList.find('.btnEdit').removeClass('disabled')
    bookmarkList.find('.btnDelete').removeClass('disabled')
}

const createBookmarkItem = bookmark => {
    const date = new Date(bookmark.date)
    const dateText = generalBookmark ? '' : `${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`


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
                        classList: ['ui', 'right', 'floated', 'tiny', 'buttons'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'basic', 'button', 'btnActivate'],
                                innerText: 'Activate'
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'icon', 'button', 'btnEdit'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['pen', 'icon'],
                                    },
                                ]
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'red', 'icon', 'button', 'btnDelete'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['trash', 'icon'],
                                    },
                                ]
                            },
                        ]
                    },
                ],
            },
        ],
    })

    const iconCheck = item.find('.icoCheck')
    const extraButtons = item.find('.extra > .ui.buttons')
    const buttonActivate = extraButtons.find('.btnActivate')
    const buttonEdit = extraButtons.find('.btnEdit')
    const buttonDelete = extraButtons.find('.btnDelete')

    item.hover(() => {
        if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id) {
            iconCheck.show()
            buttonActivate.hide()
        }
        else {
            iconCheck.hide()
            buttonActivate.show()
        }
        extraButtons.show()
    }, () => {
        if (bookmarkManager.bookmark === null || bookmark.id !== bookmarkManager.bookmark.id) {
            iconCheck.hide()
            buttonActivate.show()
        }
        else {
            iconCheck.show()
            buttonActivate.hide()
        }
        extraButtons.hide()
    })

    if (bookmarkManager.bookmark !== null && bookmark.id === bookmarkManager.bookmark.id)
        buttonActivate.hide()
    else
        iconCheck.hide()

    extraButtons.hide()

    buttonActivate.click(() => {
        displayControlButtonLoader()
        $('#bookmark-list .btnActivate').show()
        buttonActivate.hide()
        $('#bookmark-list .icoCheck').hide()
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
            refresh()
        }, console.log)
    })

    return item
}

const updateBookmarkList = bookmarks => {
    if (bookmarks === undefined)
        return

    hideLoader()

    if (bookmarks.length === 0) displayEmptyView()
    else displayBookmarksView()

    bookmarkList.empty()
    bookmarkList.append(...bookmarks.map(createBookmarkItem))
    bookmarkList.parent().parent().scrollTop(0)
}

const retrieveBookmarks = () => {
    if (generalBookmark === undefined && currentDate === undefined)
        return

    displayLoader()

    let requestUrl

    if (generalBookmark === true)
        requestUrl ='/api/bookmarks/songs/bookmarks?is_active=true&has_date=false&ordering=name'
    else
        requestUrl = `/api/bookmarks/songs/bookmarks?is_active=true&month=${currentDate.getMonth()+1}&year=${currentDate.getFullYear()}`

    axios.get(requestUrl)
        .then(({ data: bookmarks }) => bookmarksSubject.next(bookmarks))
        .catch(e => {
            console.log(e)
            displayErrorView()
            hideLoader()
        })
}

const updateFilterButtonText = currentDate => {
    buttonFilterText.text(currentDate.toLocaleString('en-us', {month:'short', year:'numeric'}))
}

const refresh = () => {
    retrieveBookmarks()
}

bookmarkManager.bookmarkItemsSubject.subscribe(hideControlButtonLoader)

bookmarksSubject.subscribe(value => bookmarks = value)
bookmarksSubject.subscribe(updateBookmarkList)

currentDateSubject.subscribe(value => currentDate = value)
currentDateSubject.subscribe(retrieveBookmarks)
currentDateSubject.subscribe(updateFilterButtonText)

generalBookmarkSubject.subscribe(value => generalBookmark = value)
generalBookmarkSubject.subscribe(retrieveBookmarks)
