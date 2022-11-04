const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const BC_NAME_TATIB_ITEM = 'OBS-TATIB-TATIB-ITEM'
const BC_NAME_STATUS = 'OBS-TATIB-STATUS'

export const tatibItemSubject = new BehaviorSubject()
export const statusSubject = new BehaviorSubject().pipe(distinctUntilChanged())

const bcTatibItem = new BroadcastChannel(BC_NAME_TATIB_ITEM)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)

export const postTatibItemMessage = (title, text) => {
    bcTatibItem.postMessage({
        title: title,
        text: text,
    })
}

export const postStatusMessage = status => {
    bcStatus.postMessage({
        status: status,
    })

    statusSubject.next(status)
}

bcTatibItem.onmessage = ({ data: songInfo }) => tatibItemSubject.next(songInfo)

bcStatus.onmessage = ({ data: status }) => statusSubject.next(status)

tatibItemSubject.subscribe(console.log)
statusSubject.subscribe(console.log)
