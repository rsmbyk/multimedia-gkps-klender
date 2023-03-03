import * as bc from '../../../common/bc.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevVerse = $('#display-button-prev-verse')
const buttonNextVerse = $('#display-button-next-verse')

function handleControlInput({ control }) {
    if (control === 'right') {
        if (!buttonNextVerse.hasClass('disabled')) {
            buttonNextVerse.click()
        }
    } else if (control === 'left') {
        if (!buttonPrevVerse.hasClass('disabled')) {
            buttonPrevVerse.click()
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
