import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('bible history storage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.resetModules()
  })

  it('defaults to [] and round-trips history', async () => {
    const storage = await import('./history-storage.js')
    expect(storage.loadHistory()).toEqual([])

    const history = [{ chapterNumber: 3, verseNumber: 16 }]
    storage.saveHistory(history)
    expect(storage.loadHistory()).toEqual(history)
  })
})
