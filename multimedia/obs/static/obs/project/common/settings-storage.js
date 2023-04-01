const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const LS_KEY_PROJECT_TITLE_TEXT_COLOUR = 'SETTINGS_PROJECT_TITLE_TEXT_COLOUR'
const LS_KEY_PROJECT_CONTENT_TEXT_COLOUR = 'SETTINGS_PROJECT_CONTENT_TEXT_COLOUR'
const LS_KEY_PROJECT_BACKGROUND_COLOUR = 'SETTINGS_PROJECT_BACKGROUND_COLOUR'

export const defaultTitleTextColour = 'ffe951'
export const defaultContentTextColour = 'ffffff'
export const defaultBackgroundColour = '323233'

export const titleTextColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const contentTextColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const backgroundColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())

const getSettingsValue = (key, defaultValue) => {
    let value = localStorage.getItem(key)
    if (value === null) value = defaultValue
    return value
}

const setSettingsValue = (key, value, subject) => {
    localStorage.setItem(key, value)
    subject.next(value)
}

export const getTitleTextColour = () => getSettingsValue(LS_KEY_PROJECT_TITLE_TEXT_COLOUR, defaultTitleTextColour)
export const setTitleTextColour = (value) => setSettingsValue(LS_KEY_PROJECT_TITLE_TEXT_COLOUR, value, titleTextColourSubject)
export const resetTitleTextColour = () => setTitleTextColour(defaultTitleTextColour)

export const getContentTextColour = () => getSettingsValue(LS_KEY_PROJECT_CONTENT_TEXT_COLOUR, defaultContentTextColour)
export const setContentTextColour = (value) => setSettingsValue(LS_KEY_PROJECT_CONTENT_TEXT_COLOUR, value, contentTextColourSubject)
export const resetContentTextColour = () => setContentTextColour(defaultContentTextColour)

export const getBackgroundColour = () => getSettingsValue(LS_KEY_PROJECT_BACKGROUND_COLOUR, defaultBackgroundColour)
export const setBackgroundColour = (value) => setSettingsValue(LS_KEY_PROJECT_BACKGROUND_COLOUR, value, backgroundColourSubject)
export const resetBackgroundColour = () => setBackgroundColour(defaultBackgroundColour)

window.addEventListener('storage', ({ key, newValue }) => {
    if (key === LS_KEY_PROJECT_TITLE_TEXT_COLOUR)
        titleTextColourSubject.next(newValue)

    else if (key === LS_KEY_PROJECT_CONTENT_TEXT_COLOUR)
        contentTextColourSubject.next(newValue)

    else if (key === LS_KEY_PROJECT_BACKGROUND_COLOUR)
        backgroundColourSubject.next(newValue)
})

window.onload = function() {
    titleTextColourSubject.next(getTitleTextColour())
    contentTextColourSubject.next(getContentTextColour())
    backgroundColourSubject.next(getBackgroundColour())
}
