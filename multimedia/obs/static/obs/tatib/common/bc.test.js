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

describe('tatib BroadcastChannel contracts', () => {
  beforeEach(() => {
    posted.length = 0
    vi.stubGlobal('BroadcastChannel', FakeBroadcastChannel)
    vi.resetModules()
  })

  it('posts tatib item, status, and control payloads', async () => {
    const bc = await import('./bc.js')
    const statuses = []
    bc.statusSubject.subscribe(v => statuses.push(v))

    bc.postTatibItemMessage('Doa', 'Mari berdoa')
    bc.postStatusMessage('inactive', 'source')
    const beforeSkip = statuses.length
    bc.postStatusMessage('active', 'source', true)
    bc.postControlMessage('next')

    expect(posted).toEqual([
      {
        name: 'OBS-TATIB-TATIB-ITEM',
        data: { title: 'Doa', text: 'Mari berdoa' },
      },
      {
        name: 'OBS-TATIB-STATUS',
        data: { status: 'inactive', source: 'source' },
      },
      {
        name: 'OBS-TATIB-STATUS',
        data: { status: 'active', source: 'source' },
      },
      {
        name: 'OBS-TATIB-CONTROL',
        data: { control: 'next' },
      },
    ])
    expect(statuses.at(-1)).toEqual({ status: 'inactive', source: 'source' })
    expect(statuses.length).toBe(beforeSkip)
  })
})
