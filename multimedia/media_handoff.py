"""Private R2 handoff: server signs one-object transfers, never proxies bytes."""

import os
import hashlib
import secrets
from datetime import timedelta

from django.utils import timezone
from django.db.models import Q

from multimedia.tatib.models import MediaShare


class CloudUnavailable(RuntimeError):
    pass


def config():
    names = ('GKPS_R2_ACCOUNT_ID', 'GKPS_R2_BUCKET', 'GKPS_R2_ACCESS_KEY_ID',
             'GKPS_R2_SECRET_ACCESS_KEY')
    values = {name: os.environ.get(name, '').strip() for name in names}
    if not all(values.values()):
        raise CloudUnavailable('Online sharing is not configured.')
    prefix = os.environ.get('GKPS_R2_PREFIX', 'temporary-media').strip('/')
    if not prefix or '..' in prefix.split('/'):
        raise CloudUnavailable('Invalid R2 prefix.')
    values['prefix'] = prefix
    values['endpoint'] = os.environ.get('GKPS_R2_ENDPOINT') or (
        'https://' + values['GKPS_R2_ACCOUNT_ID'] + '.r2.cloudflarestorage.com')
    if not values['endpoint'].startswith('https://'):
        raise CloudUnavailable('R2 requires an HTTPS endpoint.')
    return values


def client():
    values = config()
    try:
        import boto3
        from botocore.config import Config
    except ImportError as exc:
        raise CloudUnavailable('R2 client is not installed.') from exc
    return boto3.client(
        's3', endpoint_url=values['endpoint'],
        aws_access_key_id=values['GKPS_R2_ACCESS_KEY_ID'],
        aws_secret_access_key=values['GKPS_R2_SECRET_ACCESS_KEY'],
        region_name='auto', config=Config(signature_version='s3v4'))


def bucket():
    return config()['GKPS_R2_BUCKET']


def object_key(sha):
    return config()['prefix'] + '/' + sha


def live_share(sha):
    share = MediaShare.objects.filter(media_id=sha, status='available').first()
    return share if share and share.expires_at and share.expires_at > timezone.now() else None


def status_for(identities):
    now = timezone.now()
    return {share.media_id: share.expires_at.isoformat()
            for share in MediaShare.objects.filter(media_id__in=identities,
                                                  status='available', expires_at__gt=now)}


def begin_share(media):
    from django.db import transaction
    with transaction.atomic():
        share = MediaShare.objects.select_for_update().filter(media=media).first()
        if share and share.status == 'available' and share.expires_at > timezone.now():
            return None, share
        key = object_key(media.sha256)
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        if share:
            share.object_key, share.status = key, 'pending'
            share.completion_token_hash = token_hash
            share.created_at = timezone.now()
            share.uploaded_at = share.expires_at = None
            share.save()
        else:
            share = MediaShare.objects.create(media=media, object_key=key,
                                              completion_token_hash=token_hash)
    url = client().generate_presigned_url(
        'put_object', Params={'Bucket': bucket(), 'Key': key,
                              'ContentType': 'application/octet-stream'},
        ExpiresIn=3600)
    return url, share, token


def complete_share(media, token):
    share = MediaShare.objects.filter(media=media, status='pending').first()
    if not share:
        raise CloudUnavailable('No upload is awaiting verification.')
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    if not secrets.compare_digest(share.completion_token_hash, token_hash):
        raise CloudUnavailable('Upload completion is not authorized.')
    try:
        head = client().head_object(Bucket=bucket(), Key=share.object_key)
    except Exception as exc:
        raise CloudUnavailable('The uploaded object could not be verified.') from exc
    if head.get('ContentLength') != media.byte_count:
        raise CloudUnavailable('The uploaded object has the wrong size.')
    share.status = 'available'
    share.completion_token_hash = ''
    share.uploaded_at = timezone.now()
    share.expires_at = share.uploaded_at + timedelta(days=7)
    share.save(update_fields=['status', 'completion_token_hash', 'uploaded_at', 'expires_at'])
    return share


def download_url(media):
    share = live_share(media.sha256)
    if not share:
        raise CloudUnavailable('This file is not available online.')
    remaining = int((share.expires_at - timezone.now()).total_seconds())
    if remaining <= 0:
        raise CloudUnavailable('This file is not available online.')
    try:
        head = client().head_object(Bucket=bucket(), Key=share.object_key)
    except Exception as exc:
        code = getattr(exc, 'response', {}).get('Error', {}).get('Code', '')
        if code in ('404', 'NoSuchKey', 'NotFound'):
            share.delete()
            raise CloudUnavailable('This file is no longer available online.') from exc
        raise CloudUnavailable('Online availability could not be checked.') from exc
    if head.get('ContentLength') != media.byte_count:
        share.delete()
        raise CloudUnavailable('The online file has the wrong size.')
    return client().generate_presigned_url(
        'get_object', Params={'Bucket': bucket(), 'Key': share.object_key},
        ExpiresIn=min(remaining, 604800)), share.expires_at


def cleanup_expired():
    count = 0
    now = timezone.now()
    for share in MediaShare.objects.filter(
            Q(expires_at__lte=now) |
            Q(status='pending', created_at__lte=now - timedelta(days=1))):
        try:
            client().delete_object(Bucket=bucket(), Key=share.object_key)
        except Exception:
            continue
        share.delete()
        count += 1
    return count
