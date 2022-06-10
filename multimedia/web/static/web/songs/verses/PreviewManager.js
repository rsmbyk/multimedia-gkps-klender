import { BehaviorSubject } from '/static/helpers/rx.js'

const previewSegment = $('#preview-segment')
const previewText = $('#preview-text')

const previewButtonNextLyric = $('#preview-button-next-lyric')
const previewButtonPrevLyric = $('#preview-button-prev-lyric')

let activeLyrics
let activeLyricIndex

const activeLyricsSubject = new BehaviorSubject()
const activeLyricIndexSubject = new BehaviorSubject()

export const buildLyrics = lyric => {
    const joinAdjacentText = lyricTexts => {
        const result = []
        let joinedTexts = ''

        for (let i=0; i < lyricTexts.length; i++) {
            if (joinedTexts.length !== 0) joinedTexts += '\n'
            joinedTexts += lyricTexts[i]

            if ((i+1) % 2 === 0) {
                result.push(joinedTexts)
                joinedTexts = ''
            }
        }

        if (joinedTexts.length > 0) result.push(joinedTexts)
        return result
    }

    activeLyricsSubject.next(joinAdjacentText(lyric.split('\n')))
    activeLyricIndexSubject.next(0)
    previewSegment.transition('fade up in')
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
    previewText.text(activeLyrics[activeLyricIndex])
}

previewSegment.click(e => {
    if (previewButtonNextLyric[0].contains(e.target) || previewButtonPrevLyric[0].contains(e.target))
        return false

    previewSegment.transition({
        animation: 'fade up out',
        duration: '125ms',
        queue: false,
    })
})

previewButtonNextLyric.click(nextLyric)
previewButtonPrevLyric.click(prevLyric)

activeLyricsSubject.subscribe(value => activeLyrics = value)

activeLyricIndexSubject.subscribe(value => activeLyricIndex = value)
activeLyricIndexSubject.subscribe(updatePreviewText)
