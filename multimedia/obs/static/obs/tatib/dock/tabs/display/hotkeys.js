import * as tabManager from '/static/helpers/tab-manager.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevItem = $('#display-button-prev-item')
const buttonNextItem = $('#display-button-next-item')
const buttonNextItemActivate = $('#display-button-next-item-activate')

hotkeys('left', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonPrevItem.hasClass('disabled')) {
            buttonPrevItem.click()
        }
    }
})

hotkeys('right', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (buttonNextItemActivate.is(':visible')) {
            buttonNextItemActivate.click()
        } else if (!buttonNextItem.hasClass('disabled')) {
            buttonNextItem.click()
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
