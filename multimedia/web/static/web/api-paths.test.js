import { describe, expect, it } from 'vitest'
import * as paths from './api-paths.js'

describe('web API path contracts', () => {
  it('builds songs endpoints used by the content UI', () => {
    expect(paths.songsBooksUrl()).toBe('/api/songs/books')
    expect(paths.songsBookUrl(3)).toBe('/api/songs/books/3')
    expect(paths.songsForBookUrl(3)).toBe('/api/songs/songs?book=3')
    expect(paths.songUrl(9)).toBe('/api/songs/songs/9')
    expect(paths.versesForSongUrl(9)).toBe('/api/songs/verses?song=9')
    expect(paths.verseUrl(12)).toBe('/api/songs/verses/12')
  })

  it('builds tatib endpoints used by the content UI', () => {
    expect(paths.tatibsUrl()).toBe('/api/tatib/tatibs')
    expect(paths.tatibUrl(4)).toBe('/api/tatib/tatibs/4')
    expect(paths.tatibItemsUrl(4)).toBe(
      '/api/tatib/items?tatib=4&ordering=order_number',
    )
    expect(paths.tatibItemsReorderUrl()).toBe('/api/tatib/items/reorder')
  })
})
