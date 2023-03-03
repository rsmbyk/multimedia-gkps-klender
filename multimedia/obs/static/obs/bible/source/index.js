import * as bc from '../common/bc.js'

const passageSegment = $('#passage-segment')
const passageVerse = $('#passage-verse')

const passageBookName = $('#passage-book-name')
const passageChapterNumber = $('#passage-chapter-number')
const passageVerseNumber = $('#passage-verse-number')
const passageVerseTitle = $('#passage-verse-title')
const passageVerseText = $('#passage-verse-text')

const updatePassage = ({ bookName, chapterNumber, verseNumber, title, text }) => {
    passageBookName.text(bookName)
    passageChapterNumber.text(chapterNumber)
    passageVerseNumber.text(verseNumber)
    passageVerseTitle.text(title)
    passageVerseText.text(text)
}

const doTransition = () => {
    passageVerse.transition({
        animation: 'fade in',
        queue: false,
    })
}

const updateDisplayState = ({ status }) => {
    if (status === true) passageSegment.transition('fade up in')
    else if (passageSegment.is(':visible')) {
        passageSegment.transition({
            animation: 'fade up out',
            duration: '125ms',
            queue: false,
        })
    }
}

bc.passageSubject.subscribe(updatePassage)
bc.passageSubject.subscribe(doTransition)

bc.statusSubject.subscribe(updateDisplayState)

bc.postStatusMessage(false, 'source')
