"""Service entry forms and helpers (spec 006, slice 2).

One form per kind, because the modals are per kind. The model owns the rules
(``ServiceEntry.clean``); these forms only decide which fields a kind accepts and
turn a song's checked verses into the numbers the model stores. ``kind`` stays a
form field -- hidden, with the kind fixed -- because Django skips a field that is
not in ``Meta.fields`` during model validation, which would silently drop the
model's own rules (the lesson from spec 005).
"""

from django import forms
from django.core.exceptions import ValidationError

from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models
from multimedia.tatib.screen_breaks import line_shape

KINDS = {
    'text': tatib_models.ServiceEntryKind.TEXT,
    'scripture': tatib_models.ServiceEntryKind.SCRIPTURE,
    'song': tatib_models.ServiceEntryKind.SONG,
    'media': tatib_models.ServiceEntryKind.MEDIA,
    'fill_in': tatib_models.ServiceEntryKind.FILL_IN,
    'choice': tatib_models.ServiceEntryKind.CHOICE,
}
"""The kinds that can be written. The section break is retired (spec 131): its stored rows
still render, project, reorder and delete, but no form is built for it, so every endpoint
answers `Unknown kind.` — the same refusal an unknown kind has always had."""


class ServiceEntryForm(forms.ModelForm):
    """What every kind shares: the hidden kind, the service, and saving.

    ``kind`` travels in the URL as a name ('scripture', 'section_break') because that
    is what the modals and the tests speak, and the view turns that name into a stored
    value before the form is built. The field itself speaks the model's own numbers --
    an edit form is bound to an instance whose ``kind`` is already stored, so its
    choices must be those values or every re-render rejects the entry it is editing.
    """

    kind = forms.TypedChoiceField(choices=tatib_models.ServiceEntryKind.choices,
                                  coerce=int, widget=forms.HiddenInput)

    class Meta:
        model = tatib_models.ServiceEntry
        fields = []
        widgets = {'kind': forms.HiddenInput}

    def __init__(self, *args, tatib=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tatib = tatib or (self.instance.tatib if self.instance.pk else None)
        if self.tatib is not None and not self.instance.pk:
            # The model's own rules read the Tata Ibadah (a slot is template-only), and
            # model validation runs before the form's save().
            self.instance.tatib = self.tatib

    def save(self, commit=True):
        entry = super().save(commit=False)
        if self.tatib is not None:
            entry.tatib = self.tatib
        if commit:
            entry.save()
        return entry


class TextEntryForm(ServiceEntryForm):
    default_screen_mode = forms.ChoiceField(choices=tatib_models.TextScreenMode.choices,
                                            required=False, widget=forms.HiddenInput)

    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'title', 'text', 'default_screen_mode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_line_shape = (line_shape(self.instance.text)
                                    if self.instance.pk else None)
        if self.instance.pk:
            self.fields['default_screen_mode'].disabled = True

    def clean_default_screen_mode(self):
        if self.instance.pk:
            return self.instance.default_screen_mode
        return self.cleaned_data['default_screen_mode'] or tatib_models.TextScreenMode.MULTI_LINE

    def save(self, commit=True):
        entry = super().save(commit=False)
        if (entry.kind == tatib_models.ServiceEntryKind.TEXT
                and entry.screen_breaks is not None
                and self.original_line_shape != line_shape(entry.text)):
            entry.screen_breaks = None
            entry.screen_breaks_reset = True
        if commit:
            entry.save()
        return entry


class RangeCheckedModelChoiceField(forms.ModelChoiceField):
    """Reject primary keys outside the database field's range before querying."""

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, self.queryset.model):
            value = value.pk
        pk_field = self.queryset.model._meta.pk
        try:
            pk = pk_field.to_python(value)
            pk_field.run_validators(pk)
        except (TypeError, ValueError, OverflowError, ValidationError) as exc:
            raise ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            ) from exc
        return super().to_python(pk)


class ScriptureEntryForm(ServiceEntryForm):
    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'book_translation', 'chapter', 'verse_start', 'verse_end']
        field_classes = {'book_translation': RangeCheckedModelChoiceField}


