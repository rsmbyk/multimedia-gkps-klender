import * as bc from '../common/bc.js'

const tatibSegment = $('#tatib-segment')

const tatibTitle = $('#tatib-title')
const tatibText = $('#tatib-text')

const updateText = tatibItem => {
    tatibTitle.text(tatibItem.title)
    tatibText.text(tatibItem.text)
}

const doTransition = () => {
    tatibText.transition({
        animation: 'fade in',
        queue: false,
    })
}

const updateDisplayState = status => {
    if (status === true) tatibSegment.transition('fade up in')
    else if (tatibSegment.is(':visible')) {
        tatibSegment.transition({
            animation: 'fade up out',
            duration: '125ms',
            queue: false,
        })
    }
}

bc.tatibItemSubject.subscribe(updateText)
bc.tatibItemSubject.subscribe(doTransition)

bc.statusSubject.subscribe(updateDisplayState)

bc.postStatusMessage(false)
