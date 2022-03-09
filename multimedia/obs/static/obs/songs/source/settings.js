import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../../common/settings-storage.js'

const songSegment = $('#song-segment')
const headerSongInfo = $('#song-info').find('.header')
const label = songSegment.find('.corner.label')
const divider = $('.ui.divider')
const songLyric = $('#song-lyric')

const updateTitleTextSize = titleTextSize => {
    headerSongInfo.removeClass(settingsStorage.sizes)
    headerSongInfo.addClass(titleTextSize)
}

const updateLyricTextSize = contentTextSize => {
    songLyric.removeClass(settingsStorage.sizes)
    songLyric.addClass(contentTextSize)
}

const updateBackgroundColour = () => {
    const backgroundColour = settingsStorage.getBackgroundColour()
    const { r, g, b, a } = colour.hexToRgb(backgroundColour)
    const opacity = isNaN(a) ? settingsStorage.getOpacity() : a / 255
    songSegment.css('background', `rgba(${r}, ${g}, ${b}, ${opacity}`)
}

const updateLabelColour = () => {
    const labelColour = settingsStorage.getLabelColour()
    const { r, g, b, a } = colour.hexToRgb(labelColour)
    const opacity = isNaN(a) ? settingsStorage.getOpacity() : a / 255
    label.css('border-color', `rgba(${r}, ${g}, ${b}, ${opacity}`)
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
