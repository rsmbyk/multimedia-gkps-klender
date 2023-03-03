import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'
import * as bcBible from '../../bible/common/bc.js'

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
    return ({ status, source }) => {
        if (status === true) {
            transitionIn(projectSegment)

            if (source !== 'source') {
                if (appName === 'songs') {
                    bcTatib.postStatusMessage(false, 'source', true)
                    bcBible.postStatusMessage(false, 'source', true)
                } else if (appName === 'tatib') {
                    bcSongs.postStatusMessage(false, 'source', true)
                    bcBible.postStatusMessage(false, 'source', true)
                } else if (appName === 'bible') {
                    bcSongs.postStatusMessage(false, 'source', true)
                    bcTatib.postStatusMessage(false, 'source', true)
                }
            }
        }
        else if (projectSegment.is(':visible') && source !== 'source') transitionOut(projectSegment)
    }
}

bcSongs.statusSubject.subscribe(updateDisplayState('songs'))
bcTatib.statusSubject.subscribe(updateDisplayState('tatib'))
bcBible.statusSubject.subscribe(updateDisplayState('bible'))

bcSongs.postStatusMessage(false, 'source')
bcTatib.postStatusMessage(false, 'source')
bcBible.postStatusMessage(false, 'source')
