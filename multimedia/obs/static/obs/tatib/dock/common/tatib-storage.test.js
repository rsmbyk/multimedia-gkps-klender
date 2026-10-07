import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('tatib storage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.resetModules()
  })

  it('saves, loads, and removes tatib + items', async () => {
    const storage = await import('./tatib-storage.js')
    const tatib = { id: 2, name: 'Ibadah' }
    const items = [{ id: 5, title: 'Intro' }]

    storage.saveTatib(tatib)
    storage.saveTatibItems(items)
    expect(storage.loadTatib()).toEqual(tatib)
    expect(storage.loadTatibItems()).toEqual(items)

    storage.removeTatib()
    storage.removeTatibItems()
    expect(storage.loadTatib()).toBeNull()
    expect(storage.loadTatibItems()).toBeNull()
  })
})
