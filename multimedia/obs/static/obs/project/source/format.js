/**
 * Pure formatting helpers for the combined project source.
 * Kept free of jQuery/BroadcastChannel so Vitest can lock the display contract.
 */

export function formatSongProjectContent({ lyric }) {
  return {
    title: '',
    text: lyric,
  }
}

export function formatTatibProjectContent({ title, text }) {
  return { title, text }
}

export function formatPassageProjectContent({
  bookName,
  chapterNumber,
  verseNumber,
  title: passageTitle,
  text: passageText,
}) {
  let projectTitle = `${bookName} ${chapterNumber} : ${verseNumber}`
  if (passageTitle && passageTitle.length > 0) {
    projectTitle += `\n${passageTitle}`
  }
  return {
    title: projectTitle,
    text: passageText,
  }
}
