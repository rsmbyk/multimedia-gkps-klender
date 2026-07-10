import { describe, expect, it } from 'vitest'
import { joinAdjacentLyricLines } from './lyric-chunks.js'

describe('joinAdjacentLyricLines', () => {
  it('pairs consecutive lines for preview chunks', () => {
    expect(joinAdjacentLyricLines('a\nb\nc\nd')).toEqual(['a\nb', 'c\nd'])
  })

  it('keeps a trailing odd line', () => {
    expect(joinAdjacentLyricLines('a\nb\nc')).toEqual(['a\nb', 'c'])
  })
})
