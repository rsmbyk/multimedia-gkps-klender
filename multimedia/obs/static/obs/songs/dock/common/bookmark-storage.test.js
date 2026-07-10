import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('bookmark storage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.resetModules()
  })

  it('saves, loads, and removes bookmark + items', async () => {
    const storage = await import('./bookmark-storage.js')
    const bookmark = { id: 1, name: 'Sunday' }
    const items = [{ id: 10, verse: '1,2' }]

    storage.saveBookmark(bookmark)
    storage.saveBookmarkItems(items)
    expect(storage.loadBookmark()).toEqual(bookmark)
    expect(storage.loadBookmarkItems()).toEqual(items)

    storage.removeBookmark()
    storage.removeBookmarkItems()
    expect(storage.loadBookmark()).toBeNull()
    expect(storage.loadBookmarkItems()).toBeNull()
  })
})
