import * as hotkeys from '/static/helpers/hotkeys.js'
import * as tabManager from '/static/helpers/tab-manager.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevSong = $('#display-btn-prev-song')
const buttonNextSong = $('#display-btn-next-song')
const buttonPrevVerse = $('#display-btn-prev-verse')
const buttonNextVerse = $('#display-btn-next-verse')
const buttonPrevLyric = $('#display-btn-prev-lyric')
const buttonNextLyric = $('#display-btn-next-lyric')
const buttonLastLyric = $('#display-btn-last-lyric')
const buttonLastVerse = $('#display-btn-last-verse')

hotkeys.bind('left', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonPrevLyric.hasClass('disabled')) {
            buttonPrevLyric.click()
        }
    }
})

hotkeys.bind('right', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (buttonLastVerse.is(':visible')) {
            buttonLastVerse.click()
        } else if (buttonLastLyric.is(':visible')) {
            buttonLastLyric.click()
        } else if (!buttonNextLyric.hasClass('disabled')) {
            buttonNextLyric.click()
        }
    }
})

hotkeys.bind('ctrl+left', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonPrevVerse.hasClass('disabled')) {
            buttonPrevVerse.click()
        }
    }
})

hotkeys.bind('ctrl+right', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonNextVerse.hasClass('disabled')) {
            buttonNextVerse.click()
        }
    }
})

hotkeys.bind('shift+left', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonPrevSong.hasClass('disabled')) {
            buttonPrevSong.click()
        }
    }
})

hotkeys.bind('shift+right', () => {
    if (tabManager.getActiveTab() === 'tab-display') {
        if (!buttonNextSong.hasClass('disabled')) {
            buttonNextSong.click()
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
