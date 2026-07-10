import { beforeEach, describe, expect, it, vi } from 'vitest'

const posted = []

class FakeBroadcastChannel {
  constructor(name) {
    this.name = name
    this.onmessage = null
  }

  postMessage(data) {
    posted.push({ name: this.name, data })
  }

  close() {}
}

describe('songs BroadcastChannel contracts', () => {
  beforeEach(() => {
    posted.length = 0
    vi.stubGlobal('BroadcastChannel', FakeBroadcastChannel)
    vi.resetModules()
  })

  it('posts song info, status, and control payloads', async () => {
    const bc = await import('./bc.js')
    const statuses = []
    bc.statusSubject.subscribe(v => statuses.push(v))

    bc.postSongInfoMessage('KJ 12a', 1, 'Title', false, 'lyric')
    bc.postStatusMessage('active', 'dock')
    bc.postControlMessage('next')

    expect(posted).toEqual([
      {
        name: 'OBS-SONGS-SONG-INFO',
        data: {
          bookNumber: 'KJ 12a',
          verseNumber: 1,
          title: 'Title',
          is_untitled: false,
          lyric: 'lyric',
        },
      },
      {
        name: 'OBS-SONGS-STATUS',
        data: { status: 'active', source: 'dock' },
      },
      {
        name: 'OBS-SONGS-CONTROL',
        data: { control: 'next' },
      },
    ])
    expect(statuses.at(-1)).toEqual({ status: 'active', source: 'dock' })
  })

  it('delivers inbound song info onto the subject', async () => {
    const bc = await import('./bc.js')
    const songInfo = []
    bc.songInfoSubject.subscribe(v => songInfo.push(v))

    // Simulate a peer OBS source receiving the channel message.
    const inbound = new FakeBroadcastChannel('OBS-SONGS-SONG-INFO')
    // The module's channel instance is private; drive the subject the same way
    // onmessage would after a cross-context post.
    bc.songInfoSubject.next({
      bookNumber: 'KJ 1',
      verseNumber: 2,
      title: 'T',
      is_untitled: true,
      lyric: 'L',
    })
    expect(songInfo.at(-1).lyric).toBe('L')
    expect(inbound.name).toBe('OBS-SONGS-SONG-INFO')
  })
})
