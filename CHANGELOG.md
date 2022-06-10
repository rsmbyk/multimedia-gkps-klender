# Changelog

---

## Version `0.3.8`

### App Versions

- Django: `v0.3.dj3`
- Bible: `v0.3.b18`
- Songs: `v0.3.s39`
- Tatib: `v0.3.t15`

### Changes

- `[s37]` NKB (Nyanyikanlah Kidung Baru) hymn book is now available.
- `[s38, t15]` Song's Verse and TataIbadahItem can now be previewed in the web by clicking the preview button (black eye icon).
- `[s39]` Deleted Bookmarks can now be viewed and restored to be used again.
- `[dj3]` Added and updated some Django Model Admins.

---

## Version `0.3.7`

### App Versions

- Django: `v0.3.dj2`
- Bible: `v0.3.b18`
- Songs: `v0.3.s36`
- Tatib: `v0.3.t14`

### Changes

- `[b12, s26, t1]` Added an indicator to indicate whether the Dock windows are being focused or not.
- `[b13, t2]` Added keyboard navigation support to Bible and Tatib dock.
- `[s27]` Fixed wrapping issue on overflowing texts in songs' Source Segment.
- `[t3]` Added reorder functionality to Tatib web.
- `[s28]` Fixed not-working codes to check disabled buttons.
- `[b14, s29]` Changed indicator button's icon to cross.
- `[t4]` Changed tatib's tab icon to cross.
- `[b15, s30, t5]` Changed Dock's background colour.
- `[t6]` Changed tatib's colour theme to red.
- `[t7]` Fixed a bug where TatibItem not actually being posted to BroadcastChannel on changing active item index.
- `[t8]` Fixed tatib's web page title.
- `[t9]` Removed tatib's Source Segment's label.
- `[t10]` Removed unused codes.
- `[t11]` Fixed an error accessing Tatib's name when there is no active tab.
- `[b16, s31, t12]` Fixed a bug where the Dock keep updating StatusButton's indefinitely when opening multiple dock windows.
- `[s32]` Replaced ReplaySubject with BehaviorSubject.
- `[s33]` Added more infos in string representation of Bookmark model class.
- `[b17, s34, t13]` Fixed a bug where the Dock's display status not being updated when specifically refreshing the source.
- `[s35, t14]` Changed Paste Modal's positive button's text to "Display".
- `[b18, s36]` Reduced margins and paddings by a little.

---

## Version `0.3.6`

### App Versions

- Django: `v0.3.dj2`
- Songs: `v0.3.s25`
- Bible: `v0.3.b11`
- Tatib: `v0.3.t0`

### Changes

- `[s24, b10]` Reduced Source Segment's height by the following methods:
  - Reducing segment's padding.
  - Reducing divider's margin.
  - Changing label's size to big.
- `[s25, b11]` Added an option to change the colour of Source's Label Icon.
- `[t0]` Added a new app: Tatib

---

## Version `0.3.5`

### App Versions

- Django: `v0.3.dj2`
- Songs: `v0.3.s23`
- Bible: `v0.3.b9`

### Changes

- `[s12]` Increased Song's Title length limit to 64 characters.
- `[s13]` Added keyboard support to navigate through the song.
- `[s14, b5]` Added a QoL support to block texts in DisplayTab from being selected by cursor clicks.
- `[b6]` Added a title in HistoryTab.
- `[s15]` Allowed some common symbols to be used in SongBook's and Song's title.
- `[s16, b7]` Added exit transitions when deactivating source.
- `[s17]` Added Song info (BookNumber and Title) on PrevSongButton and NextSongButton popups.
- `[dj2, s18]` Added reorder functionality to BookmarkDetailModal
- `[s19]` Fixed an error when updating popup on PrevSongButton and NextSongButton on empty Bookmark (and no active Bookmark).
- `[s20, b8]` Added an option to change Text Colour of the source.
- `[s21]` Changed Text Size options value to be numerical (in pixels).
- `[s22, b9]` Fixed an issue in which the source displaying brief exit transition when reloading both the dock and source.
- `[s23]` Allowed the same song to be added multiple of times to the same Bookmark.

---

## Version 0.3.4

### Songs (v0.3.s11)

- [s11] Remove "disabled days of week" in Bookmark form.
