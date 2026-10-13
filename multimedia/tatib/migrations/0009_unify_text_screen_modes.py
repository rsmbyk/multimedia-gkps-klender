from django.db import migrations, models


def unify_text_rows(apps, schema_editor):
    entry = apps.get_model('tatib', 'ServiceEntry')
    entry.objects.using(schema_editor.connection.alias).filter(kind=4).update(
        kind=0, default_screen_mode='single_screen')


def restore_text_rows(apps, schema_editor):
    entry = apps.get_model('tatib', 'ServiceEntry')
    entry.objects.using(schema_editor.connection.alias).filter(
        kind=0, default_screen_mode='single_screen').update(kind=4)


class Migration(migrations.Migration):
    dependencies = [('tatib', '0008_serviceentry_screen_breaks')]

    operations = [
        migrations.AddField(
            model_name='serviceentry', name='default_screen_mode',
            field=models.CharField(max_length=13, default='multi_line', choices=[
                ('multi_line', 'Multi-line'), ('single_screen', 'Single-screen')]),
        ),
        migrations.RunPython(unify_text_rows, restore_text_rows),
        migrations.AlterField(
            model_name='serviceentry', name='kind',
            field=models.IntegerField(choices=[(0, 'Text'), (1, 'Scripture'),
                                               (2, 'Song'), (3, 'Section Break')]),
        ),
    ]
