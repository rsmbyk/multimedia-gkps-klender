import { BehaviorSubject } from '/static/helpers/rx.js'

import '/static/helpers/arrays.js'
import * as doms from '/static/helpers/doms.js'
import * as toasts from '/static/helpers/toasts.js'

import * as editItemModal from './modals/edit-item.js'
import * as deleteItemModal from './modals/delete-item.js'

import * as PreviewManager from './PreviewManager.js'

const breadcrumb = $('#breadcrumb')
const breadcrumbTatib = $('#breadcrumb-tatib')

const tatibName = $('#tatib-name')
const tatibDate = $('#tatib-date')

const itemList = $('#item-list')

const containerActionButtons = $('#container-action-buttons')
const buttonAddText = $('#btn-add-item')
const buttonAddEndOfSection = $('#btn-add-eos')

const buttonReorder = $('#btn-reorder')
const buttonSave = $('#btn-save')
const buttonDiscard = $('#btn-discard')

const placeholderTatibInfo = $('#placeholder-tatib-info')
const placeholderItemList = $('#placeholder-item-list')
const containerItemList = $('#container-item-list')
const viewError = $('#view-error')
const viewEmpty = $('#view-empty')

let tatib
let items
let itemsOrder

const tatibSubject = new BehaviorSubject()
const itemsSubject = new BehaviorSubject()
const itemsOrderSubject = new BehaviorSubject(null)

const showLoader = () => {
    buttonAddText.addClass('loading disabled')
    buttonAddEndOfSection.addClass('loading disabled')

    buttonSave.addClass('loading disabled')
    buttonDiscard.addClass('disabled')
    itemList.find('.btnUp').addClass('disabled')
    itemList.find('.btnDown').addClass('disabled')
}

const hideLoader = () => {
    buttonAddText.removeClass('loading disabled')
    buttonAddEndOfSection.removeClass('loading disabled')

    buttonSave.removeClass('loading disabled')
    buttonDiscard.removeClass('disabled')
    itemList.find('.btnUp').removeClass('disabled')
    itemList.find('.btnDown').removeClass('disabled')
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
    buttonReorder.show()
}

const displayErrorView = () => {
    placeholderItemList.hide()
    viewError.show()
}

const displayEmptyView = () => {
    placeholderItemList.hide()
    viewEmpty.show()
    buttonReorder.hide()
}

