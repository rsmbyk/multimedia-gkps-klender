import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('OBS display settings storage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.resetModules()
  })

  it('requires a prefix and round-trips values', async () => {
    const settings = await import('./settings-storage.js')
    expect(() => settings.getTextColour()).toThrow(/LS Key Prefix/)

    settings.setPrefix('SONGS')
    expect(settings.getTextColour()).toBe(settings.defaultTextColour)

    settings.setTextColour('abcdef')
    settings.setOpacity(0.5)
    expect(settings.getTextColour()).toBe('abcdef')
    expect(settings.getOpacity()).toBe('0.5')

    settings.resetTextColour()
    expect(settings.getTextColour()).toBe(settings.defaultTextColour)
  })
})
