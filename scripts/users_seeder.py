import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multimedia.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import User, Group, Permission


if not User.objects.filter(username='rsmbyk').exists():
    user_rsmbyk = User.objects.create_superuser('rsmbyk', 'ronaldsumbayak611@gmail.com', 'sumbayak611')
    user_rsmbyk.first_name = 'Ronald'
    user_rsmbyk.last_name = 'Sumbayak'
    user_rsmbyk.save()

group_multimedia, created = Group.objects.get_or_create(name='Multimedia')
if created:
    group_multimedia.permissions.add(
        *Permission.objects.filter(content_type__app_label='songs'),
        *Permission.objects.filter(content_type__app_label='bible'),
        *Permission.objects.filter(content_type__app_label='bookmarks'),
    )

if not User.objects.filter(username='multimedia').exists():
    user_multimedia = User.objects.create_user('multimedia', '', 'multimedia321')
    user_multimedia.groups.add(group_multimedia)
    user_multimedia.is_staff = True
    user_multimedia.save()

group_public, created = Group.objects.get_or_create(name='Public')
if created:
    group_public.permissions.add(
        *Permission.objects.filter(content_type__app_label='songs', name__contains='Can view'),
        *Permission.objects.filter(content_type__app_label='bible', name__contains='Can view'),
        *Permission.objects.filter(content_type__app_label='bookmarks', name__contains='Can view'),
    )

if not User.objects.filter(username='gkpsklender'):
    user_gkpsklender = User.objects.create_user('gkpsklender', 'gkpsklender123')
    user_gkpsklender.groups.add(group_public)
