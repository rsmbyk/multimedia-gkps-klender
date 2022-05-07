from django.db import models


class TataIbadah(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date', '-created_at')


class TataIbadahItemType(models.IntegerChoices):
    TEXT = 0
    END_OF_SECTION = 1


class TataIbadahItem(models.Model):
    tatib = models.ForeignKey(TataIbadah, models.PROTECT)
    item_type = models.IntegerField(choices=TataIbadahItemType.choices)
    text = models.TextField(blank=True)
    order_number = models.PositiveIntegerField()

    class Meta:
        ordering = ('tatib', 'order_number')
