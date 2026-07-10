import { beforeEach, describe, expect, it } from 'vitest'

import { APP_VERSION, applyAppVersion, formatAppVersion } from './version.js'

describe('OBS app version', () => {
  beforeEach(() => {
    document.body.innerHTML = ''
  })

  it('exports a single SemVer product version', () => {
    expect(APP_VERSION).toMatch(/^\d+\.\d+\.\d+$/)
    expect(APP_VERSION).toBe('0.5.0')
  })

  it('formats the display string from the constant', () => {
    expect(formatAppVersion()).toBe('0.5.0')
  })

  it('fills every data-app-version element from the constant', () => {
    document.body.innerHTML = `
      <div data-app-version></div>
      <span data-app-version>stale</span>
    `
    applyAppVersion(document)
    const nodes = [...document.querySelectorAll('[data-app-version]')]
    expect(nodes).toHaveLength(2)
    expect(nodes.every((node) => node.textContent === '0.5.0')).toBe(true)
  })
})
