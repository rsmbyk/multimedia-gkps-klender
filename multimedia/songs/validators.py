from django.core import validators

import multimedia.songs.models


class BookShortNameUniqueValidator(validators.BaseValidator):
    message = 'This short name has already been used.'
    code = 'unique_book_short_name'

    def __init__(self, check_blank_value=False):
        super().__init__(check_blank_value)

    def compare(self, a, b):
        if not b and len(a) == 0:
            return False
        return multimedia.songs.models.Book.objects.filter(short_name=a).count() > 0
