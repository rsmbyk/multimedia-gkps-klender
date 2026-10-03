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
    """What every kind shares: the hidden kind, the service, and saving."""

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
        self.song = self._chosen_song()
        numbers = list(self.song.verse_set.order_by('number').values_list('number', flat=True)) \
            if self.song else []
        self.fields['verses'].choices = [(n, str(n)) for n in numbers]

    def _chosen_song(self):
        if self.is_bound:
            chosen = self.data.get('song')
        else:
            chosen = getattr(self.instance, 'song_id', None)
        return song_models.Song.objects.filter(pk=chosen).first() if chosen else None

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


def kind_name(value):
    """The URL's name for a stored kind value ('section_break', 'song', ...)."""
    return tatib_models.ServiceEntryKind(value).name.lower()


def build_entry_form(kind, data=None, instance=None, tatib=None):
    """The form for a kind, or None when the kind is not one of ours."""
    form_class = FORMS.get(kind)
    if form_class is None:
        return None
    form = form_class(data=data, instance=instance, tatib=tatib)
    form.instance.kind = KINDS[kind]              # the kind is the URL's, not the post's
    return form


def next_order_number(tatib):
    """Where a new entry goes: after the last one in the service."""
    last = tatib.service_entries.order_by('-order_number').first()
    return (last.order_number if last else 0) + 1


def scripture_books():
    """The books, with the chapter count the modal needs to fill the next dropdown."""
    from multimedia.bible import models as bible_models
    rows = []
    for translation in (bible_models.BookTranslation.objects
                        .select_related('book', 'version').order_by('book_id')):
        rows.append({'id': translation.pk, 'name': translation.translation,
                     'chapters': translation.book.number_of_chapters})
    return rows


def chapter_verse_count(translation_pk, chapter):
    from multimedia.bible import models as bible_models
    return bible_models.Verse.objects.filter(
        book_translation_id=translation_pk, chapter=chapter).count()
