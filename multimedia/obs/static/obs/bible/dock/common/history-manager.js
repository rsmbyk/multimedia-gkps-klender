import { BehaviorSubject } from '/static/helpers/rx.js'

import * as historyStorage from './history-storage.js';

const historyLimit = 25

let history

export const historySubject = new BehaviorSubject()
const originalHistorySubject = new BehaviorSubject(historyStorage.loadHistory())

export const addItem = (translation, chapterNumber, verses, verseNumber) => {
    const item = {
        translation: translation,
        chapterNumber: chapterNumber,
        verses: verses,
        verseNumber: verseNumber,
    }

    const index = history.findIndex(e => {
        return e.translation.name === translation.name &&
               e.chapterNumber === chapterNumber &&
               e.verseNumber === verseNumber
    })

    if (index > -1) history.splice(index, 1)

    history.push(item)

    if (history.length > historyLimit) history.shift()

    historyStorage.saveHistory(history)
    originalHistorySubject.next(history)
}

originalHistorySubject.subscribe(v => history = v)
originalHistorySubject.subscribe(v => historySubject.next(v.concat().reverse()))
