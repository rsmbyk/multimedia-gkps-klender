const LS_KEY_TATIB = 'TATIB'
const LS_KEY_TATIB_ITEMS = 'TATIB_ITEMS'

export const saveTatib = tatib => {
    console.log(tatib)
    localStorage.setItem(LS_KEY_TATIB, JSON.stringify(tatib))
}

export const loadTatib = () => {
    return JSON.parse(localStorage.getItem(LS_KEY_TATIB))
}

export const removeTatib = () => {
    localStorage.removeItem(LS_KEY_TATIB)
}

export const saveTatibItems = tatibItems => {
    console.log(tatibItems)
    localStorage.setItem(LS_KEY_TATIB_ITEMS, JSON.stringify(tatibItems))
}

export const loadTatibItems = () => {
    return JSON.parse(localStorage.getItem(LS_KEY_TATIB_ITEMS))
}

export const removeTatibItems = () => {
    localStorage.removeItem(LS_KEY_TATIB_ITEMS)
}
