import * as bc from '../../../common/bc.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevSong = $('#display-btn-prev-song')
const buttonPrevVerse = $('#display-btn-prev-verse')
const buttonPrevLyric = $('#display-btn-prev-lyric')
const buttonNextLyric = $('#display-btn-next-lyric')
const buttonLastLyric = $('#display-btn-last-lyric')
const buttonLastVerse = $('#display-btn-last-verse')

function handleControlInput({ control }) {
    if (control === 'right') {
        if (buttonLastVerse.is(':visible')) {
            buttonLastVerse.click()
        } else if (buttonLastLyric.is(':visible')) {
            buttonLastLyric.click()
        } else if (!buttonNextLyric.hasClass('disabled')) {
            buttonNextLyric.click()
        }
    } else if (control === 'left') {
        if (!buttonPrevLyric.hasClass('disabled')) {
            buttonPrevLyric.click()
        } else if (!buttonPrevVerse.hasClass('disabled')) {
            buttonPrevVerse.click()
        } else if (!buttonPrevSong.hasClass('disabled')) {
            buttonPrevSong.click()
        }
    } else if (control === 'space') {
        if (buttonStatusActive.is(':visible')) {
            buttonStatusActive.click()
        } else if (buttonStatusInactive.is(':visible')) {
            buttonStatusInactive.click()
        }
    }
}

bc.controlSubject.subscribe(handleControlInput)
