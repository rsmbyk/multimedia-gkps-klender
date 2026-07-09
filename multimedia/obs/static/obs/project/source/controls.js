import * as hotkeys from '/static/helpers/hotkeys.js'
import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'
import * as bcBible from '../../bible/common/bc.js'

let lastActiveBC = null

function updateLastActiveApp(bc) {
    return function({ status, source }) {
        if (source !== 'source') {
            lastActiveBC = bc
        }
    }
}

hotkeys.bind('left', function() {
    if (lastActiveBC !== null) {
        lastActiveBC.postControlMessage('left')
    }
})

hotkeys.bind('right', function() {
    if (lastActiveBC !== null) {
        lastActiveBC.postControlMessage('right')
    }
})

hotkeys.bind('space', function() {
    if (lastActiveBC !== null) {
        lastActiveBC.postControlMessage('space')
    }
})

hotkeys.bind('1', function() {
    lastActiveBC = bcSongs
    lastActiveBC.postControlMessage('rebroadcast')
})

hotkeys.bind('2', function() {
    lastActiveBC = bcBible
    lastActiveBC.postControlMessage('rebroadcast')
})

hotkeys.bind('3', function() {
    lastActiveBC = bcTatib
    lastActiveBC.postControlMessage('rebroadcast')
})

bcSongs.statusSubject.subscribe(updateLastActiveApp(bcSongs))
bcTatib.statusSubject.subscribe(updateLastActiveApp(bcTatib))
bcBible.statusSubject.subscribe(updateLastActiveApp(bcBible))

// reinitialize lastActiveBC after subscribing to StatusSubjects
lastActiveBC = null