class SongEntryForm(ServiceEntryForm):
    """The verses are the song's own numbers; what is stored is the ones included."""

    verses = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'song', 'verses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        song_queryset = song_models.Song.objects.active().filter(book__is_deleted=False)
        if self.instance.pk and self.instance.song_id:
            song_queryset |= song_models.Song.objects.filter(pk=self.instance.song_id)
        self.fields['song'].queryset = song_queryset
        self.song = self._chosen_song()
        numbers = list(self.song.verse_set.filter(is_deleted=False)
                       .order_by('number').values_list('number', flat=True)) if self.song else []
        if self.instance.pk and self.instance.song_id == getattr(self.song, 'pk', None):
            numbers = sorted(set(numbers) | set(self.instance.verses or []))
        self.fields['verses'].choices = [(n, str(n)) for n in numbers]

    def _chosen_song(self):
        if self.is_bound:
            chosen = self.data.get('song')
        else:
            chosen = getattr(self.instance, 'song_id', None)
        return self.fields['song'].queryset.filter(pk=chosen).first() if chosen else None

    @property
    def song_has_no_verses(self):
        """A song is picked and it carries no verses at all (spec 162).

        The field's only other "nothing here" state is no song picked, and the two must not
        read alike; this is the one of them the server can be wrong about, because the
        fragment it renders already names the song.
        """
        return self.song is not None and not self.fields['verses'].choices

    def clean_verses(self):
        return sorted(int(number) for number in self.cleaned_data.get('verses') or [])

    def save(self, commit=True):
        entry = super().save(commit=False)          # the base saves; this field is ours
        entry.verses = self.cleaned_data.get('verses') or []
        if commit:
            entry.save()
        return entry


class MediaEntryForm(ServiceEntryForm):
    """An edit can rename the entry, never point it at different bytes."""

    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'title', 'media', 'media_filename']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['kind'].disabled = True
            self.fields['media'].disabled = True
            self.fields['media_filename'].disabled = True

    def clean_kind(self):
        if self.cleaned_data['kind'] != tatib_models.ServiceEntryKind.MEDIA:
            raise ValidationError('This entry must remain a media entry.')
        return self.cleaned_data['kind']

    def clean_media_filename(self):
        value = self.cleaned_data['media_filename']
        if '/' in value or '\\' in value:
            raise ValidationError('A plain filename is required.')
        return value


class SlotForm(ServiceEntryForm):
    """A fill-in or a choice: a title and the kind it will resolve to (spec 167).

    Both kinds hold no content; the difference is what generation does with them -- a
    fill-in becomes the entry the operator picks, a choice becomes one of its options.
    """

    # Text is the default the preview shows selected: a slot always has a kind, and the
    # form must never open with none of the four pressed.
    fill_kind = forms.TypedChoiceField(choices=tatib_models.SlotKind.choices, coerce=int,
                                       initial=tatib_models.SlotKind.TEXT,
                                       widget=forms.HiddenInput)

    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'title', 'fill_kind']

    def clean(self):
        cleaned = super().clean()
        if self.tatib is not None and self.tatib.kind != tatib_models.TataIbadahKind.TEMPLATE:
            raise ValidationError('A fill-in or a choice exists only on a template.')
        return cleaned


class FillInEntryForm(SlotForm):
    pass


class ChoiceEntryForm(SlotForm):
    pass


FORMS = {
    'text': TextEntryForm,
    'scripture': ScriptureEntryForm,
    'song': SongEntryForm,
    'media': MediaEntryForm,
    'fill_in': FillInEntryForm,
    'choice': ChoiceEntryForm,
}


TITLES = {
    'text': 'text', 'scripture': 'passage',
    'song': 'song', 'media': 'media',
    'fill_in': 'fill-in', 'choice': 'choice',
}

SLOT_LABELS = {
    'text': 'Text', 'scripture': 'Passage', 'song': 'Song', 'media': 'Media',
}


