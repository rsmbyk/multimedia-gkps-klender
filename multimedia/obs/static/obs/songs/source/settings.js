import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../../common/settings-storage.js'

const songSegment = $('#song-segment')
const headerSongInfo = $('#song-info').find('.header')
const songLyric = $('#song-lyric')

const label = songSegment.find('.ui.label')
const divider = songSegment.find('.ui.divider')

const updateTitleTextSize = titleTextSize => {
    headerSongInfo.removeClass(settingsStorage.sizes)
    headerSongInfo.addClass(titleTextSize)
}

const updateLyricTextSize = contentTextSize => {
    songLyric.removeClass(settingsStorage.sizes)
    songLyric.addClass(contentTextSize)
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

settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColour)

settingsStorage.labelColourSubject.subscribe(updateLabelColour)

settingsStorage.opacitySubject.subscribe(updateBackgroundColour)
settingsStorage.opacitySubject.subscribe(updateLabelColour)
settingsStorage.opacitySubject.subscribe(updateDividerOpacity)
