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
    if (!el) {
      return {
        hasClass: () => false,
        is: () => false,
        click: vi.fn(),
      }
    }
    return {
      hasClass: (name) => el.classList.contains(name),
      is: (query) => {
        if (query === ':visible') return el.style.display !== 'none'
        return false
      },
      click: (...args) => {
        if (typeof args[0] === 'function') return el
        return el.click(...args)
      },
    }
  }
}

describe('songs display hotkeys', () => {
  beforeEach(() => {
    vi.resetModules()
    document.body.innerHTML = ''
  })

  it('binds left/right/space and modifier variants to display controls', async () => {
    const bindings = new Map()
    window.hotkeys = (keys, cb) => bindings.set(keys, cb)

    const buttons = {
      '#display-button-status-active': makeButton({ visible: true }),
      '#display-button-status-inactive': makeButton({ visible: false }),
      '#display-btn-prev-song': makeButton(),
      '#display-btn-next-song': makeButton(),
      '#display-btn-prev-verse': makeButton(),
      '#display-btn-next-verse': makeButton(),
      '#display-btn-prev-lyric': makeButton(),
      '#display-btn-next-lyric': makeButton(),
      '#display-btn-last-lyric': makeButton({ visible: false }),
      '#display-btn-last-verse': makeButton({ visible: false }),
    }
    window.$ = jqueryFromMap(buttons)

    vi.doMock('/static/helpers/tab-manager.js', () => ({
      getActiveTab: () => 'tab-display',
    }))

    await import('./hotkeys.js')

    expect([...bindings.keys()].sort()).toEqual([
      'ctrl+left',
      'ctrl+right',
      'left',
      'right',
      'shift+left',
      'shift+right',
      'space',
    ])

    bindings.get('left')()
    expect(buttons['#display-btn-prev-lyric'].click).toHaveBeenCalled()

    bindings.get('ctrl+right')()
    expect(buttons['#display-btn-next-verse'].click).toHaveBeenCalled()

    bindings.get('shift+left')()
    expect(buttons['#display-btn-prev-song'].click).toHaveBeenCalled()

    bindings.get('space')()
    expect(buttons['#display-button-status-active'].click).toHaveBeenCalled()
  })
})
