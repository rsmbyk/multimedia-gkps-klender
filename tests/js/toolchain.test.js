import { describe, expect, it } from 'vitest'

describe('frontend test toolchain', () => {
  it('runs in a jsdom environment', () => {
    expect(typeof document).toBe('object')
    expect(document.createElement('div').tagName).toBe('DIV')
  })
})
