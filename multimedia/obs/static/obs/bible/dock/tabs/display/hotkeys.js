import * as tabManager from '/static/helpers/tab-manager.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevVerse = $('#display-button-prev-verse')
const buttonNextVerse = $('#display-button-next-verse')

hotkeys('left', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonPrevVerse.hasClass('disabled')) {
            buttonPrevVerse.click()
        }
    }
})

hotkeys('right', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonNextVerse.hasClass('disabled')) {
            buttonNextVerse.click()
        }
    }
})

hotkeys('space', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (buttonStatusActive.is(':visible')) {
            buttonStatusActive.click()
        } else if (buttonStatusInactive.is(':visible')) {
            buttonStatusInactive.click()
        }
    }
})
