from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    lang = models.ForeignKey(Language, models.PROTECT)
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.lang})'


class Testament(models.TextChoices):
    OLD = 'old'
    NEW = 'new'


class Book(models.Model):
    name = models.CharField(max_length=4)
    testament = models.CharField(max_length=4, choices=Testament.choices)
    number_of_chapters = models.IntegerField()

    def __str__(self):
        return self.name


class BookTranslation(models.Model):
    version = models.ForeignKey(Version, models.PROTECT)
    book = models.ForeignKey(Book, models.PROTECT)
    translation = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.translation} ({self.version} : {self.book})'

    class Meta:
        unique_together = ('version', 'book', 'translation')


class Verse(models.Model):
    book_translation = models.ForeignKey(BookTranslation, models.PROTECT)
    chapter = models.IntegerField()
    verse = models.IntegerField()
    title = models.CharField(max_length=128, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.book_translation.translation} {self.chapter} : {self.verse}'

    class Meta:
        unique_together = ('book_translation', 'chapter', 'verse')
        ordering = ('book_translation', 'chapter', 'verse')
