from django.core.exceptions import ValidationError
from django.db import models

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models


class TataIbadahKind(models.IntegerChoices):
    """A service is dated and projects; a template is dated never and generates (spec 167)."""

    SERVICE = 0
    TEMPLATE = 1


class TataIbadah(models.Model):
    name = models.CharField(max_length=64)
    kind = models.SmallIntegerField(choices=TataIbadahKind.choices,
                                    default=TataIbadahKind.SERVICE)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date', '-created_at')
        constraints = [models.CheckConstraint(
            check=(models.Q(kind=TataIbadahKind.SERVICE, date__isnull=False)
                   | models.Q(kind=TataIbadahKind.TEMPLATE, date__isnull=True)),
            name='tatib_kind_matches_date')]

    def clean(self):
        errors = self._type_errors()
        if errors:
            raise ValidationError(errors)

    def _type_errors(self):
        errors = {}
        if self.kind == TataIbadahKind.TEMPLATE and self.date is not None:
            errors['date'] = 'A template has no date.'
        if self.kind == TataIbadahKind.SERVICE and self.date is None:
            errors['date'] = 'A normal Tata Ibadah needs a date.'
        if not self._state.adding and self.pk:
            stored = (type(self).objects.filter(pk=self.pk)
                      .values_list('kind', flat=True).first())
            if stored is not None and stored != self.kind:
                errors['kind'] = 'A Tata Ibadah never changes its type.'
        return errors

    def save(self, *args, **kwargs):
        """The type is chosen once. A writer that has no word for it keeps the old rule:
        a create with no date is a template, so the API and the old editors stay correct."""
        if self._state.adding:
            if self.date is None:
                self.kind = TataIbadahKind.TEMPLATE
        else:
            errors = self._type_errors()
            if errors:
                raise ValidationError(errors)
        super().save(*args, **kwargs)



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


class MediaShare(models.Model):
    """Temporary R2 copy of one immutable media identity."""

    media = models.OneToOneField(MediaIdentity, models.CASCADE, primary_key=True,
                                 related_name='share')
    object_key = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default='pending')
    completion_token_hash = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.CheckConstraint(
            check=models.Q(status__in=['pending', 'available']),
            name='media_share_valid_status')]


class ServiceEntryKind(models.IntegerChoices):
    TEXT = 0
    SCRIPTURE = 1
    SONG = 2
    SECTION_BREAK = 3
    MEDIA = 4
    FILL_IN = 5, 'Fill-in'
    CHOICE = 6, 'Choice'


class SlotKind(models.IntegerChoices):
    """What a fill-in or a choice resolves to: the four kinds an operator can add."""

    TEXT = 0
    SCRIPTURE = 1
    SONG = 2
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

    # song: the verse IDs this entry includes, stored explicitly (IDs, not numbers,
    # so a reorder changes the displayed number but never the reference — spec 189 FR-008).
    song = models.ForeignKey(song_models.Song, models.PROTECT, null=True, blank=True)
    verses = models.JSONField(default=list, blank=True)

    def verse_numbers(self):
        """Current numbers of the referenced verses, in number order (FR-008)."""
        if not self.song_id:
            return []
        verses = (self.song.verse_set.filter(pk__in=self.verses or [], is_deleted=False)
                  .order_by('number'))
        return [verse.number for verse in verses]

    def verse_lines(self):
        """Lyrics of the referenced verses in current-number order."""
        if not self.song_id:
            return []
        verses = (self.song.verse_set.filter(pk__in=self.verses or [], is_deleted=False)
                  .order_by('number'))
        return [verse.lyric for verse in verses]

    # Media bytes remain on the operator computer; the service keeps identity and label.
    media = models.ForeignKey(MediaIdentity, models.PROTECT, null=True, blank=True)
    media_filename = models.CharField(max_length=255, blank=True)

    # A slot (spec 167): a fill-in or a choice lives on a template, names the kind it will
    # resolve to, and holds no content of its own. A choice's options are ordinary entries
    # of that kind, each pointing back at the choice through ``parent``.
    fill_kind = models.SmallIntegerField(choices=SlotKind.choices, null=True, blank=True)
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True,
                               related_name='options')


    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('tatib', 'order_number')

    def __str__(self):
        return f'{self.tatib}: {self.order_number} ({self.get_kind_display()})'

    def clean(self):
        errors = {}
        if self.kind in (ServiceEntryKind.FILL_IN, ServiceEntryKind.CHOICE):
            errors.update(self._slot_errors())
        elif self.parent_id:
            errors.update(self._option_errors())
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
                # Two causes, two sentences: a song with nothing in it cannot be brought
                # into the service at all, which is not the same as clearing its boxes.
                if self.song.verse_set.filter(is_deleted=False).exists():
                    errors['verses'] = 'Keep at least one verse in the service.'
                else:
                    errors['verses'] = 'This song has no verses: pick another song.'
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

    def _slot_errors(self):
        """A fill-in or a choice: a template's word for work still to come (spec 167)."""
        errors = {}
        if not self.tatib_id or self.tatib.kind != TataIbadahKind.TEMPLATE:
            errors['kind'] = 'A fill-in or a choice exists only on a template.'
        if self.fill_kind is None:
            errors['fill_kind'] = 'Choose the kind this entry resolves to.'
        if self.parent_id:
            errors['parent'] = 'A fill-in or a choice cannot be an option.'
        if ((self.text or '').strip() or self.song_id or self.book_translation_id
                or self.media_id or (self.media_filename or '').strip()):
            errors['text'] = 'A fill-in holds no content of its own.'
        return errors

    def _option_errors(self):
        """An option is an ordinary entry of its choice's kind, in the same Tata Ibadah."""
        errors = {}
        parent = self.parent
        if parent.kind != ServiceEntryKind.CHOICE:
            errors['parent'] = "Only a choice holds options."
        elif parent.tatib_id != self.tatib_id:
            errors['parent'] = "An option belongs to its choice's Tata Ibadah."
        elif self.kind != parent.fill_kind:
            errors['kind'] = 'An option must be the kind its choice resolves to.'
        if self.fill_kind is not None:
            errors['fill_kind'] = 'An option is an ordinary entry.'
        return errors

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
        if self.kind in (ServiceEntryKind.FILL_IN, ServiceEntryKind.CHOICE):
            # A slot never projects -- it only ever appears on a template's page.
            return self.title, ''
        return self.title, self.text

    @property
    def target_deleted(self):
        if self.kind != ServiceEntryKind.SONG or not self.song_id:
            return False
        song = self.song
        return (song.is_deleted or song.book.is_deleted
                or song.verse_set.filter(pk__in=self.verses or [], is_deleted=True).exists())

    def _scripture_body(self):
        verses = (bible_models.Verse.objects
                  .filter(book_translation_id=self.book_translation_id,
                          chapter=self.chapter,
                          verse__gte=self.verse_start or 1,
                          verse__lte=self.verse_end or self.verse_start or 0)
                  .order_by('verse'))
        return '\n\n'.join(f'{v.verse} {v.text}'.strip() for v in verses)

    def _song_body(self):
        verses = (self.song.verse_set.filter(pk__in=self.verses or [], is_deleted=False)
                  .order_by('number'))
        return '\n\n'.join((v.lyric or '').strip() for v in verses)
