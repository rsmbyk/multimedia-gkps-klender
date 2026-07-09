import * as hotkeys from '/static/helpers/hotkeys.js'
import * as tabManager from '/static/helpers/tab-manager.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevVerse = $('#display-button-prev-verse')
const buttonNextVerse = $('#display-button-next-verse')

hotkeys.bind('left', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonPrevVerse.hasClass('disabled')) {
            buttonPrevVerse.click()
        }
    }
})

hotkeys.bind('right', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonNextVerse.hasClass('disabled')) {
            buttonNextVerse.click()
        }
    }
})

hotkeys.bind('space', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (buttonStatusActive.is(':visible')) {
            buttonStatusActive.click()
        } else if (buttonStatusInactive.is(':visible')) {
            buttonStatusInactive.click()
        }
    }
})
