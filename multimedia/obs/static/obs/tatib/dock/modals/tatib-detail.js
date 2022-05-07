import { BehaviorSubject } from '/static/helpers/rx.js'
import * as doms from '/static/helpers/doms.js'
import * as mutations from '/static/helpers/mutations.js'

const modal = $('#modal-tatib-detail')

const tatibName = modal.find('#modal-tatib-detail-tatib-name')
const tatibDate = modal.find('#modal-tatib-detail-tatib-date')

const tatibItemList = modal.find('#modal-tatib-detail-tatib-item-list')

const placeholderTatibInfo = modal.find('#modal-tatib-detail-placeholder-tatib-info')
const placeholderTatibItemList = modal.find('#modal-tatib-detail-placeholder-tatib-item-list')
const containerTatibItemList = modal.find('#modal-tatib-detail-container-tatib-item-list')
const viewError = modal.find('#modal-tatib-detail-view-error')
const viewEmpty = modal.find('#modal-tatib-detail-view-empty')

const tatibSubject = new BehaviorSubject()
const tatibItemsSubject = new BehaviorSubject()

const displayTatibItemListPlaceholder = () => {
    containerTatibItemList.hide()
    viewError.hide()
    viewEmpty.hide()
    placeholderTatibItemList.show()
}

const displayTatibItemList = () => {
    placeholderTatibItemList.hide()
    containerTatibItemList.show()
}

const displayErrorView = e => {
    console.log(e)
    placeholderTatibItemList.hide()
    viewError.show()
}

const displayEmptyView = () => {
    placeholderTatibItemList.hide()
    viewEmpty.show()
}

const displayTatibInfoPlaceholder = () => {
    tatibName.hide()
    tatibDate.hide()
    placeholderTatibInfo.show()
}

const displayTatibInfo = () => {
    placeholderTatibInfo.hide()
    tatibName.show()
    tatibDate.show()
}

const updateTatibInfo = tatib => {
    const date = new Date(tatib.date)
    tatibName.text(tatib.name)
    tatibDate.text(tatib.date === null ? '-' : `${date.getDate()} ${date.toLocaleString('en-us', {
        month: 'long',
        year: 'numeric'
    })}`)

    tatibDate.css('visibility', tatib.date === null ? 'hidden' : 'visible')

    displayTatibInfo()
}

const createTatibItemListItem = tatibItem => {
    return doms.createDOMFromJSON({
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
                        innerText: tatibItem.item_type === 1 ? '--- END OF SECTION ---' : tatibItem.text,
                    },
                ],
            },
        ],
    })
}

const updateTatibItemList = tatibItems => {
    tatibItemList.empty()
    tatibItemList.append(...tatibItems.map(createTatibItemListItem))

    if (tatibItems.length === 0) displayEmptyView()
    else displayTatibItemList()
}

const retrieveTatib = ({ id }) => {
    axios.get(`/api/tatib/tatibs/${id}`)
        .then(({ data: tatib }) => tatibSubject.next(tatib))
        .catch(displayErrorView)
}

const retrieveTatibItems = ({ id }) => {
    axios.get(`/api/tatib/items?tatib=${id}&ordering=order_number`)
        .then(({ data: tatibItems}) => tatibItemsSubject.next(tatibItems))
        .catch(displayErrorView)
}

export const open = tatib => {
    displayTatibItemListPlaceholder()
    displayTatibInfoPlaceholder()
    modal.modal('show')
    retrieveTatib(tatib)
    retrieveTatibItems(tatib)
}

mutations.observeFlexModal(modal[0])

tatibSubject.subscribe(updateTatibInfo)

tatibItemsSubject.subscribe(updateTatibItemList)
