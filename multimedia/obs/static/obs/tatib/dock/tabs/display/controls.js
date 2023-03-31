import * as bc from '../../../common/bc.js'

import * as display from '../display.js'

const buttonStatusActive = $('#display-button-status-active')
const buttonStatusInactive = $('#display-button-status-inactive')

const buttonPrevItem = $('#display-button-prev-item')
const buttonNextItem = $('#display-button-next-item')
const buttonNextItemActivate = $('#display-button-next-item-activate')

function handleControlInput({ control }) {
    if (control === 'right') {
        if (buttonNextItemActivate.is(':visible')) {
            buttonNextItemActivate.click()
        } else if (!buttonNextItem.hasClass('disabled')) {
            buttonNextItem.click()
        }
    } else if (control === 'left') {
        if (!buttonPrevItem.hasClass('disabled')) {
            buttonPrevItem.click()
        }
    } else if (control === 'space') {
        if (buttonStatusActive.is(':visible')) {
            buttonStatusActive.click()
        } else if (buttonStatusInactive.is(':visible')) {
            buttonStatusInactive.click()
        }
    } else if (control === 'rebroadcast') {
        display.rebroadcast()
    }
}

bc.controlSubject.subscribe(handleControlInput)
