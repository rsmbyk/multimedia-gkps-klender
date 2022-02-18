import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multimedia.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import User, Group, Permission


user_rsmbyk = User.objects.create_superuser('rsmbyk', 'ronaldsumbayak611@gmail.com', 'sumbayak611')
user_rsmbyk.first_name = 'Ronald'
user_rsmbyk.last_name = 'Sumbayak'
user_rsmbyk.save()

group_multimedia = Group.objects.create(name='Multimedia')
group_multimedia.permissions.add(
    *Permission.objects.filter(content_type__app_label='songs')
                       .exclude(content_type__model='language'),
    *Permission.objects.filter(content_type__app_label='bookmarks'),
)

user_multimedia = User.objects.create_user('multimedia', '', 'multimedia321')
user_multimedia.groups.add(group_multimedia)
user_multimedia.is_staff = True
user_multimedia.save()

group_public = Group.objects.create(name='Public')
group_public.permissions.add(
    Permission.objects.get(name='Can view book'),
    Permission.objects.get(name='Can view song'),
    Permission.objects.get(name='Can view verse'),
)

user_gkpsklender = User.objects.create_user('gkpsklender', 'gkpsklender123')
user_gkpsklender.groups.add(group_public)