const handleErrors = e => {
    if (e.response) {
        console.log(e.response.data)
        toasts.error('Reorder bookmark failed')
    } else if (e.request) {
        console.log(e.request)
        toasts.error('Network error. Try again')
    } else {
        console.log(e)
        toasts.error('Something went wrong. Please refresh the page')
    }
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

const onItemsOrderChanged = itemsOrder => {
    if (itemsOrder !== null) {
        updateItemList(itemsOrder)
    } else if (items !== undefined) {
        updateItemList(items)
    }
}

const updateItemListItemsClass = itemsOrder => {
    if (itemsOrder !== null) {
        itemList.removeClass('items')
    } else {
        itemList.addClass('items')
    }
}

const updateActionButtonsVisibility = itemsOrder => {
    if (itemsOrder !== null) {
        buttonAddText.hide()
        buttonAddEndOfSection.hide()
    } else {
        buttonAddText.show()
        buttonAddEndOfSection.show()
    }
}

const updateReorderButtonsVisibility = itemsOrder => {
    if (itemsOrder !== null) {
        buttonReorder.hide()
        buttonDiscard.show()
    } else {
        buttonReorder.show()
        buttonDiscard.hide()
        buttonSave.hide()
    }
}

const updateReorderSaveButton = itemsOrder => {
    if (itemsOrder === null || itemsOrder.equals(items)) {
        buttonSave.hide()
    } else {
        buttonSave.show()
    }
}

const swapItem = (i1, i2) => {
    const newItemsOrder = itemsOrder.concat()
    const temp = newItemsOrder[i1]
    newItemsOrder[i1] = newItemsOrder[i2]
    newItemsOrder[i2] = temp
    return newItemsOrder
}

const moveItemUp = index => {
    if (index > 0)
        itemsOrderSubject.next(swapItem(index, index-1))
}

const moveItemDown = index => {
    if (index < items.length - 1)
        itemsOrderSubject.next(swapItem(index, index+1))
}

const createTatibItemListItem = (tatibItem, index) => {
    const item = doms.createDOMFromJSON({
        tag: 'div',
        classList: ['item'],
        children: [
            {
                tag: 'div',
                classList: ['right', 'floated', 'content'],
                children: [
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'icon', 'button', 'btnUp'],
                        children: [
                            {
                                tag: 'i',
                                classList: ['angle', 'up', 'icon'],
                            },
                        ],
                    },
                    {
                        tag: 'div',
                        classList: ['ui', 'right', 'floated', 'icon', 'button', 'btnDown'],
                        children: [
                            {
                                tag: 'i',
                                classList: ['angle', 'down', 'icon'],
                            },
                        ],
                    },
                ],
            },
            {
                tag: 'div',
                classList: ['content'],
                children: [
                    {
                        tag: 'div',
                        classList: ['description', 'tatibItemTitle'],
                        innerText: tatibItem.title,
                    },
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
                                classList: ['ui', 'secondary', 'icon', 'button', 'btnPreview'],
                                children: [
                                    {
                                        tag: 'i',
                                        classList: ['eye', 'icon'],
                                    },
                                ],
                            },
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

    const title = item.find('.tatibItemTitle')
    title.css('font-weight', '700')

    const extra = item.find('.extra')
    const buttonPreview = item.find('.btnPreview')
    const buttonEdit = item.find('.btnEdit')
    const buttonDelete = item.find('.btnDelete')

    const buttonUp = item.find('.btnUp')
    const buttonDown = item.find('.btnDown')

    buttonUp.click(() => {
        moveItemUp(index)
    })

    buttonDown.click(() => {
        moveItemDown(index)
    })

    item.hover(() => {
        if (itemsOrder === null) {
            extra.show()
        }

        if (tatibItem.item_type === 0) {
            buttonPreview.show()
            buttonEdit.show()
        } else {
            buttonPreview.hide()
            buttonEdit.hide()
        }
    }, () => {
        extra.hide()
    })

    buttonPreview.click(() => {
        PreviewManager.showPreviewText(tatibItem.title, tatibItem.text)
    })

    buttonEdit.click(() => {
        editItemModal.open(tatibItem, tatib, retrieveItems)
    })

    buttonDelete.click(() => {
        deleteItemModal.open(tatibItem, retrieveItems)
    })

    if (itemsOrder === null) {
        buttonUp.hide()
        buttonDown.hide()
    } else {
        buttonUp.show()
        buttonDown.show()
    }

    if (itemsOrder !== null && itemsOrder[index].id !== items[index].id) {
        buttonUp.addClass('secondary')
        buttonDown.addClass('secondary')
    }

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

const buildReorderRequestData = () => {
    return {
        items: itemsOrder.map((item, index) => {
            return {
                item: item.id,
                order_number: index + 1,
            }
        })
    }
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

buttonReorder.click(() => {
    itemsOrderSubject.next(items)
})

buttonDiscard.click(() => {
    itemsOrderSubject.next(null)
})

buttonSave.click(() => {
    showLoader()

    axios.post('/api/tatib/items/reorder', buildReorderRequestData())
        .then(({ data }) => {
            itemsOrderSubject.next(null)
            retrieveItems()
        })
        .catch(handleErrors)
        .finally(hideLoader)
})

tatibSubject.subscribe(value => tatib = value)
tatibSubject.subscribe(updateBreadcrumb)
tatibSubject.subscribe(updateTatibInfo)

itemsSubject.subscribe(value => items = value)
itemsSubject.subscribe(updateItemList)

itemsOrderSubject.subscribe(value => itemsOrder = value)
itemsOrderSubject.subscribe(onItemsOrderChanged)
itemsOrderSubject.subscribe(updateActionButtonsVisibility)
itemsOrderSubject.subscribe(updateReorderButtonsVisibility)
itemsOrderSubject.subscribe(updateReorderSaveButton)
itemsOrderSubject.subscribe(updateItemListItemsClass)

retrieveTatib()
