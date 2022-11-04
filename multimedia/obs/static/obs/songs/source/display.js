import * as bc from '../common/bc.js'
import * as options from '../common/options.js'

const segmentDisplay = $('#segment-display')
const boxDisplay = $('#box-display')
const outlineDisplay = $('#outline-display')

let status
let activeDisplay

function transitionIn(element) {
    if (element === undefined)
        return

    element.transition('fade up in')
}

function transitionOut(element) {
    if (element === undefined)
        return

    element.transition({
        animation: 'fade up out',
        duration: '125ms',
        queue: false,
    })
}

function getActiveDisplay(displayMode) {
    switch (displayMode) {
        case options.DISPLAY_MODE_SEGMENT:
            return segmentDisplay
        case options.DISPLAY_MODE_BOX:
            return boxDisplay
        case options.DISPLAY_MODE_OUTLINE:
            return outlineDisplay
        default:
            return undefined
    }
}

function updateDisplayMode(displayMode) {
    if (activeDisplay !== undefined)
        transitionOut(activeDisplay)

    activeDisplay = getActiveDisplay(displayMode)

    if (status === true)
        transitionIn(activeDisplay)
}

function updateDisplayState({ status }) {
    if (activeDisplay === undefined)
        return

    if (status === true) transitionIn(activeDisplay)
    else if (activeDisplay.is(':visible')) transitionOut(activeDisplay)
}

bc.statusSubject.subscribe(value => status = value)
bc.statusSubject.subscribe(updateDisplayState)

bc.postStatusMessage(false)

options.displayModeSubject.subscribe(updateDisplayMode)
