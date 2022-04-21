import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../../common/settings-storage.js'

const passageSegment = $('#passage-segment')
const passageVerseReference = $('#passage-verse-reference')
const passageVerse = $('#passage-verse')
const passageVerseTitle = $('#passage-verse-title')
const passageVerseText = $('#passage-verse-text')

const label = passageSegment.find('.ui.label')
const divider = passageSegment.find('.ui.divider')

const updateTitleTextSize = titleTextSize => {
    passageVerseReference.css('font-size', `${titleTextSize}px`)
}

const updateVerseTextSize = contentTextSize => {
    passageVerse.css('font-size', `${contentTextSize}px`)
    passageVerseTitle.css('font-size', '.6666666667em')
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
    // h means header, s means subheader
    const { r: hr, g: hg, b: hb, a: ha } = extractColour(settingsStorage.getTextColour(), 1)
    const { r: sr, g: sg, b: sb, a: sa } = extractColour(settingsStorage.getTextColour(), 0.8)
    passageVerseReference.css('color', `rgba(${hr}, ${hg}, ${hb}, ${ha})`)
    passageVerseText.css('color', `rgba(${hr}, ${hg}, ${hb}, ${ha})`)
    passageVerseTitle.css('color', `rgba(${sr}, ${sg}, ${sb}, ${sa})`)
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

settingsStorage.textColourSubject.subscribe(updateTextColour)

settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColour)

settingsStorage.labelColourSubject.subscribe(updateLabelColour)

settingsStorage.opacitySubject.subscribe(updateBackgroundColour)
settingsStorage.opacitySubject.subscribe(updateLabelColour)
settingsStorage.opacitySubject.subscribe(updateDividerOpacity)
