"""Check private R2 configuration; opt-in one-object transfer smoke test."""

import hashlib
import secrets
import urllib.request

from django.core.management.base import BaseCommand, CommandError

from multimedia import media_handoff


class Command(BaseCommand):
    help = 'Check R2 bucket access; --smoke uploads, downloads, and deletes one tiny object.'

    def add_arguments(self, parser):
        parser.add_argument('--smoke', action='store_true', help='Run an opt-in tiny transfer test.')

    def handle(self, *args, **options):
        try:
            client = media_handoff.client()
            bucket = media_handoff.bucket()
            client.head_bucket(Bucket=bucket)
            self.stdout.write(self.style.SUCCESS('R2 bucket access: OK'))
            if not options['smoke']:
                return
            data = b'gkps-media-r2-smoke-' + secrets.token_bytes(12)
            key = media_handoff.config()['prefix'] + '/.smoke-' + secrets.token_hex(12)
            digest = hashlib.sha256(data).hexdigest()
            try:
                put_url = client.generate_presigned_url(
                    'put_object', Params={'Bucket': bucket, 'Key': key,
                                          'ContentType': 'application/octet-stream'}, ExpiresIn=120)
                request = urllib.request.Request(put_url, data=data, method='PUT',
                                                 headers={'Content-Type': 'application/octet-stream'})
                with urllib.request.urlopen(request, timeout=30) as response:
                    if response.status not in (200, 201, 204):
                        raise CommandError('R2 smoke upload failed.')
                head = client.head_object(Bucket=bucket, Key=key)
                if head['ContentLength'] != len(data):
                    raise CommandError('R2 smoke HEAD size mismatch.')
                get_url = client.generate_presigned_url(
                    'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=120)
                with urllib.request.urlopen(get_url, timeout=30) as response:
                    downloaded = response.read()
                if hashlib.sha256(downloaded).hexdigest() != digest:
                    raise CommandError('R2 smoke downloaded bytes mismatch.')
            finally:
                client.delete_object(Bucket=bucket, Key=key)
            try:
                client.head_object(Bucket=bucket, Key=key)
            except Exception:
                self.stdout.write(self.style.SUCCESS('R2 smoke upload/GET/delete: OK'))
                return
            raise CommandError('R2 smoke object remains after deletion.')
        except media_handoff.CloudUnavailable as exc:
            raise CommandError(str(exc)) from exc
