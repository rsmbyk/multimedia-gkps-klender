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

describe('bible BroadcastChannel contracts', () => {
  beforeEach(() => {
    posted.length = 0
    vi.stubGlobal('BroadcastChannel', FakeBroadcastChannel)
    vi.resetModules()
  })

  it('posts passage, status, and control payloads', async () => {
    const bc = await import('./bc.js')

    bc.postPassage('Yohanes', 3, 16, 'Kasih', 'text')
    bc.postControlMessage('prev')

    expect(posted).toEqual([
      {
        name: 'OBS-BIBLE-PASSAGE',
        data: {
          bookName: 'Yohanes',
          chapterNumber: 3,
          verseNumber: 16,
          title: 'Kasih',
          text: 'text',
        },
      },
      {
        name: 'OBS-BIBLE-CONTROL',
        data: { control: 'prev' },
      },
    ])
  })
})
