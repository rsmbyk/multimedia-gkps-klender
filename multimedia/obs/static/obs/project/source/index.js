import * as bcSongs from '../../songs/common/bc.js'
import * as bcTatib from '../../tatib/common/bc.js'

const lyricText = $('#lyric-text')

const updateSongInfo = ({ lyric }) => {
    lyricText.text(lyric)
}

function updateTatibInfo(tatibItem) {
    lyricText.text(tatibItem.text)
}

const doTransition = () => {
    lyricText.transition({
        animation: 'fade in',
        queue: false,
    })
}

bcSongs.songInfoSubject.subscribe(updateSongInfo)
bcSongs.songInfoSubject.subscribe(doTransition)

bcTatib.tatibItemSubject.subscribe(updateTatibInfo)
bcTatib.tatibItemSubject.subscribe(doTransition)
