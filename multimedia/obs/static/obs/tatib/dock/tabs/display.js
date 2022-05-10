import { BehaviorSubject } from '/static/helpers/rx.js';
import { ToggleButton } from '/static/helpers/buttons.js'
import * as doms from '/static/helpers/doms.js'

import * as focusManager from '../../../common/focusManager.js'

import * as bc from '../../common/bc.js'

import * as tatibManager from '../common/tatib-manager.js'

const hasPopup = $('#tab-display .hasPopup')

const tatibName = $('#display-tatib-name')

const tatibItemList = $('#display-tatib-item-list')

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevItem = $('#display-button-prev-item')
const buttonNextItem = $('#display-button-next-item')
const buttonNextItemActivate = $('#display-button-next-item-activate')

const placeholderTatibName = $('#display-placeholder-tatib-name')
const placeholderTatibItemList = $('#display-placeholder-tatib-item-list')
const containerTatibItemList = $('#display-container-tatib-item-list')

let tatibItems
let activeItemIndex

const tatibItemsSubject = new BehaviorSubject()
const activeItemIndexSubject = new BehaviorSubject()

const displayTatibItemListPlaceholder = () => {
    containerTatibItemList.hide()
    viewEmpty.hide()
    placeholderTatibItemList.show()
}

const displayTatibNamePlaceholder = () => {
    tatibName.hide()
    placeholderTatibName.show()
}

const displayTatibName = () => {
    placeholderTatibName.hide()
    tatibName.show()
}

const displayTatibItemList = () => {
    placeholderTatibItemList.hide()
    containerTatibItemList.show()
}

const displayEmptyView = () => {
    placeholderTatibItemList.hide()
    viewEmpty.show()
}

const setIdle = () => {
    toggleButtonStatus.setInactive()
    activeItemIndexSubject.next(null)
    displayTatibItemListPlaceholder()
    displayTatibNamePlaceholder()
}

const init = () => {
    toggleButtonStatus.setInactive()
    activeItemIndexSubject.next(0)
    displayTatibItemList()
    displayTatibName()
}

const onTatibItemsUpdated = tatibItems => {
    if (tatibItems === null) setIdle()
    else init()
}

const appendEndOfTatib = tatibItems => {
    if (tatibItems === null) {
        tatibItemsSubject.next(null)
    } else {
        tatibItemsSubject.next([
            ...tatibItems,
            {
                item_type: 0,
                text: '--- END ---',
            },
        ])
    }
}

const updateTatibName = tatib => {
    tatibName.text(tatib.name)
}

const updateActiveItemMarker = activeItemIndex => {
    if (activeItemIndex === null)
        return

    tatibItemList.find('.item i.icon').hide()
    tatibItemList.children().eq(activeItemIndex).find('i.icon').show()
}

const createTatibItemListItem = (tatibItem, index) => {
    const item = doms.createDOMFromJSON({
        tag: 'div',
        classList: ['item'],
        children: [
            {
                tag: 'i',
                classList: ['inverted', 'middle', 'aligned', 'small', 'map', 'marker', 'alternate', 'icon'],
                innerText: '',
            },
            {
                tag: 'div',
                classList: ['middle', 'aligned', 'content'],
                innerText: tatibItem.item_type === 1 ? '--- END OF SECTION ---' : tatibItem.text,
            },
        ],
    })

    const iconMarker = item.find('i.icon')
    if (index !== activeItemIndex) iconMarker.hide()

    item.click(() => activeItemIndexSubject.next(index))

    return item
}

const updateTatibItemList = tatibItems => {
    if (tatibItems === null)
        return

    tatibItemList.empty()
    tatibItemList.append(...tatibItems.map(createTatibItemListItem))
}

const updateStatusButton = status => {
    if (status === true) toggleButtonStatus.setActive()
    else toggleButtonStatus.setInactive()
}

const checkEndOfSection = activeItemIndex => {
    if (activeItemIndex !== null && tatibItems[activeItemIndex].item_type === 1)
        toggleButtonStatus.setInactive()
}

