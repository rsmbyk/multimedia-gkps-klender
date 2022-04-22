import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../../common/settings-storage.js'

const songSegment = $('#song-segment')
const headerSongInfo = $('#song-info').find('.header:not(.sub)')
const songBookInfo = $('#song-book-info')
const songTitle = $('#song-title')
const songLyric = $('#song-lyric')

const label = songSegment.find('.ui.label')
const divider = songSegment.find('.ui.divider')

const updateTitleTextSize = titleTextSize => {
    headerSongInfo.css('font-size', `${titleTextSize}px`)
    headerSongInfo.find('.sub.header').css('font-size', '.6666666667em')
}

const updateLyricTextSize = contentTextSize => {
    songLyric.css('font-size', `${contentTextSize}px`)
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
    songLyric.css('color', `rgba(${hr}, ${hg}, ${hb}, ${ha})`)
    songTitle.css('color', `rgba(${hr}, ${hg}, ${hb}, ${ha})`)
    songBookInfo.css('color', `rgba(${sr}, ${sg}, ${sb}, ${sa})`)
}

const updateBackgroundColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getBackgroundColour())
    songSegment.css('background', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateLabelColour = () => {
    const { r, g, b, a } = extractColour(settingsStorage.getLabelColour())
    label.css('border-color', `rgba(${r}, ${g}, ${b}, ${a})`)
}

const updateDividerOpacity = opacity => {
    divider.css('opacity', opacity)
}

settingsStorage.setPrefix('OBS_SONGS')

settingsStorage.titleTextSizeSubject.subscribe(updateTitleTextSize)

settingsStorage.contentTextSizeSubject.subscribe(updateLyricTextSize)

settingsStorage.textColourSubject.subscribe(updateTextColour)

settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColour)

settingsStorage.labelColourSubject.subscribe(updateLabelColour)

settingsStorage.opacitySubject.subscribe(updateBackgroundColour)
settingsStorage.opacitySubject.subscribe(updateLabelColour)
settingsStorage.opacitySubject.subscribe(updateDividerOpacity)
