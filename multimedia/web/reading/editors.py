"""Sidebar editors (spec 005).

Forms for the three records the reading sidebars own, plus the helpers the editor
endpoints use. The rules mirror the models' own constraints rather than inventing
looser ones; hymn songbooks and their songs are not editable, which the views
enforce as well as the templates.
"""

from django import forms
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS

from multimedia.songs import models as song_models
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
        fields = ['name', 'lang']
        labels = {'lang': 'Language'}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'That songbook already exists for this language.',
            },
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = song_models.Song
        fields = ['title']

    def __init__(self, *args, book=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = book or (self.instance.book if self.instance.pk else None)
        if self.book is not None:
            self.instance.book = self.book


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
        if pk and instance is None:
            return None, None
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
    if book is None or book.is_hymn_book:
        return None, None                    # a hymn's songs are read-only, added or not
    return SongForm(data=data, book=book), book


def _record(model, pk):
    try:
        records = model.objects
        if model is song_models.Book:
            records = records.active()
        elif model is song_models.Song:
            records = records.active().filter(book__is_deleted=False)
        return records.get(pk=pk)
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
