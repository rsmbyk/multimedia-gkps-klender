const { distinctUntilChanged } = rxjs

import { BehaviorSubject } from '/static/helpers/rx.js'

const BC_NAME_PASSAGE = 'OBS-BIBLE-PASSAGE'
const BC_NAME_STATUS = 'OBS-BIBLE-STATUS'

export const passageSubject = new BehaviorSubject()
export const statusSubject = new BehaviorSubject().pipe(distinctUntilChanged())

const bcPassage = new BroadcastChannel(BC_NAME_PASSAGE)
const bcStatus = new BroadcastChannel(BC_NAME_STATUS)

export const postPassage = (bookName, chapterNumber, verseNumber, title, text) => {
    bcPassage.postMessage({
        bookName: bookName,
        chapterNumber: chapterNumber,
        verseNumber: verseNumber,
        title: title,
        text: text,
    })
}

export const postStatusMessage = (status, skipUpdateSubject) => {
    bcStatus.postMessage({
        status: status,
    })

    if (!skipUpdateSubject) {
        statusSubject.next(status)
    }
}

bcPassage.onmessage = ({ data: passage }) => passageSubject.next(passage)

bcStatus.onmessage = ({ data: status }) => statusSubject.next(status)

passageSubject.subscribe(console.log)
statusSubject.subscribe(console.log)
