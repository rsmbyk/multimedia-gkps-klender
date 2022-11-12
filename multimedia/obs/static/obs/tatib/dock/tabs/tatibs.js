import { BehaviorSubject } from '/static/helpers/rx.js'
import * as doms from '/static/helpers/doms.js'
import * as tabManager from '/static/helpers/tab-manager.js'

import * as tatibManager from '../common/tatib-manager.js'

import * as tatibDetailModal from '../modals/tatib-detail.js'

const tatibList = $('#tatibs-tatib-list')

const calendar = $('#tatibs-calendar')
const calendarText = $('#tatibs-calendar-text')
const buttonFilterDate = $('#tatibs-button-filter-date')
const buttonFilterGeneral = $('#tatibs-button-filter-general')

const placeholderTatibList = $('#tatibs-placeholder-tatib-list')
const containerTatibList = $('#tatibs-container-tatib-list')
const viewError = $('#tatibs-view-error')
const viewEmpty = $('#tatibs-view-empty')

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

const showLoader = () => {
    calendar.find('.ui.button').addClass('disabled')
    buttonFilterGeneral.addClass('loading disabled')
    buttonFilterDate.addClass('loading disabled')
}

const hideLoader = () => {
    calendar.find('.ui.button').removeClass('disabled')
    buttonFilterGeneral.removeClass('loading disabled')
    buttonFilterDate.removeClass('loading disabled')
}

const showControlButtonsLoader = () => {
    tatibList.find('.btnActivate').addClass('disabled')
    tatibList.find('.btnEdit').addClass('disabled')
    tatibList.find('.btnDelete').addClass('disabled')
}

const hideControlButtonsLoader = () => {
    tatibList.find('.btnActivate').removeClass('disabled')
    tatibList.find('.btnEdit').removeClass('disabled')
    tatibList.find('.btnDelete').removeClass('disabled')
}

const displayPlaceholder = () => {
    containerTatibList.hide()
    viewEmpty.hide()
    viewError.hide()
    placeholderTatibList.show()
}

const displayTatibList = () => {
    placeholderTatibList.hide()
    containerTatibList.show()
}

const displayEmptyView = () => {
    placeholderTatibList.hide()
    viewEmpty.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderTatibList.hide()
    viewError.show()
}

const hideCheckIcons = (activeTatib) => {
    if (activeTatib === null)
        tatibList.find('.icoCheck').hide()
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
                        classList: ['ui', 'right', 'floated', 'mini', 'buttons'],
                        children: [
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'basic', 'button', 'btnActivate'],
                                innerText: 'Activate',
                            },
                            {
                                tag: 'div',
                                classList: ['ui', 'inverted', 'primary', 'icon', 'button', 'btnDisplay'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['desktop', 'icon'],
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
    const buttonDisplay = item.find('.btnDisplay')

    console.log(tatibManager.tatib, tatib.name, tatib.id)

    if (tatibManager.tatib !== null && tatibManager.tatib.id === tatib.id) {
        iconCheck.show()
        buttonActivate.hide()
        buttonDisplay.show()
    } else {
        iconCheck.hide()
        buttonDisplay.hide()
        buttonActivate.show()
    }

    buttonActivate.click(() => {
        tatibList.find('.btnActivate').show()
        buttonActivate.hide()
        tatibList.find('.btnDisplay').hide()
        buttonDisplay.show()
        tatibList.find('.icoCheck').hide()
        iconCheck.show()
        tatibManager.activateTatib(tatib)
    })

    buttonDisplay.click(() => {
        tabManager.changeTab('tab-display')
    })

    item.click(e => {
        if (buttonActivate[0].contains(e.target) || buttonDisplay[0].contains(e.target))
            return false

        tatibDetailModal.open(tatib)
    })

    return item
}

const updateTatibList = tatibs => {
    tatibList.empty()
    tatibList.append(...tatibs.map(createTatibListItem))
    tatibList.parent().parent().scrollTop(0)

    hideLoader()

    if (tatibs.length === 0) displayEmptyView()
    else displayTatibList()
}

const triggerRetrieveTatibs = date => {
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

tatibManager.tatibSubject.subscribe(hideCheckIcons)
tatibManager.tatibItemsSubject.subscribe(hideControlButtonsLoader)

tatibsSubject.subscribe(updateTatibList)

dateSubject.subscribe(value => date = value)
dateSubject.subscribe(triggerRetrieveTatibs)
dateSubject.subscribe(updateFilterButtonText)
