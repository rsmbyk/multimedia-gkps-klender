import { BehaviorSubject } from '/static/helpers/rx.js'

import * as doms from '/static/helpers/doms.js'

import * as editTatibModal from './modals/edit-tatib.js'
import * as deleteTatibModal from './modals/delete-tatib.js'

const tatibList = $('#tatib-list')

const calendar = $('#calendar')
const calendarText = $('#calendar-text')
const buttonFilterDate = $('#button-filter-date')
const buttonFilterGeneral = $('#button-filter-general')

const buttonAddTatib = $('#btn-add-tatib')

const placeholderTatibList = $('#placeholder-tatib-list')
const containerTatibList = $('#container-tatib-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

let date

const tatibsSubject = new BehaviorSubject()
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

buttonAddTatib.click(() => {
    editTatibModal.open(null, refreshTatibs)
})

const showLoader = () => {
    buttonAddTatib.addClass('loading disabled')
    calendar.find('.ui.button').addClass('disabled')
    buttonFilterGeneral.addClass('loading disabled')
    buttonFilterDate.addClass('loading disabled')
}

const hideLoader = () => {
    buttonAddTatib.removeClass('loading disabled')
    calendar.find('.ui.button').removeClass('disabled')
    buttonFilterGeneral.removeClass('loading disabled')
    buttonFilterDate.removeClass('loading disabled')
}

const displayPlaceholder = () => {
    placeholderTatibList.show()
    containerTatibList.hide()
    viewError.hide()
    viewEmpty.hide()
}

const displayBookList = () => {
    placeholderTatibList.hide()
    containerTatibList.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderTatibList.hide()
    viewError.show()
}

const displayEmptyView = () => {
    placeholderTatibList.hide()
    viewEmpty.show()
}

const updateFilterButtonText = date => {
    if (date !== null)
        calendarText.text(date.toLocaleString('en-us', {month:'short', year:'numeric'}))
}

const createTatibListItem = tatib => {
    const tatibDate = new Date(tatib.date)
    const dateText = tatib.date === null ? '' : `${tatibDate.getDate()} ${tatibDate.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`

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
                        innerText: tatib.name,
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
        extra.show()
    }, () => {
        extra.hide()
    })

    item.click(e => {
        if (buttonEdit[0].contains(e.target) || buttonDelete[0].contains(e.target))
            return false

        // open book-detail unless clicking the action buttons.
        // clicking on the extra content will still trigger the
        // click.
        window.location = `tatibs/${tatib.id}`
    })

    buttonEdit.click(() => {
        editTatibModal.open(tatib, refreshTatibs)
    })

    buttonDelete.click(() => {
        deleteTatibModal.open(tatib, refreshTatibs)
    })

    extra.hide()

    return item
}

const updateTatibList = books => {
    tatibList.empty()
    tatibList.append(...books.map(createTatibListItem))

    hideLoader()

    if (books.length === 0) displayEmptyView()
    else displayBookList()
}

const refreshTatibs = () => {
    retrieveTatibs(`/api/tatib/tatibs?is_active=true&has_date=${date === null ? 'false' : 'true'}`)
}

const retrieveTatibs = requestUrl => {
    showLoader()
    displayPlaceholder()

    axios.get(requestUrl)
        .then(({ data: tatibs }) => tatibsSubject.next(tatibs))
        .catch(e => {
            displayErrorView(e)
            hideLoader()
        })
}

tatibsSubject.subscribe(updateTatibList)

dateSubject.subscribe(value => date = value)
dateSubject.subscribe(refreshTatibs)
dateSubject.subscribe(updateFilterButtonText)
