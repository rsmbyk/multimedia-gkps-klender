"""Forms for editing the original TataIbadahItem rows (spec 007, slice 1)."""

from django import forms

from multimedia.tatib import models as tatib_models


class LegacyItemForm(forms.ModelForm):
    """Edit only the content fields supported by the stored legacy row kind."""

    class Meta:
        model = tatib_models.TataIbadahItem
        fields = ['title', 'text']
        widgets = {'text': forms.Textarea(attrs={'rows': 6})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.item_type == tatib_models.TataIbadahItemType.END_OF_SECTION:
            self.fields.pop('title')
            self.fields['text'].label = 'Note'
            self.fields['text'].required = False
        for field_name in self.errors:
            self.fields[field_name].widget.attrs['aria-invalid'] = 'true'

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if (self.instance.item_type == tatib_models.TataIbadahItemType.TEXT
                and not text.strip()):
            raise forms.ValidationError('Text is required.')
        return text


def kind_name(item):
    if item.item_type == tatib_models.TataIbadahItemType.END_OF_SECTION:
        return 'end_of_section'
    return 'text'
