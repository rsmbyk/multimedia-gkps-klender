import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'

const projectSegment = $('#project-segment')

function transitionIn(element) {
    if (element === undefined)
        return

    element.transition('fade in')
}

function transitionOut(element) {
    if (element === undefined)
        return

    element.transition({
        animation: 'fade out',
        duration: '125ms',
        queue: false,
    })
}

function updateDisplayState(appName) {
    return ({ status }) => {
        if (status === true) {
            transitionIn(projectSegment)

            if (appName === 'songs') {
                bcTatib.postStatusMessage(false, true)
            } else if (appName === 'tatib') {
                bcSongs.postStatusMessage(false, true)
            }
        }
        else if (projectSegment.is(':visible')) transitionOut(projectSegment)
    }
}

bcSongs.statusSubject.subscribe(updateDisplayState('songs'))
bcTatib.statusSubject.subscribe(updateDisplayState('tatib'))

bcSongs.postStatusMessage(false)
bcTatib.postStatusMessage(false)
