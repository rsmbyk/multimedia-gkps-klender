/**
 * Web UI API paths used by content-admin screens.
 * Kept as named helpers so Vitest can lock the contracts without Semantic UI.
 */

export const songsBooksUrl = () => '/api/songs/books'
export const songsBookUrl = (id) => `/api/songs/books/${id}`
export const songsForBookUrl = (bookId) => `/api/songs/songs?book=${bookId}`
export const songUrl = (id) => `/api/songs/songs/${id}`
export const songsCreateUrl = () => '/api/songs/songs'
export const versesForSongUrl = (songId) => `/api/songs/verses?song=${songId}`
export const versesCreateUrl = () => '/api/songs/verses'
export const verseUrl = (id) => `/api/songs/verses/${id}`

export const tatibsUrl = () => '/api/tatib/tatibs'
export const tatibUrl = (id) => `/api/tatib/tatibs/${id}`
export const tatibItemsUrl = (tatibId) =>
  `/api/tatib/items?tatib=${tatibId}&ordering=order_number`
export const tatibItemsCreateUrl = () => '/api/tatib/items'
export const tatibItemUrl = (id) => `/api/tatib/items/${id}`
export const tatibItemsReorderUrl = () => '/api/tatib/items/reorder'