def entry_title(kind, entry=None):
    """What the modal says at the top: 'New passage', 'Edit song', ..."""
    what = TITLES.get(kind, kind)
    return f'Edit {what}' if entry is not None else f'New {what}'


def kind_name(value):
    """The URL's name for a stored kind value ('section_break', 'song', ...)."""
    return tatib_models.ServiceEntryKind(value).name.lower()


def kind_from_post(value):
    """The URL name for what the form posted, which is the model's own value."""
    try:
        return kind_name(int(value))
    except (TypeError, ValueError):
        return None


def build_entry_form(kind, data=None, instance=None, tatib=None):
    """The form for a kind, or None when the kind is not one of ours."""
    form_class = FORMS.get(kind)
    if form_class is None:
        return None
    form = form_class(data=data, instance=instance, tatib=tatib)
    form.fields['kind'].initial = KINDS[kind]     # the URL names the kind; the field stores it
    return form


def next_order_number(tatib):
    """The next number after both old rows and entries in the shared order."""
    last_legacy = (tatib.tataibadahitem_set.order_by('-order_number')
                   .values_list('order_number', flat=True).first() or 0)
    last_entry = (tatib.service_entries.order_by('-order_number')
                  .values_list('order_number', flat=True).first() or 0)
    return max(last_legacy, last_entry) + 1


def scripture_books(selected_translation_pk=None):
    """The books, with the chapter count the modal needs to fill the next dropdown."""
    from multimedia.bible import models as bible_models
    from multimedia.web.reading import search as search_lib

    selected_translation = None
    selected_pk = None
    if selected_translation_pk not in (None, ''):
        pk_field = bible_models.BookTranslation._meta.pk
        try:
            selected_pk = pk_field.to_python(selected_translation_pk)
            pk_field.run_validators(selected_pk)
        except (TypeError, ValueError, OverflowError, ValidationError):
            selected_pk = None
    if selected_pk is not None:
        selected_translation = (bible_models.BookTranslation.objects
                                .only('pk', 'book_id', 'translation')
                                .filter(pk=selected_pk).first())

    rows = []
    for info in search_lib.bible_book_index().values():
        translations = info['by_version']
        tb = translations.get('TB')
        sim = translations.get('SIM')
        primary = tb or next(iter(translations.values()), None)
        if primary is None:
            continue
        selected = (selected_translation
                    if selected_translation and selected_translation.book_id == info['book'].pk
                    else None)
        rows.append({
            'id': primary.pk,
            'tb_id': tb.pk if tb else None,
            'sim_id': sim.pk if sim else None,
            'tb_name': tb.translation if tb else info['display'],
            'sim_name': sim.translation if sim else '',
            'tb_abbr': info['book'].name,
            'sim_abbr': (sim.abbreviation or info['book'].name) if sim else info['book'].name,
            'testament': info['book'].testament,
            'display': info['display'],
            'other': info['other'],
            'testament_label': ('Perjanjian Lama' if info['book'].testament == 'old'
                                else 'Perjanjian Baru'),
            'testament_sim_label': ('Padan na Basaia' if info['book'].testament == 'old'
                                    else 'Padan na Baru'),
            'chapters': info['book'].number_of_chapters,
            'selected': selected is not None,
            'selected_translation_id': selected.pk if selected else None,
            'selected_translation_name': selected.translation if selected else '',
            'selected_translation_is_primary': selected is not None and selected.pk == primary.pk,
            'selected_translation_is_sim': selected is not None and sim is not None
                                          and selected.pk == sim.pk,
            'selected_edition': 'sim' if selected is not None and sim is not None
                                and selected.pk == sim.pk else 'tb',
        })
    return rows


def chapter_verse_numbers(translation_pk, chapter):
    from multimedia.bible import models as bible_models
    return list(bible_models.Verse.objects.filter(
        book_translation_id=translation_pk, chapter=chapter)
        .order_by('verse').values_list('verse', flat=True))


def chapter_verse_count(translation_pk, chapter):
    return len(chapter_verse_numbers(translation_pk, chapter))
