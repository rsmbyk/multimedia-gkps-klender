const { BehaviorSubject } = rxjs
import *  as tatibStorage from './tatib-storage.js'

export let tatib
export let tatibItems

export const tatibSubject = new BehaviorSubject(tatibStorage.loadTatib())
export const tatibItemsSubject = new BehaviorSubject(tatibStorage.loadTatibItems())

export const activateTatib = tatib => {
    tatibStorage.saveTatib(tatib)
    tatibSubject.next(tatib)
}

export const refreshTatibItems = () => {
    if (tatib === null)
        return

    axios.get(`/api/tatib/items?tatib=${tatib.id}&ordering=order_number`)
        .then(({ data: tatibItems }) => activateTatibItems(tatibItems))
}

const activateTatibItems = tatibItems => {
    tatibStorage.saveTatibItems(tatibItems)
    tatibItemsSubject.next(tatibItems)
}

export const activateSingleTatibItem = (text) => {
    deactivate()
    activateTatib({
        id: 0,
        name: '$QUICK_PASTE$',
    })
    activateTatibItems([{
        item_type: 0,
        text: text,
    }])
}

export const deactivate = () => {
    tatibStorage.removeTatib()
    tatibStorage.removeTatibItems()
    tatibSubject.next(null)
    tatibItemsSubject.next(null)
}

tatibSubject.subscribe(value => tatib = value)
tatibSubject.subscribe(refreshTatibItems)

tatibItemsSubject.subscribe(value => tatibItems = value)
