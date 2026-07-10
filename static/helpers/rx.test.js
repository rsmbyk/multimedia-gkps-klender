import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

describe('BehaviorSubject (rx helper)', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  it('skips undefined until the first real value, then exposes next/getValue', async () => {
    const { BehaviorSubject } = await import('./rx.js')
    const subject = new BehaviorSubject()
    const values = []
    subject.subscribe(value => values.push(value))

    expect(values).toEqual([])
    subject.next(undefined)
    expect(values).toEqual([])
    subject.next('ready')
    expect(values).toEqual(['ready'])
    expect(subject.getValue()).toBe('ready')
  })

  it('keeps next/getValue after additional pipe()', async () => {
    const { skip } = rxjs
    const { BehaviorSubject } = await import('./rx.js')
    const subject = new BehaviorSubject('a')
    const piped = subject.pipe(skip(0))
    expect(typeof piped.next).toBe('function')
    expect(typeof piped.getValue).toBe('function')
    piped.next('b')
    expect(subject.getValue()).toBe('b')
  })
})

describe('local-storage helper', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('round-trips values by key', async () => {
    const { LocalStorageHelper } = await import('./local-storage.js')
    const helper = new LocalStorageHelper('TEST_KEY')
    expect(helper.value).toBeNull()
    helper.setValue('hello')
    expect(helper.value).toBe('hello')
  })
})

describe('hotkeys helper', () => {
  it('binds through window.hotkeys', async () => {
    const bindFn = vi.fn()
    window.hotkeys = bindFn
    const { bind } = await import('./hotkeys.js')
    const cb = () => {}
    bind('left', cb)
    expect(bindFn).toHaveBeenCalledWith('left', cb)
  })
})

describe('arrays equals', () => {
  it('compares nested arrays by value', async () => {
    await import('./arrays.js')
    expect([1, [2, 3]].equals([1, [2, 3]])).toBe(true)
    expect([1, 2].equals([1, 3])).toBe(false)
    expect([1].equals(null)).toBe(false)
  })
})

describe('date-util', () => {
  it('formats a long date string', async () => {
    const { formatLongDate } = await import('./date-util.js')
    expect(formatLongDate('2026-07-10T00:00:00')).toMatch(/10 July 2026/)
  })
})

describe('colour helper', () => {
  it('converts hex to rgb components', async () => {
    const { hexToRgb } = await import('./colour.js')
    expect(hexToRgb('#ff00aa')).toMatchObject({ r: 255, g: 0, b: 170 })
    expect(Number.isNaN(hexToRgb('#ff00aa').a)).toBe(true)
    expect(hexToRgb('#abc')).toMatchObject({ r: 170, g: 187, b: 204 })
  })
})

describe('tab-manager', () => {
  afterEach(() => {
    document.body.innerHTML = ''
    delete window.$
  })

  it('tracks the active tab from Semantic UI callbacks', async () => {
    const settings = {}
    const api = {
      tab(method, arg) {
        if (method === 'setting') {
          settings[arg] = arguments[2]
          return this
        }
        if (method === 'change tab') {
          settings.onVisible?.(arg)
          return this
        }
        return this
      },
      find() {
        return {
          first() {
            return {
              length: 1,
              attr: () => 'tab-display',
            }
          },
        }
      },
    }
    window.$ = () => api

    const tabManager = await import('./tab-manager.js')
    tabManager.init()
    expect(tabManager.getActiveTab()).toBe('tab-display')
    tabManager.changeTab('tab-bible')
    expect(tabManager.getActiveTab()).toBe('tab-bible')
  })
})
