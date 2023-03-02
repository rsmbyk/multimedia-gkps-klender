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

hotkeys('left', function() {
    if (lastActiveBC !== null) {
        lastActiveBC.postControlMessage('left')
    }
})

hotkeys('right', function() {
    if (lastActiveBC !== null) {
        lastActiveBC.postControlMessage('right')
    }
})

hotkeys('space', function() {
    if (lastActiveBC !== null) {
        lastActiveBC.postControlMessage('space')
    }
})

bcSongs.statusSubject.subscribe(updateLastActiveApp(bcSongs))
bcTatib.statusSubject.subscribe(updateLastActiveApp(bcTatib))
bcBible.statusSubject.subscribe(updateLastActiveApp(bcBible))

// reinitialize lastActiveBC after subscribing to StatusSubjects
lastActiveBC = null
