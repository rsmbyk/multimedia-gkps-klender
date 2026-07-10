import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('project settings storage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.resetModules()
  })

  it('returns defaults then persists colour overrides', async () => {
    const settings = await import('./settings-storage.js')
    expect(settings.getTitleTextColour()).toBe(settings.defaultTitleTextColour)
    expect(settings.getContentTextColour()).toBe(settings.defaultContentTextColour)
    expect(settings.getBackgroundColour()).toBe(settings.defaultBackgroundColour)

    settings.setTitleTextColour('112233')
    settings.setContentTextColour('445566')
    settings.setBackgroundColour('778899')

    expect(settings.getTitleTextColour()).toBe('112233')
    expect(settings.getContentTextColour()).toBe('445566')
    expect(settings.getBackgroundColour()).toBe('778899')

    settings.resetTitleTextColour()
    expect(settings.getTitleTextColour()).toBe(settings.defaultTitleTextColour)
  })
})
