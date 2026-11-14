"""Make old rows and service entries share the pane's existing reading order."""

from django.db import migrations


def assign_shared_order(apps, schema_editor):
    TataIbadah = apps.get_model('tatib', 'TataIbadah')
    LegacyItem = apps.get_model('tatib', 'TataIbadahItem')
    ServiceEntry = apps.get_model('tatib', 'ServiceEntry')
    database = schema_editor.connection.alias

    # Before this migration the pane showed every legacy row, followed by every
    # entry. Keep that visible order while assigning the single shared sequence.
    for service_id in TataIbadah.objects.using(database).order_by('pk').values_list('pk', flat=True):
        order_number = 1
        old_rows = list(LegacyItem.objects.using(database)
                        .filter(tatib_id=service_id).order_by('order_number', 'pk'))
        for row in old_rows:
            row.order_number = order_number
            order_number += 1
        if old_rows:
            LegacyItem.objects.using(database).bulk_update(old_rows, ['order_number'])

        entries = list(ServiceEntry.objects.using(database)
                       .filter(tatib_id=service_id).order_by('order_number', 'pk'))
        for entry in entries:
            entry.order_number = order_number
            order_number += 1
        if entries:
            ServiceEntry.objects.using(database).bulk_update(entries, ['order_number'])


class Migration(migrations.Migration):
    dependencies = [
        ('tatib', '0005_serviceentry'),
    ]

    operations = [
        migrations.RunPython(assign_shared_order, migrations.RunPython.noop),
    ]
