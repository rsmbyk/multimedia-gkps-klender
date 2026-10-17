from django.core.management.base import BaseCommand

from multimedia.media_handoff import cleanup_expired


class Command(BaseCommand):
    help = 'Delete R2 media objects whose seven-day sharing period has ended.'

    def handle(self, *args, **options):
        self.stdout.write(f'Deleted {cleanup_expired()} expired media object(s).')
