const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

let lsKeyPrefix = undefined

const LS_KEY_TITLE_TEXT_SIZE = 'SETTINGS_TITLE_TEXT_SIZE'
const LS_KEY_CONTENT_TEXT_SIZE = 'SETTINGS_CONTENT_TEXT_SIZE'
const LS_KEY_TEXT_COLOUR = 'SETTINGS_TEXT_COLOUR'
const LS_KEY_BACKGROUND_COLOUR = 'SETTINGS_BACKGROUND_COLOUR'
const LS_KEY_LABEL_ICON_COLOUR = 'SETTINGS_LABEL_ICON_COLOUR'
const LS_KEY_LABEL_BACKGROUND_COLOUR = 'SETTINGS_LABEL_BACKGROUND_COLOUR'
const LS_KEY_OPACITY = 'SETTINGS_OPACITY'

export const sizes = ['mini', 'tiny', 'small', 'medium', 'large', 'big', 'huge', 'massive']

const defaultTitleTextSize = 18
const defaultContentTextSize = 26
const defaultTextColour = 'ffffff'
const defaultBackgroundColour = '1a5399'
const defaultLabelIconColour = 'ffffff'
const defaultLabelBackgroundColour = '00b200'
const defaultOpacity = 0.89

export const textSizeMinValue = 1
export const textSizeMaxValue = 64

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
    textColourSubject.next(getTextColour())
    backgroundColourSubject.next(getBackgroundColour())
    labelIconColourSubject.next(getLabelIconColour())
    labelBackgroundColourSubject.next(getLabelBackgroundColour())
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

export const getTextColour = () => getSettingsValue(getLSKey(LS_KEY_TEXT_COLOUR), defaultTextColour)
export const setTextColour = (value) => setSettingsValue(getLSKey(LS_KEY_TEXT_COLOUR), value, textColourSubject)
export const resetTextColour = () => setSettingsValue(getLSKey(LS_KEY_TEXT_COLOUR), defaultTextColour, textColourSubject)

export const getBackgroundColour = () => getSettingsValue(getLSKey(LS_KEY_BACKGROUND_COLOUR), defaultBackgroundColour)
export const setBackgroundColour = (value) => setSettingsValue(getLSKey(LS_KEY_BACKGROUND_COLOUR), value, backgroundColourSubject)
export const resetBackgroundColour = () => setSettingsValue(getLSKey(LS_KEY_BACKGROUND_COLOUR), defaultBackgroundColour, backgroundColourSubject)

export const getLabelIconColour = () => getSettingsValue(getLSKey(LS_KEY_LABEL_ICON_COLOUR), defaultLabelIconColour)
export const setLabelIconColour = (value) => setSettingsValue(getLSKey(LS_KEY_LABEL_ICON_COLOUR), value, labelIconColourSubject)
export const resetLabelIconColour = () => setSettingsValue(getLSKey(LS_KEY_LABEL_ICON_COLOUR), defaultLabelIconColour, labelIconColourSubject)

export const getLabelBackgroundColour = () => getSettingsValue(getLSKey(LS_KEY_LABEL_BACKGROUND_COLOUR), defaultLabelBackgroundColour)
export const setLabelBackgroundColour = (value) => setSettingsValue(getLSKey(LS_KEY_LABEL_BACKGROUND_COLOUR), value, labelBackgroundColourSubject)
export const resetLabelBackgroundColour = () => setSettingsValue(getLSKey(LS_KEY_LABEL_BACKGROUND_COLOUR), defaultLabelBackgroundColour, labelBackgroundColourSubject)

export const getOpacity = () => getSettingsValue(getLSKey(LS_KEY_OPACITY), defaultOpacity)
export const setOpacity = (value) => setSettingsValue(getLSKey(LS_KEY_OPACITY), value, opacitySubject)
export const resetOpacity = () => setSettingsValue(getLSKey(LS_KEY_OPACITY), defaultOpacity, opacitySubject)

export const titleTextSizeSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const contentTextSizeSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const textColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const backgroundColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const labelIconColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const labelBackgroundColourSubject = new BehaviorSubject().pipe(distinctUntilChanged())
export const opacitySubject = new BehaviorSubject().pipe(distinctUntilChanged())

window.addEventListener('storage', ({ key, newValue }) => {
    if (lsKeyPrefix === undefined)
        return

    if (key === getLSKey(LS_KEY_TITLE_TEXT_SIZE))
        titleTextSizeSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_CONTENT_TEXT_SIZE))
        contentTextSizeSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_TEXT_COLOUR))
        textColourSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_BACKGROUND_COLOUR))
        backgroundColourSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_LABEL_ICON_COLOUR))
        labelIconColourSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_LABEL_BACKGROUND_COLOUR))
        labelBackgroundColourSubject.next(newValue)

    else if (key === getLSKey(LS_KEY_OPACITY))
        opacitySubject.next(newValue)
})
