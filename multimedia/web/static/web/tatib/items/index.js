import { BehaviorSubject } from '/static/helpers/rx.js'

import * as doms from '/static/helpers/doms.js'
import * as toasts from '/static/helpers/toasts.js'

import * as editItemModal from './modals/edit-item.js'
import * as deleteItemModal from './modals/delete-item.js'

const breadcrumb = $('#breadcrumb')
const breadcrumbTatib = $('#breadcrumb-tatib')

const tatibName = $('#tatib-name')
const tatibDate = $('#tatib-date')

const itemList = $('#item-list')

const containerActionButtons = $('#container-action-buttons')
const buttonAddText = $('#btn-add-item')
const buttonAddEndOfSection = $('#btn-add-eos')

const placeholderTatibInfo = $('#placeholder-tatib-info')
const placeholderItemList = $('#placeholder-item-list')
const containerItemList = $('#container-item-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

let tatib
let items

const tatibSubject = new BehaviorSubject()
const itemsSubject = new BehaviorSubject()

const showLoader = () => {
    buttonAddText.addClass('loading disabled')
    buttonAddEndOfSection.addClass('loading disabled')
}

const hideLoader = () => {
    buttonAddText.removeClass('loading disabled')
    buttonAddEndOfSection.removeClass('loading disabled')
}

const displayTatibInfoPlaceholder = () => {
    placeholderTatibInfo.show()
    breadcrumb.hide()
    tatibName.hide()
    tatibDate.hide()
}

const displayBreadcrumb = () => {
    placeholderTatibInfo.hide()
    breadcrumb.show()
}

const displayTatibInfo = () => {
    placeholderTatibInfo.hide()
    tatibName.show()
    tatibDate.show()
}

const displayItemListPlaceholder = () => {
    placeholderItemList.show()
    containerItemList.hide()
    containerActionButtons.hide()
    viewError.hide()
    viewEmpty.hide()
}

const displayItemList = () => {
    placeholderItemList.hide()
    containerItemList.show()
}

const displayErrorView = () => {
    placeholderItemList.hide()
    viewError.show()
}

const displayEmptyView = () => {
    placeholderItemList.hide()
    viewEmpty.show()
}

const updateBreadcrumb = tatib => {
    const formatDate = () => {
        const date = new Date(tatib.date)
        return `${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`
    }

    breadcrumbTatib.text(tatib.name + (tatib.date === null ? '' : ` (${formatDate()})`))
    displayBreadcrumb()
}

const updateTatibInfo = tatib => {
    const formatDate = () => {
        const date = new Date(tatib.date)
        return `${date.getDate()} ${date.toLocaleString('en-us', {month: 'long', year: 'numeric'})}`
    }

    tatibName.text(tatib.name)
    tatibDate.text(tatib.date === null ? '' : formatDate())
    displayTatibInfo()
}

const createTatibItemListItem = tatibItem => {
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
                        classList: ['description'],
                        innerText: tatibItem.item_type === 1 ? '--- END OF SECTION --- ' : tatibItem.text,
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
        if (tatibItem.item_type === 0) buttonEdit.show()
        else buttonEdit.hide()
    }, () => {
        extra.hide()
    })

    buttonEdit.click(() => {
        editItemModal.open(tatibItem, tatib, retrieveItems)
    })

    buttonDelete.click(() => {
        deleteItemModal.open(tatibItem, retrieveItems)
    })

    extra.hide()

    return item
}

const updateItemList = items => {
    itemList.empty()
    itemList.append(...items.map(createTatibItemListItem))

    hideLoader()
    containerActionButtons.show()

    if (items.length === 0) displayEmptyView()
    else displayItemList()
}

const retrieveItems = () => {
    showLoader()
    displayItemListPlaceholder()

    axios.get(`/api/tatib/items?tatib=${tatibId}&ordering=order_number`)
        .then(({ data: items }) => itemsSubject.next(items))
        .catch(displayErrorView)
}

const retrieveTatib = () => {
    showLoader()
    displayTatibInfoPlaceholder()
    displayItemListPlaceholder()

    axios.get(`/api/tatib/tatibs/${tatibId}`)
        .then(({ data: tatib }) => tatibSubject.next(tatib))
        .then(retrieveItems)
        .catch(displayErrorView)
}

buttonAddEndOfSection.click(() => {
    showLoader()

    const body = {
        tatib: tatibId,
        item_type: 1,
    }

    axios.post('/api/tatib/items', body)
        .then(retrieveItems)
        .catch(e => {
            console.log(e)
            toasts.error('Failed to create item', 'left bottom')
        })
})

buttonAddText.click(() => {
    editItemModal.open(null, tatib, retrieveItems)
})

tatibSubject.subscribe(value => tatib = value)
tatibSubject.subscribe(updateBreadcrumb)
tatibSubject.subscribe(updateTatibInfo)

itemsSubject.subscribe(value => items = value)
itemsSubject.subscribe(updateItemList)

retrieveTatib()
