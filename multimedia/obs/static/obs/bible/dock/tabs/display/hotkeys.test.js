import { beforeEach, describe, expect, it, vi } from 'vitest'

function makeButton({ disabled = false, visible = true } = {}) {
  const el = document.createElement('button')
  if (disabled) el.classList.add('disabled')
  if (!visible) el.style.display = 'none'
  el.click = vi.fn()
  return el
}

function jqueryFromMap(map) {
  return (selector) => {
    const el = map[selector]
    return {
      hasClass: (name) => el.classList.contains(name),
      is: (query) => (query === ':visible' ? el.style.display !== 'none' : false),
      click: (...args) => {
        if (typeof args[0] === 'function') return el
        return el.click(...args)
      },
    }
  }
}

describe('bible display hotkeys', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  it('binds left/right/space to verse and status controls', async () => {
    const bindings = new Map()
    window.hotkeys = (keys, cb) => bindings.set(keys, cb)

    const buttons = {
      '#display-button-status-active': makeButton({ visible: false }),
      '#display-button-status-inactive': makeButton({ visible: true }),
      '#display-button-prev-verse': makeButton(),
      '#display-button-next-verse': makeButton(),
    }
    window.$ = jqueryFromMap(buttons)

    vi.doMock('/static/helpers/tab-manager.js', () => ({
      getActiveTab: () => 'tab-display',
    }))

    await import('./hotkeys.js')

    bindings.get('left')()
    expect(buttons['#display-button-prev-verse'].click).toHaveBeenCalled()
    bindings.get('right')()
    expect(buttons['#display-button-next-verse'].click).toHaveBeenCalled()
    bindings.get('space')()
    expect(buttons['#display-button-status-inactive'].click).toHaveBeenCalled()
  })
})
