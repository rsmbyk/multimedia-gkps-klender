from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('tatib', '0010_mediaidentity_serviceentry_media_filename_and_more')]

    operations = [
        migrations.CreateModel(
            name='MediaShare',
            fields=[
                ('media', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                               primary_key=True, related_name='share',
                                               serialize=False, to='tatib.mediaidentity')),
                ('object_key', models.CharField(max_length=255)),
                ('status', models.CharField(default='pending', max_length=10)),
                ('completion_token_hash', models.CharField(blank=True, max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='mediashare',
            constraint=models.CheckConstraint(
                check=models.Q(status__in=['pending', 'available']),
                name='media_share_valid_status'),
        ),
    ]
