const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const BC_NAME_PASSAGE = 'OBS-BIBLE-PASSAGE'
const BC_NAME_STATUS = 'OBS-BIBLE-STATUS'
const BC_NAME_CONTROL = 'OBS-BIBLE-CONTROL'

export const passageSubject = new BehaviorSubject()
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

const bcPassage = new BroadcastChannel(BC_NAME_PASSAGE)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)
const bcControl = new BroadcastChannel(BC_NAME_CONTROL)

export const postPassage = (bookName, chapterNumber, verseNumber, title, text) => {
    bcPassage.postMessage({
        bookName: bookName,
        chapterNumber: chapterNumber,
        verseNumber: verseNumber,
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

bcPassage.onmessage = ({ data: passage }) => passageSubject.next(passage)
bcStatus.onmessage = ({ data: status }) => statusSubject.next(status)
bcControl.onmessage = ({ data: control }) => controlSubject.next(control)

passageSubject.subscribe(console.log)
statusSubject.subscribe(console.log)
controlSubject.subscribe(console.log)
