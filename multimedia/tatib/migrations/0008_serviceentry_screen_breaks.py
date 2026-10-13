from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('tatib', '0007_alter_serviceentry_kind')]

    operations = [
        migrations.AddField(
            model_name='serviceentry',
            name='screen_breaks',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='serviceentry',
            name='screen_breaks_reset',
            field=models.BooleanField(default=False),
        ),
    ]
