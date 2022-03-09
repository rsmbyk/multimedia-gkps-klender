import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../../common/settings-storage.js'

const passageSegment = $('#passage-segment')
const passageVerseReference = $('#passage-verse-reference')
const passageVerse = $('#passage-verse')

const label = passageSegment.find('.ui.label')
const divider = passageSegment.find('.ui.divider')

const updateTitleTextSize = titleTextSize => {
    passageVerseReference.removeClass(settingsStorage.sizes)
    passageVerseReference.addClass(titleTextSize)
}

const updateVerseTextSize = contentTextSize => {
    passageVerse.removeClass(settingsStorage.sizes)
    passageVerse.addClass(contentTextSize)
}

const extractColour = (hexColour) => {
    const { r, g, b, a } = colour.hexToRgb(hexColour)
    const opacity = isNaN(a) ? settingsStorage.getOpacity() : a / 255
    return {
        r: r,
        g: g,
        b: b,
        a: opacity
    }
}

const updateBackgroundColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getBackgroundColour())
    passageSegment.css('background', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateLabelColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getLabelColour())
    label.css('border-color', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateDividerOpacity = opacity => {
    divider.css('opacity', opacity)
}

settingsStorage.setPrefix('OBS_BIBLE')

settingsStorage.titleTextSizeSubject.subscribe(updateTitleTextSize)

settingsStorage.contentTextSizeSubject.subscribe(updateVerseTextSize)

settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColour)

settingsStorage.labelColourSubject.subscribe(updateLabelColour)

settingsStorage.opacitySubject.subscribe(updateBackgroundColour)
settingsStorage.opacitySubject.subscribe(updateLabelColour)
settingsStorage.opacitySubject.subscribe(updateDividerOpacity)
