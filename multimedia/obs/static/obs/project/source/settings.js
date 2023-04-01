import * as colour from '/static/helpers/colour.js'

import * as settingsStorage from '../common/settings-storage.js'

const background = $('body')
const title = $('#project-title')
const text = $('#project-text')

function updateTitleTextColour(titleTextColour) {
    colour.updateStyleColour(title, titleTextColour, 'color')
}

function updateContentTextColour(contentTextColour) {
    colour.updateStyleColour(text, contentTextColour, 'color')
}

function updateBackgroundColour(backgroundColour) {
    colour.updateStyleColour(background, backgroundColour, 'background')
}

settingsStorage.titleTextColourSubject.subscribe(updateTitleTextColour)
settingsStorage.contentTextColourSubject.subscribe(updateContentTextColour)
settingsStorage.backgroundColourSubject.subscribe(updateBackgroundColour)
