const DisplayTab = () => {
    const songBookNumber = $('#display-song-book-number')
    const songTitle      = $('#display-song-title')
    const songVerses     = $('#display-song-verses')
    const songLyricList  = $('#display-song-lyric-list')

    const btnStatusActive = $('#display-button-status-active')
    const btnStatusInactive = $('#display-button-status-inactive')

    const btnPrevSong  = $('#display-btn-prev-song')
    const btnNextSong  = $('#display-btn-next-song')
    const btnPrevVerse = $('#display-btn-prev-verse')
    const btnNextVerse = $('#display-btn-next-verse')
    const btnPrevLyric = $('#display-btn-prev-lyric')
    const btnNextLyric = $('#display-btn-next-lyric')

    let activeBookmark
    let activeBookmarkItems

    let   activeSong
    const activeSongSubject = new BehaviorSubject(null)
    activeSongSubject.subscribe(v => activeSong = v)
    let   activeVerses
    const activeVersesSubject = new BehaviorSubject([])
    activeVersesSubject.subscribe(v => activeVerses = v)
    let   activeLyrics
    const activeLyricsSubject = new BehaviorSubject([])
    activeLyricsSubject.subscribe(v => activeLyrics = v)

    let   activeSongIndex
    const activeSongIndexSubject = new BehaviorSubject(null)
    activeSongIndexSubject.subscribe(v => activeSongIndex = v)
    let   activeVerseIndex
    const activeVerseIndexSubject = new BehaviorSubject(null)
    activeVerseIndexSubject.subscribe(v => activeVerseIndex = v)
    let   activeLyricIndex
    const activeLyricIndexSubject = new BehaviorSubject(null)
    activeLyricIndexSubject.subscribe(v => activeLyricIndex = v)

    let   numberOfLine = 1
    const numberOfLineSubject = new BehaviorSubject(null)

    const update = bookmarkItems => {
        if (bookmarkItems === null) setIdle()
        else init()
    }

    const setIdle = () => {

    }

    const init = () => {
        activeSongIndexSubject.next(0)
    }

    const setSongBookNumber = value => songBookNumber.text(value)
    const setSongTitle = value => songTitle.text(value)

    const setSongVerses = (activeVerses) => {
        const createVerseText = (verseNumber, index) => {
            const item = createDOMFromJSON({
                tag: 'span',
                classList: ['ui', 'inverted', 'text'],
                innerText: verseNumber,
            })

            $(item)
                .css('cursor', 'pointer')
                .css('padding-left', '0.28em')
                .css('padding-right', '0.28em')
                .click(() => {
                    activeVerseIndexSubject.next(index)
                })

            return item
        }

        songVerses.empty()
        songVerses.append(...activeVerses.map(v => v.number).map(createVerseText))
    }

    const updateSong = () => {
        if (activeSongIndex === null)
            return

        activeSongSubject.next(activeBookmarkItems[activeSongIndex])
        activeVersesSubject.next(activeBookmarkItems[activeSongIndex].verse_info)
        activeVerseIndexSubject.next(0)
    }

    const updateSongInfo = (activeSong) => {
        if (activeSong === null)
            return

        setSongBookNumber(activeSong.song_info.book_number)
        setSongTitle(activeSong.song_info.title)
    }

    const updateActiveVerseMarker = (activeVerseIndex) => {
        songVerses.children().addClass('disabled')
        songVerses.children().eq(activeVerseIndex).removeClass('disabled')
    }

    const buildLyrics = (activeVerseIndex) => {
        if (activeVerseIndex === null)
            return

        const joinAdjacentText = lyricTexts => {
            const result = []
            let joinedTexts = ''

            for (let i=0; i < lyricTexts.length; i++) {
                if (joinedTexts.length !== 0) joinedTexts += '\n'
                joinedTexts += lyricTexts[i]

                if ((i+1) % numberOfLine === 0) {
                    result.push(joinedTexts)
                    joinedTexts = ''
                }
            }

            if (joinedTexts.length > 0) result.push(joinedTexts)
            return result
        }

        const lyric = activeVerses[activeVerseIndex].lyric
        activeLyricsSubject.next(joinAdjacentText(lyric.split('\n')))
    }

    const updateLyricList = (activeLyrics) => {
        const createLyricTextItem = (lyricText, index) => {
            const item = createDOMFromJSON({
                tag: 'div',
                classList: ['item'],
                children: [
                    {
                        tag: 'i',
                        classList: ['inverted', 'middle', 'aligned', 'small', 'map', 'marker', 'icon'],
                        innerText: '',
                    },
                    {
                        tag: 'div',
                        classList: ['middle', 'aligned', 'content'],
                        innerText: lyricText,
                    },
                ],
            })

            const icoMarker = $(item).find('i.icon')
            if (index !== activeLyricIndex) icoMarker.hide()

            $(item).click(() => activeLyricIndexSubject.next(index))

            return item
        }

        songLyricList.empty()
        songLyricList.append(...activeLyrics.map(createLyricTextItem))

        activeLyricIndexSubject.next(0)
    }

    const updateActiveLyricMarker = (activeLyricIndex) => {
        songLyricList.find('.item i.icon').hide()
        songLyricList.children().eq(activeLyricIndex).find('i.icon').show()
    }

    const nextSong = () => {
        const nextSongIndex =
            Math.min(activeSongIndex + 1, activeBookmarkItems.length - 1)

        if (nextSongIndex !== activeSongIndex)
            activeSongIndexSubject.next(nextSongIndex)
    }

    const prevSong = () => {
        const prevSongIndex =
            Math.max(activeSongIndex - 1, 0)

        if (prevSongIndex !== activeSongIndex)
            activeSongIndexSubject.next(prevSongIndex)
    }

    const nextVerse = () => {
        const nextVerseIndex =
            Math.min(activeVerseIndex + 1, activeVerses.length - 1)

        if (nextVerseIndex !== activeVerseIndex)
            activeVerseIndexSubject.next(nextVerseIndex)
    }

    const prevVerse = () => {
        const prevVerseIndex =
            Math.max(activeVerseIndex - 1, 0)

        if (prevVerseIndex !== activeVerseIndex)
            activeVerseIndexSubject.next(prevVerseIndex)
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

    const evaluateButton = (button, isValid) => {
        if (isValid) button.removeClass('disabled')
        else button.addClass('disabled')
    }

    const evaluateButtonStatusActive = activeBookmarkItems =>
        evaluateButton(btnStatusActive, activeBookmarkItems !== null)
    const evaluateButtonStatusInactive = activeBookmarkItems =>
        evaluateButton(btnStatusInactive, activeBookmarkItems !== null)

    const evaluateButtonNextLyric = activeLyricIndex =>
        evaluateButton(btnNextLyric, activeLyricIndex !== activeLyrics.length - 1)
    const evaluateButtonPrevLyric = activeLyricIndex =>
        evaluateButton(btnPrevLyric, activeLyricIndex !== 0)
    const evaluateButtonNextVerse = activeVerseIndex =>
        evaluateButton(btnNextVerse, activeVerseIndex !== activeVerses.length - 1)
    const evaluateButtonPrevVerse = activeVerseIndex =>
        evaluateButton(btnPrevVerse, activeVerseIndex !== 0)
    const evaluateButtonNextSong = activeSongIndex =>
        evaluateButton(btnNextSong, activeSongIndex !== activeBookmarkItems.length - 1)
    const evaluateButtonPrevSong = activeSongIndex =>
        evaluateButton(btnPrevSong, activeSongIndex !== 0)

    bookmarkManager.activeBookmark.subscribe(value => activeBookmark = value)

    bookmarkManager.activeBookmarkItems.subscribe(value => activeBookmarkItems = value)
    bookmarkManager.activeBookmarkItems.subscribe(update)

    new ToggleButton(btnStatusActive, btnStatusInactive)

    btnNextSong.click(nextSong)
    btnPrevSong.click(prevSong)
    btnNextVerse.click(nextVerse)
    btnPrevVerse.click(prevVerse)
    btnNextLyric.click(nextLyric)
    btnPrevLyric.click(prevLyric)

    bookmarkManager.activeBookmarkItems.subscribe(evaluateButtonStatusActive)
    bookmarkManager.activeBookmarkItems.subscribe(evaluateButtonStatusInactive)
    activeSongIndexSubject.subscribe(updateSong)
    activeSongIndexSubject.subscribe(evaluateButtonNextSong)
    activeSongIndexSubject.subscribe(evaluateButtonPrevSong)
    activeSongSubject.subscribe(updateSongInfo)
    activeVersesSubject.subscribe(setSongVerses)
    activeVerseIndexSubject.subscribe(updateActiveVerseMarker)
    activeVerseIndexSubject.subscribe(buildLyrics)
    activeVerseIndexSubject.subscribe(evaluateButtonNextVerse)
    activeVerseIndexSubject.subscribe(evaluateButtonPrevVerse)
    activeLyricsSubject.subscribe(updateLyricList)
    activeLyricIndexSubject.subscribe(updateActiveLyricMarker)
    activeLyricIndexSubject.subscribe(evaluateButtonNextLyric)
    activeLyricIndexSubject.subscribe(evaluateButtonPrevLyric)
}
