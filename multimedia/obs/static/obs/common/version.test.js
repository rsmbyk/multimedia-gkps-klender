import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { beforeEach, describe, expect, it } from 'vitest'

import { APP_VERSION, applyAppVersion, formatAppVersion } from './version.js'

const here = dirname(fileURLToPath(import.meta.url))

describe('OBS app version', () => {
  beforeEach(() => {
    document.body.innerHTML = ''
  })

  it('exports a single SemVer product version', () => {
    expect(APP_VERSION).toMatch(/^\d+\.\d+\.\d+$/)
    expect(APP_VERSION).toBe('0.5.1')
  })

  it('formats the display string from the constant', () => {
    expect(formatAppVersion()).toBe('0.5.1')
  })

  it('fills every data-app-version element from the constant', () => {
    document.body.innerHTML = `
      <div data-app-version></div>
      <span data-app-version>stale</span>
    `
    applyAppVersion(document)
    const nodes = [...document.querySelectorAll('[data-app-version]')]
    expect(nodes).toHaveLength(2)
    expect(nodes.every((node) => node.textContent === '0.5.1')).toBe(true)
  })

  it('dock indexes import version from obs/common (not per-app common)', () => {
    // From obs/<app>/dock/index.js, ../common points at obs/<app>/common
    // (404 in production). The shared module lives at obs/common/version.js.
    for (const app of ['songs', 'bible', 'tatib']) {
      const src = readFileSync(
        join(here, '..', app, 'dock', 'index.js'),
        'utf8',
      )
      expect(src).toMatch(/from ['"]\.\.\/\.\.\/common\/version\.js['"]/)
      expect(src).not.toMatch(/from ['"]\.\.\/common\/version\.js['"]/)
    }
  })
})
