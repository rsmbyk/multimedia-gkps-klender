"""Service entry forms and helpers (spec 006, slice 2).

One form per kind, because the modals are per kind. The model owns the rules
(``ServiceEntry.clean``); these forms only decide which fields a kind accepts and
turn a song's checked verses into the numbers the model stores. ``kind`` stays a
form field -- hidden, with the kind fixed -- because Django skips a field that is
not in ``Meta.fields`` during model validation, which would silently drop the
model's own rules (the lesson from spec 005).
"""

from django import forms

from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models

KINDS = {
    'text': tatib_models.ServiceEntryKind.TEXT,
    'scripture': tatib_models.ServiceEntryKind.SCRIPTURE,
    'song': tatib_models.ServiceEntryKind.SONG,
    'section_break': tatib_models.ServiceEntryKind.SECTION_BREAK,
}


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

    def save(self, commit=True):
        entry = super().save(commit=False)
        if self.tatib is not None:
            entry.tatib = self.tatib
        if commit:
            entry.save()
        return entry


class TextEntryForm(ServiceEntryForm):
    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'title', 'text']


class SectionBreakEntryForm(ServiceEntryForm):
    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'title']


class ScriptureEntryForm(ServiceEntryForm):
    class Meta(ServiceEntryForm.Meta):
        fields = ['kind', 'book_translation', 'chapter', 'verse_start', 'verse_end']


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

    def clean_verses(self):
        return sorted(int(number) for number in self.cleaned_data.get('verses') or [])

    def save(self, commit=True):
        entry = super().save(commit=False)          # the base saves; this field is ours
        entry.verses = self.cleaned_data.get('verses') or []
        if commit:
            entry.save()
        return entry


FORMS = {
    'text': TextEntryForm,
    'section_break': SectionBreakEntryForm,
    'scripture': ScriptureEntryForm,
    'song': SongEntryForm,
}


TITLES = {
    'text': 'text', 'scripture': 'passage', 'song': 'song', 'section_break': 'break',
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


def scripture_books():
    """The books, with the chapter count the modal needs to fill the next dropdown."""
    from multimedia.bible import models as bible_models
    rows = []
    for translation in (bible_models.BookTranslation.objects
                        .select_related('book', 'version').order_by('book_id')):
        rows.append({'id': translation.pk, 'name': translation.translation,
                     'testament_label': ('Perjanjian Lama' if translation.book.testament == 'old'
                                         else 'Perjanjian Baru'),
                     'chapters': translation.book.number_of_chapters})
    return rows


def chapter_verse_numbers(translation_pk, chapter):
    from multimedia.bible import models as bible_models
    return list(bible_models.Verse.objects.filter(
        book_translation_id=translation_pk, chapter=chapter)
        .order_by('verse').values_list('verse', flat=True))


def chapter_verse_count(translation_pk, chapter):
    return len(chapter_verse_numbers(translation_pk, chapter))
