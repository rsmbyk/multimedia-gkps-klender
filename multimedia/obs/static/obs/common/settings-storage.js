const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

let lsKeyPrefix = undefined

const LS_KEY_TITLE_TEXT_SIZE = 'SETTINGS_TITLE_TEXT_SIZE'
const LS_KEY_CONTENT_TEXT_SIZE = 'SETTINGS_CONTENT_TEXT_SIZE'
const LS_KEY_BACKGROUND_COLOUR = 'SETTINGS_BACKGROUND_COLOUR'
const LS_KEY_LABEL_COLOUR = 'SETTINGS_LABEL_COLOUR'
const LS_KEY_OPACITY = 'SETTINGS_OPACITY'

export const sizes = ['mini', 'tiny', 'small', 'medium', 'large', 'big', 'huge', 'massive']

const defaultTitleTextSize = 'medium'
const defaultContentTextSize = 'big'
const defaultBackgroundColour = '1a5399'
const defaultLabelColour = '00b200'
const defaultOpacity = 0.89

const getSettingsValue = (key, defaultValue) => {
    let value = localStorage.getItem(key)
    if (value === null) value = defaultValue
    return value
}

const setSettingsValue = (key, value, subject) => {
    localStorage.setItem(key, value)
    subject.next(value)
}

export const setPrefix = prefix => {
    lsKeyPrefix = prefix
    titleTextSizeSubject.next(getTitleTextSize())
    contentTextSizeSubject.next(getContentTextSize())
    backgroundColourSubject.next(getBackgroundColour())
    labelColourSubject.next(getLabelColour())
    opacitySubject.next(getOpacity())
}

const getLSKey = key => {
    if (lsKeyPrefix === undefined)
        throw 'LS Key Prefix has not been set'

    return lsKeyPrefix + '_' + key
}

export const getTitleTextSize = () => getSettingsValue(getLSKey(LS_KEY_TITLE_TEXT_SIZE), defaultTitleTextSize)
export const setTitleTextSize = (value) => setSettingsValue(getLSKey(LS_KEY_TITLE_TEXT_SIZE), value, titleTextSizeSubject)
export const resetTitleTextSize = () => setSettingsValue(getLSKey(LS_KEY_TITLE_TEXT_SIZE), defaultTitleTextSize, titleTextSizeSubject)

export const getContentTextSize = () => getSettingsValue(getLSKey(LS_KEY_CONTENT_TEXT_SIZE), defaultContentTextSize)
export const setContentTextSize = (value) => setSettingsValue(getLSKey(LS_KEY_CONTENT_TEXT_SIZE), value, contentTextSizeSubject)
export const resetContentTextSize = () => setSettingsValue(getLSKey(LS_KEY_CONTENT_TEXT_SIZE), defaultContentTextSize, contentTextSizeSubject)

export const getBackgroundColour = () => getSettingsValue(getLSKey(LS_KEY_BACKGROUND_COLOUR), defaultBackgroundColour)
export const setBackgroundColour = (value) => setSettingsValue(getLSKey(LS_KEY_BACKGROUND_COLOUR), value, backgroundColourSubject)
export const resetBackgroundColour = () => setSettingsValue(getLSKey(LS_KEY_BACKGROUND_COLOUR), defaultBackgroundColour, backgroundColourSubject)

export const getLabelColour = () => getSettingsValue(getLSKey(LS_KEY_LABEL_COLOUR), defaultLabelColour)
export const setLabelColour = (value) => setSettingsValue(getLSKey(LS_KEY_LABEL_COLOUR), value, labelColourSubject)
export const resetLabelColour = () => setSettingsValue(getLSKey(LS_KEY_LABEL_COLOUR), defaultLabelColour, labelColourSubject)

export const getOpacity = () => getSettingsValue(getLSKey(LS_KEY_OPACITY), defaultOpacity)
export const setOpacity = (value) => setSettingsValue(getLSKey(LS_KEY_OPACITY), value, opacitySubject)
export const resetOpacity = () => setSettingsValue(getLSKey(LS_KEY_OPACITY), defaultOpacity, opacitySubject)

export const titleTextSizeSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const contentTextSizeSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const backgroundColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const labelColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const opacitySubject = new BehaviorSubject().pipe(distinctUntilChanged())

window.addEventListener('storage', ({ key, newValue }) => {
    if (lsKeyPrefix === undefined)
        return

    if (key === getLSKey(LS_KEY_TITLE_TEXT_SIZE))
        titleTextSizeSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_CONTENT_TEXT_SIZE))
        contentTextSizeSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_BACKGROUND_COLOUR))
        backgroundColourSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_LABEL_COLOUR))
        labelColourSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_OPACITY))
        opacitySubject.next(newValue)
})
