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

const updateDisplayState = status => {
    if (status === true) passageSegment.removeClass('hidden')
    else passageSegment.addClass('hidden')
}

bc.passageSubject.subscribe(updatePassage)
bc.statusSubject.subscribe(updateDisplayState)

bc.postStatusMessage(false)
