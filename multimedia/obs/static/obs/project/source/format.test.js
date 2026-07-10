import { describe, expect, it } from 'vitest'
import {
  formatPassageProjectContent,
  formatSongProjectContent,
  formatTatibProjectContent,
} from './format.js'

describe('project source formatting', () => {
  it('shows lyric only for songs', () => {
    expect(formatSongProjectContent({ lyric: 'Line one' })).toEqual({
      title: '',
      text: 'Line one',
    })
  })

  it('passes through tatib title and text', () => {
    expect(
      formatTatibProjectContent({ title: 'Doa', text: 'Mari berdoa' }),
    ).toEqual({ title: 'Doa', text: 'Mari berdoa' })
  })

  it('formats bible reference and optional passage title', () => {
    expect(
      formatPassageProjectContent({
        bookName: 'Yohanes',
        chapterNumber: 3,
        verseNumber: 16,
        title: '',
        text: 'Karena begitu besar...',
      }),
    ).toEqual({
      title: 'Yohanes 3 : 16',
      text: 'Karena begitu besar...',
    })

    expect(
      formatPassageProjectContent({
        bookName: 'Yohanes',
        chapterNumber: 3,
        verseNumber: 16,
        title: 'Kasih Allah',
        text: 'Karena begitu besar...',
      }),
    ).toEqual({
      title: 'Yohanes 3 : 16\nKasih Allah',
      text: 'Karena begitu besar...',
    })
  })
})
