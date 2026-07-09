const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const BC_NAME_TATIB_ITEM = 'OBS-TATIB-TATIB-ITEM'
const BC_NAME_STATUS = 'OBS-TATIB-STATUS'
const BC_NAME_CONTROL = 'OBS-TATIB-CONTROL'

export const tatibItemSubject = new BehaviorSubject()
const statusSubjectInternal = new BehaviorSubject()
export const statusSubject = {
    next(value) {
        statusSubjectInternal.next(value)
    },
    subscribe(...args) {
        return statusSubjectInternal.pipe(distinctUntilChanged()).subscribe(...args)
    },
}
export const controlSubject = new BehaviorSubject()

const bcTatibItem = new BroadcastChannel(BC_NAME_TATIB_ITEM)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)
const bcControl = new BroadcastChannel(BC_NAME_CONTROL)

export const postTatibItemMessage = (title, text) => {
    bcTatibItem.postMessage({
        title: title,
        text: text,
    })
}

export const postStatusMessage = (status, source, skipUpdateSubject) => {
    bcStatus.postMessage({
        status: status,
        source: source,
    })

    if (!skipUpdateSubject) {
        statusSubject.next({ status, source })
    }
}

export function postControlMessage(control) {
    bcControl.postMessage({
        control: control,
    })
}

bcTatibItem.onmessage = ({ data: songInfo }) => tatibItemSubject.next(songInfo)
bcStatus.onmessage = ({ data: status }) => statusSubject.next(status)
bcControl.onmessage = ({ data: control }) => controlSubject.next(control)

tatibItemSubject.subscribe(console.log)
statusSubject.subscribe(console.log)
controlSubject.subscribe(console.log)
