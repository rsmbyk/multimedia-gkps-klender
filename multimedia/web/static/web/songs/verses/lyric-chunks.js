/**
 * Isolatable lyric-chunking used by the web verse preview.
 * Extracted so tests do not need Semantic UI transitions.
 */
export function joinAdjacentLyricLines(lyric) {
  const lyricTexts = lyric.split('\n')
  const result = []
  let joinedTexts = ''

  for (let i = 0; i < lyricTexts.length; i++) {
    if (joinedTexts.length !== 0) joinedTexts += '\n'
    joinedTexts += lyricTexts[i]

    if ((i + 1) % 2 === 0) {
      result.push(joinedTexts)
      joinedTexts = ''
    }
  }

  if (joinedTexts.length > 0) result.push(joinedTexts)
  return result
}
