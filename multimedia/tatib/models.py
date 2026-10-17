from django.core.exceptions import ValidationError
from django.db import models

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models


class TataIbadah(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date', '-created_at')


class TataIbadahItemType(models.IntegerChoices):
    TEXT = 0
    END_OF_SECTION = 1


class TataIbadahItem(models.Model):
    tatib = models.ForeignKey(TataIbadah, models.PROTECT)
    item_type = models.IntegerField(choices=TataIbadahItemType.choices)
    title = models.CharField(max_length=64, blank=True)
    text = models.TextField(blank=True)

    order_number = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.tatib}: {self.order_number}'

    class Meta:
        ordering = ('tatib', 'order_number')


class MediaFamily(models.TextChoices):
    IMAGE = 'image', 'Image'
    AUDIO = 'audio', 'Audio'
    VIDEO = 'video', 'Video'
    PDF = 'pdf', 'PDF'
    POWERPOINT = 'slides', 'PowerPoint'


class MediaIdentity(models.Model):
    """Server-side identity only; file bytes live in an operator's local library."""

    sha256 = models.CharField(max_length=64, primary_key=True)
    byte_count = models.PositiveIntegerField()
    family = models.CharField(max_length=6, choices=MediaFamily.choices)
    display_filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def clean(self):
        import re
        errors = {}
        if not re.fullmatch(r'[0-9a-f]{64}', self.sha256 or ''):
            errors['sha256'] = 'A complete SHA-256 fingerprint is required.'
        if not self.byte_count or self.byte_count > 200_000_000:
            errors['byte_count'] = 'A media file must be between 1 byte and 200 MB.'
        if not self.display_filename or '/' in self.display_filename or '\\' in self.display_filename:
            errors['display_filename'] = 'A plain filename is required.'
        if errors:
            raise ValidationError(errors)


class ServiceEntryKind(models.IntegerChoices):
    TEXT = 0
    SCRIPTURE = 1
    SONG = 2
    SECTION_BREAK = 3
    MEDIA = 4


class TextScreenMode(models.TextChoices):
    MULTI_LINE = 'multi_line', 'Multi-line'
    SINGLE_SCREEN = 'single_screen', 'Single-screen'


