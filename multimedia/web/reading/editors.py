"""Sidebar editors (spec 005).

Forms for the three records the reading sidebars own, plus the helpers the editor
endpoints use. The rules mirror the models' own constraints rather than inventing
looser ones; hymn songbooks and their songs are not editable, which the views
enforce as well as the templates.
"""

from django import forms
from django.conf import settings

from multimedia.songs import models as song_models
from multimedia.songs.validators import BookShortNameUniqueValidator
from multimedia.tatib import models as tatib_models

EDITOR_KINDS = ('songbook', 'song', 'tatib')

ADD_LABEL = {'songbook': 'Add songbook', 'song': 'Add song', 'tatib': 'Add Tata Ibadah'}
CREATE_TITLE = {'songbook': 'New songbook', 'song': 'New song', 'tatib': 'New Tata Ibadah'}
EDIT_TITLE = {'songbook': 'Edit songbook', 'song': 'Edit song', 'tatib': 'Edit Tata Ibadah'}


def editors_allowed(request):
    """spec 005: the owner's decision is that anyone may write; the hook can change it."""
    if not getattr(settings, 'SIDEBAR_EDITORS_REQUIRE_LOGIN', False):
        return True
    return bool(request.user.is_authenticated and request.user.is_staff)


class SongbookForm(forms.ModelForm):
    class Meta:
        model = song_models.Book
        fields = ['name', 'short_name', 'lang', 'is_hymn_book']
        labels = {'lang': 'Language', 'is_hymn_book': 'Hymn book (its songs stay read-only)'}
        error_messages = {
            'unique_together': 'That songbook already exists for this language.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The model's validator counts every row, so keeping an existing short
        # name on an edit would be rejected. Re-check instance-aware instead.
        field = self.fields['short_name']
        field.validators = [v for v in field.validators
                            if not isinstance(v, BookShortNameUniqueValidator)]

    def _get_validation_exclusions(self):
        # the model's validator counts every row, so keep it out of the instance
        # validation as well; clean_short_name re-checks instance-aware below
        exclude = super()._get_validation_exclusions()
        exclude.append('short_name')
        return exclude

    def clean_short_name(self):
        value = (self.cleaned_data.get('short_name') or '').strip()
        if value:
            clash = song_models.Book.objects.filter(short_name=value)
            if self.instance.pk:
                clash = clash.exclude(pk=self.instance.pk)
            if clash.exists():
                raise forms.ValidationError('This short name has already been used.')
        return value


class SongForm(forms.ModelForm):
    class Meta:
        model = song_models.Song
        fields = ['number', 'sub_number', 'title', 'key']

    def __init__(self, *args, book=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = book or (self.instance.book if self.instance.pk else None)
        if self.book is not None:
            self.instance.book = self.book
            if self.instance.pk is None:
                # A new song carries its songbook with the POST (the create URL's
                # query string does not survive the submit); an edit has it from the
                # instance. Not a Meta field, so the model's unique_together check is
                # skipped -- clean() re-checks the trio instance-aware below.
                self.fields['book'] = forms.IntegerField(
                    widget=forms.HiddenInput, initial=self.book.pk, required=False)
        if self.is_hymn:
            self.fields['number'].required = True
            self.fields['number'].help_text = 'Required: a hymn is identified by its number.'
        else:
            self.fields['number'].help_text = 'Leave empty for a song without a number.'

    @property
    def is_hymn(self):
        return bool(self.book is not None and self.book.is_hymn_book)

    def clean(self):
        cleaned = super().clean()
        if self.book is None:
            raise forms.ValidationError('Choose a songbook first.')
        if self.is_hymn and cleaned.get('number') is None:
            self.add_error('number', 'A hymn needs a number.')
        number = cleaned.get('number')
        if number is not None and self.book is not None:
            clash = song_models.Song.objects.filter(
                book=self.book, number=number, sub_number=cleaned.get('sub_number') or '')
            if self.instance.pk:
                clash = clash.exclude(pk=self.instance.pk)
            if clash.exists():
                self.add_error('number', 'That number is already taken in this songbook.')
        return cleaned


class TataIbadahForm(forms.ModelForm):
    first_title = forms.CharField(required=False, max_length=64, label='First section title')
    first_text = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows': 4}), label='First section text')

    class Meta:
        model = tatib_models.TataIbadah
        fields = ['name', 'date', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # sections are not edited here
            self.fields.pop('first_title')
            self.fields.pop('first_text')
        else:
            self.fields['date'].help_text = (
                'Leave empty for a recurring template (shown under Templates).')
            self.fields['first_title'].help_text = (
                'A service appears in the lists once it has a section.')


def build_form(kind, request, pk=None, data=None):
    """The form for one kind, or None when the kind or target is not editable.

    Returns ``(form, target)`` where target is the record being edited (None for
    a new record, or the songbook a new song belongs to).
    """
    if kind not in EDITOR_KINDS:
        return None, None
    query = data if data is not None else request.GET
    if kind == 'songbook':
        instance = _record(song_models.Book, pk) if pk else None
        if instance is not None and instance.is_hymn_book:
            return None, None                    # hymn songbooks are read-only
        return SongbookForm(data=data, instance=instance), instance
    if kind == 'tatib':
        instance = _record(tatib_models.TataIbadah, pk) if pk else None
        return TataIbadahForm(data=data, instance=instance), instance
    # song: the songbook comes from the instance, or from the request
    if pk:
        song = _record(song_models.Song, pk)
        if song is None or song.book.is_hymn_book:
            return None, None                    # a hymn's songs are read-only
        return SongForm(data=data, instance=song), song
    book_id = query.get('book')
    book = _record(song_models.Book, book_id) if book_id else None
    if book is None:
        return None, None
    return SongForm(data=data, book=book), book


def _record(model, pk):
    try:
        return model.objects.get(pk=pk)
    except (model.DoesNotExist, ValueError, TypeError):
        return None


def save_form(kind, form, target):
    """Persist a valid form; returns the saved object.

    A new Tata Ibadah also gets its optional first section, because the public
    lists only show services that have one -- without it the service would be
    saved but invisible, which reads as a failed save.
    """
    obj = form.save()
    if kind == 'tatib' and target is None:
        title = (form.cleaned_data.get('first_title') or '').strip()
        text = (form.cleaned_data.get('first_text') or '').strip()
        if title or text:
            tatib_models.TataIbadahItem.objects.create(
                tatib=obj, item_type=tatib_models.TataIbadahItemType.TEXT,
                title=title, text=text, order_number=1)
    return obj


def form_title(kind, pk):
    return EDIT_TITLE[kind] if pk else CREATE_TITLE[kind]
