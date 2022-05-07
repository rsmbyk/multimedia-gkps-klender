import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../../common/settings-storage.js'

const tatibSegment = $('#tatib-segment')
const tatibText = $('#tatib-text')

const label = tatibSegment.find('.ui.label')
const divider = tatibSegment.find('.ui.divider')

const updateTatibTextSize = contentTextSize => {
    tatibText.css('font-size', `${contentTextSize}px`)
}

const extractColour = (hexColour, defaultOpacity=null) => {
    const { r, g, b, a } = colour.hexToRgb(hexColour)
    const opacity = isNaN(a) ? defaultOpacity !== null ? defaultOpacity : settingsStorage.getOpacity() : a / 255
    return {
        r: r,
        g: g,
        b: b,
        a: opacity
    }
}

const updateTextColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getTextColour(), 1)
    tatibText.css('color', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateBackgroundColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getBackgroundColour())
    tatibSegment.css('background', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateLabelIconColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getLabelIconColour())
    label.find('.icon').css('color', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateLabelBackgroundColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getLabelBackgroundColour())
    label.css('border-color', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateDividerOpacity = opacity => {
    divider.css('opacity', opacity)
}

settingsStorage.setPrefix('OBS_TATIB')

settingsStorage.contentTextSizeSubject.subscribe(updateTatibTextSize)

settingsStorage.textColourSubject.subscribe(updateTextColour)

settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColour)

settingsStorage.labelIconColourSubject.subscribe(updateLabelIconColour)

settingsStorage.labelBackgroundColourSubject.subscribe(updateLabelBackgroundColour)

settingsStorage.opacitySubject.subscribe(updateBackgroundColour)
settingsStorage.opacitySubject.subscribe(updateLabelIconColour)
settingsStorage.opacitySubject.subscribe(updateLabelBackgroundColour)
settingsStorage.opacitySubject.subscribe(updateDividerOpacity)
