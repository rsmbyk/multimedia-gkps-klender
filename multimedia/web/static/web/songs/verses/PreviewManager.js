import { BehaviorSubject } from '/static/helpers/rx.js'
import { joinAdjacentLyricLines } from './lyric-chunks.js'

const previewSegment = $('#preview-segment')
const previewText = $('.previewText')

const previewButtonPrevLyric = $('.previewButtonPrevLyric')
const previewButtonNextLyric = $('.previewButtonNextLyric')

let activeLyrics
let activeLyricIndex

const activeLyricsSubject = new BehaviorSubject()
const activeLyricIndexSubject = new BehaviorSubject()

const buildLyrics = lyric => {
    activeLyricsSubject.next(joinAdjacentLyricLines(lyric))

    if (activeLyricIndex === undefined || lyric?.length === 0) {
        activeLyricIndexSubject.next(0)
    } else {
        activeLyricIndexSubject.next(Math.min(activeLyricIndex, activeLyrics.length-1))
    }
}

export function openPreview(lyric) {
    buildLyrics(lyric)
    activeLyricIndexSubject.next(0)
    previewSegment.transition('fade up in')
}

export function openModalPreview(lyric, resetIndex=false) {
    buildLyrics(lyric)
    if (resetIndex) {
        activeLyricIndexSubject.next(0)
    }
}

const nextLyric = () => {
    const nextLyricIndex =
        Math.min(activeLyricIndex + 1, activeLyrics.length - 1)

    if (nextLyricIndex !== activeLyricIndex)
        activeLyricIndexSubject.next(nextLyricIndex)
}

const prevLyric = () => {
    const prevLyricIndex =
        Math.max(activeLyricIndex - 1, 0)

    if (prevLyricIndex !== activeLyricIndex)
        activeLyricIndexSubject.next(prevLyricIndex)
}

const updatePreviewText = activeLyricIndex => {
    if (activeLyrics.length === 0) {
        previewText.text('')
    } else {
        previewText.text(activeLyrics[activeLyricIndex])
    }
}

export function closePreview() {
    if (previewSegment.is(':visible')) {
        previewSegment.transition({
            animation: 'fade up out',
            duration: '125ms',
            queue: false,
        })
    }
}

previewSegment.click(e => {
    const clickOnPrevLyric = Array.from(previewButtonPrevLyric).some((b, _) => b.contains(e.target))
    const clickOnNextLyric = Array.from(previewButtonNextLyric).some((b, _) => b.contains(e.target))

    if (clickOnPrevLyric || clickOnNextLyric)
        return false

    closePreview()
})

previewButtonNextLyric.click(nextLyric)
previewButtonPrevLyric.click(prevLyric)

activeLyricsSubject.subscribe(value => activeLyrics = value)

activeLyricIndexSubject.subscribe(value => activeLyricIndex = value)
activeLyricIndexSubject.subscribe(updatePreviewText)
