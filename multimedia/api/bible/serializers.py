from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from multimedia.bible import models


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = '__all__'


class VersionSerializer(serializers.ModelSerializer):
    lang = LanguageSerializer()

    class Meta:
        model = models.Version
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class BookTranslationSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    version = VersionSerializer()
    book = BookSerializer()

    class Meta:
        model = models.BookTranslation
        fields = '__all__'


class VerseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    book_translation = BookTranslationSerializer()

    class Meta:
        model = models.Verse
        fields = '__all__'