class ServiceEntry(models.Model):
    """One ordered element of a service order (spec 006).

    Lives beside the legacy ``TataIbadahItem``: a text, a passage, a song or a section
    break. Whatever the kind, ``resolve()`` answers the ``(title, body)`` pair the
    display renders, so nothing downstream has to know which kind it is showing.
    Bodies separate their blocks with a blank line -- the display side turns a body
    into lines, and the blank line is the operator's pause.
    """

    tatib = models.ForeignKey(TataIbadah, models.PROTECT, related_name='service_entries')
    kind = models.IntegerField(choices=ServiceEntryKind.choices)
    order_number = models.PositiveIntegerField()

    # text, and the label of a section break
    title = models.CharField(max_length=64, blank=True)
    text = models.TextField(blank=True)

    default_screen_mode = models.CharField(max_length=13, choices=TextScreenMode.choices,
                                           default=TextScreenMode.MULTI_LINE)
    # None uses the saved default: paired lines or one fitted screen.
    # A list holds custom boundaries after 1-based raw text lines.
    screen_breaks = models.JSONField(null=True, blank=True, default=None)
    screen_breaks_reset = models.BooleanField(default=False)

    # scripture
    book_translation = models.ForeignKey(bible_models.BookTranslation, models.PROTECT,
                                         null=True, blank=True)
    chapter = models.PositiveIntegerField(null=True, blank=True)
    verse_start = models.PositiveIntegerField(null=True, blank=True)
    verse_end = models.PositiveIntegerField(null=True, blank=True)

    # song: the verse numbers this entry includes, stored explicitly, so a verse
    # added to the song later has to be added to the service deliberately
    song = models.ForeignKey(song_models.Song, models.PROTECT, null=True, blank=True)
    verses = models.JSONField(default=list, blank=True)

    # Media bytes remain on the operator computer; the service keeps identity and label.
    media = models.ForeignKey(MediaIdentity, models.PROTECT, null=True, blank=True)
    media_filename = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('tatib', 'order_number')

    def __str__(self):
        return f'{self.tatib}: {self.order_number} ({self.get_kind_display()})'

    def clean(self):
        errors = {}
        if self.screen_breaks is not None:
            from multimedia.tatib.screen_breaks import valid_breaks
            if self.kind != ServiceEntryKind.TEXT or not valid_breaks(
                    self.text, self.screen_breaks,
                    single_screen=self.default_screen_mode == TextScreenMode.SINGLE_SCREEN):
                errors['screen_breaks'] = 'Screen breaks must fall between text lines.'
        if self.kind == ServiceEntryKind.TEXT and not (self.text or '').strip():
            errors['text'] = 'A text entry needs its text.'
        if self.kind == ServiceEntryKind.SCRIPTURE:
            if not self.book_translation_id or not self.chapter or not self.verse_start:
                errors['chapter'] = 'A passage needs a book, a chapter and a starting verse.'
            elif self.verse_end and self.verse_end < self.verse_start:
                errors['verse_end'] = 'The ending verse cannot come before the starting one.'
        if self.kind == ServiceEntryKind.SONG:
            if not self.song_id:
                errors['song'] = 'A song entry needs a song.'
            elif not self.verses:
                errors['verses'] = 'Keep at least one verse in the service.'
        if self.kind == ServiceEntryKind.MEDIA:
            if not self.media_id:
                errors['media'] = 'A media entry needs a file reference.'
            if not self.media_filename:
                errors['media_filename'] = 'A media entry needs a filename.'
            if self.pk:
                saved = type(self).objects.filter(pk=self.pk).values(
                    'media_id', 'media_filename').first()
                if saved and (saved['media_id'] != self.media_id
                              or saved['media_filename'] != self.media_filename):
                    errors['media'] = 'The file reference cannot change after creation.'
        elif self.pk and type(self).objects.filter(pk=self.pk, kind=ServiceEntryKind.MEDIA).exists():
            errors['kind'] = 'A media entry cannot change its kind after creation.'
        if errors:
            raise ValidationError(errors)

    def citation(self):
        """The heading a person would read out for this entry."""
        if self.kind == ServiceEntryKind.SCRIPTURE:
            name = self.book_translation.translation if self.book_translation_id else ''
            span = f'{self.chapter}:{self.verse_start}'
            if self.verse_end and self.verse_end != self.verse_start:
                span = f'{span}-{self.verse_end}'
            return f'{name} {span}'.strip()
        if self.kind == ServiceEntryKind.SONG and self.song_id:
            song, book = self.song, self.song.book
            if book.is_hymn_book and song.number is not None:
                # A hymn song reads by its short reference and title (spec 054);
                # no title leaves the short reference alone.
                return f'{song.book_number} — {song.title}' if song.title else song.book_number
            if song.number is not None:
                return f'{book.name} {song.number}{(song.sub_number or "").upper()}'
            return song.title or book.name
        if self.kind == ServiceEntryKind.MEDIA:
            return self.title or self.media_filename
        return self.title

    def resolve(self):
        """The ``(title, body)`` pair the display consumes, per kind."""
        if self.kind == ServiceEntryKind.SCRIPTURE:
            return self.citation(), self._scripture_body()
        if self.kind == ServiceEntryKind.SONG:
            return self.citation(), self._song_body()
        if self.kind == ServiceEntryKind.SECTION_BREAK:
            return '', ''
        if self.kind == ServiceEntryKind.MEDIA:
            return self.citation(), ''
        return self.title, self.text

    @property
    def target_deleted(self):
        if self.kind != ServiceEntryKind.SONG or not self.song_id:
            return False
        song = self.song
        return (song.is_deleted or song.book.is_deleted
                or song.verse_set.filter(number__in=self.verses or [], is_deleted=True).exists())

    def _scripture_body(self):
        verses = (bible_models.Verse.objects
                  .filter(book_translation_id=self.book_translation_id,
                          chapter=self.chapter,
                          verse__gte=self.verse_start or 1,
                          verse__lte=self.verse_end or self.verse_start or 0)
                  .order_by('verse'))
        return '\n\n'.join(f'{v.verse} {v.text}'.strip() for v in verses)

    def _song_body(self):
        verses = (self.song.verse_set.filter(number__in=self.verses or [], is_deleted=False)
                  .order_by('number'))
        return '\n\n'.join((v.lyric or '').strip() for v in verses)
