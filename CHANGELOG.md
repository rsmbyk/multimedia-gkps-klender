# Changelog

---

## Version `0.4.2`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b1`
- Songs: `v0.4.s8`
- Tatib: `v0.4.t8`
- Project: `v0.4.p0`

### Changes

- `[b1, s5, t5]` Added an option to skip the toggle action when toggling a ToggleButton.
- `[s6, t6]` The status broadcast message that is forwarded to the Subject will now forward the whole object instead of the status value only.
- `[s7, t7]` The display tab will not re-broadcast the status message upon receiving a status broadcast message anymore.
- `[s8, t8]` Added an option to not notify the Subject when sending status broadcast message.
- `[p0]` Added a new app: `project` to show a full screen display of lyrics and tatib (and passage possibly in the future) texts. 

---

## Version `0.4.1 Hotfix`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b0`
- Songs: `v0.4.s4`
- Tatib: `v0.4.t4`

### Hotfix Changes

- `[s4]` The displayed lyrics will be set to empty string upon reaching last lyric.

---

## Version `0.4`

### App Versions

- Django: `v0.4.dj1`
- Bible: `v0.4.b0`
- Songs: `v0.4.s3`
- Tatib: `v0.4.t4`

### Changes

- `[s1]` Added two display modes (Box and Outline DisplayModes) to use in Options.
- `[dj1, t1]` Added buttons to insert TatibItems right after a specific item.
- `[t2]` The page will now scroll to the last (detected) position before refreshing the TatibItem list.
- `[s2, t3]` The PreviewSegment in web will now be closed when trying to do other actions.
- `[s3, t4]` Added a PreviewSegment into the EditModals in Web that shows live preview of the currently edited items.

---

## Version `0.3.9`

### App Versions

- Django: `v0.3.dj3`
- Bible: `v0.3.b18`
- Songs: `v0.3.s42`
- Tatib: `v0.3.t19`

### Changes

- `[t16]` Title/Header-like can now be added to TataIbadahItem to provide additional text/info to the screen.
- `[s40, t17]` Fixed the scaling of Web Preview font-size.
- `[s41, t18]` Added a Button(s) to navigate back to the root URL of the web.
- `[s42, t19]` The top layout of some pages in the web is now in fixed position to improve the QoL when navigating around and/or editing Songs/TataIbadahItems.

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