const checkEndOfTatib = activeItemIndex => {
    if (activeItemIndex !== null && activeItemIndex === tatibItems.length - 1)
        toggleButtonStatus.setInactive()
}

const evaluateButton = (button, isValid) => {
    if (isValid) button.removeClass('disabled')
    else button.addClass('disabled')
}

const evaluateButtonStatusActive = tatibItems =>
    evaluateButton(buttonStatusActive, tatibItems !== null && tatibItems.length !== 0)
const evaluateButtonStatusInactive = tatibItems =>
    evaluateButton(buttonStatusInactive, tatibItems !== null && tatibItems.length !== 0)
const evaluateButtonPrevItem = activeItemIndex =>
    evaluateButton(buttonPrevItem, activeItemIndex !== null && activeItemIndex !== 0)
const evaluateButtonNextItem = activeItemIndex =>
    evaluateButton(buttonNextItem, activeItemIndex !== null && activeItemIndex !== tatibItems.length - 1)

const evaluateButtonNextItemActivate = activeItemIndex => {
    if (activeItemIndex !== null && tatibItems[activeItemIndex].item_type === 1 && activeItemIndex <= tatibItems.length - 3 && tatibItems[activeItemIndex + 1].item_type === 0) {
        buttonNextItem.hide()
        buttonNextItemActivate.show()
    } else {
        buttonNextItem.show()
        buttonNextItemActivate.hide()
    }
}

const prevItem = () => {
    const prevItemIndex =
        Math.max(activeItemIndex - 1, 0)

    if (prevItemIndex !== activeItemIndex)
        activeItemIndexSubject.next(prevItemIndex)
}

const nextItem = () => {
    const nextItemIndex =
        Math.min(activeItemIndex + 1, tatibItems.length)

    if (nextItemIndex !== activeItemIndex)
        activeItemIndexSubject.next(nextItemIndex)
}

const postStatusMessage = status => {
    bc.postStatusMessage(status)
}

const postTatibItem = activeItemIndex => {
    if (activeItemIndex === null)
        return

    bc.postTatibItemMessage(tatibItems[activeItemIndex].text)
}

const toggleButtonStatus = new ToggleButton(
    buttonStatusActive,
    buttonStatusInactive,
    () => {
        if (activeItemIndex === tatibItems.length - 1 || tatibItems[activeItemIndex].item_type === 1)
            return false

        postStatusMessage(true)
        postTatibItem(activeItemIndex)
    },
    () => {
        postStatusMessage(false)
    },
)

buttonPrevItem.click(prevItem)
buttonNextItem.click(nextItem)

buttonNextItemActivate.click(() => {
    nextItem()
    toggleButtonStatus.setActive()
})

focusManager.registerFocusChange('red')

tatibManager.tatibSubject.subscribe(updateTatibName)

tatibManager.tatibItemsSubject.subscribe(appendEndOfTatib)
tatibManager.tatibItemsSubject.subscribe(evaluateButtonStatusActive)
tatibManager.tatibItemsSubject.subscribe(evaluateButtonStatusInactive)

bc.statusSubject.subscribe(updateStatusButton)

tatibItemsSubject.subscribe(value => tatibItems = value)
tatibItemsSubject.subscribe(onTatibItemsUpdated)
tatibItemsSubject.subscribe(updateTatibItemList)

activeItemIndexSubject.subscribe(value => activeItemIndex = value)
activeItemIndexSubject.subscribe(postTatibItem)
activeItemIndexSubject.subscribe(updateActiveItemMarker)
activeItemIndexSubject.subscribe(evaluateButtonPrevItem)
activeItemIndexSubject.subscribe(evaluateButtonNextItem)
activeItemIndexSubject.subscribe(evaluateButtonNextItemActivate)
activeItemIndexSubject.subscribe(checkEndOfSection)
activeItemIndexSubject.subscribe(checkEndOfTatib)

hasPopup.popup()
