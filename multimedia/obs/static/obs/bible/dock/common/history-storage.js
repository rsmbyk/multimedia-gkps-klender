const LS_KEY_HISTORY = 'OBS_BIBLE_HISTORY'

export const saveHistory = history => {
    console.log(history)
    localStorage.setItem(LS_KEY_HISTORY, JSON.stringify(history))
}

export const loadHistory = () => {
    const history = localStorage.getItem(LS_KEY_HISTORY)
    return history === null ? [] : JSON.parse(history)
}
