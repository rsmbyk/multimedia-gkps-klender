from django.contrib import admin

from multimedia.tatib import models


@admin.register(models.TataIbadah)
class TataIbadahAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    list_filter = ('is_active',)


@admin.register(models.TataIbadahItem)
class TataIbadahItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ('tatib',)
    search_fields = ('tatib__name', 'text')
    list_filter = ('item_type',)


@admin.register(models.ServiceEntry)
class ServiceEntryAdmin(admin.ModelAdmin):
    autocomplete_fields = ('tatib', 'book_translation', 'song')
    search_fields = ('tatib__name', 'title', 'text')
    list_filter = ('kind',)
