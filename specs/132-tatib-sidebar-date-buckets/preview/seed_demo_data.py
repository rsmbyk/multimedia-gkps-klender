"""Seed a throwaway SQLite database with one service per bucket boundary (spec 132 preview).

Not app code and not a fixture: this exists so the owner can see all four buckets —
and the today pin inside Upcoming — on one screen. Run with DJANGO_DEVELOPMENT_MODE=true.
"""
from datetime import timedelta

from django.utils import timezone

from multimedia.tatib.models import TataIbadah

today = timezone.now().astimezone(timezone.get_current_timezone()).date()
# The panel buckets on the Jakarta day; seed from the same clock the page reads.
from zoneinfo import ZoneInfo
today = timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()

rows = [
    ('Ibadah Minggu', today),
    ('Ibadah Syukur', today),
    ('Ibadah Minggu Advent', today + timedelta(days=6)),
    ('Ibadah Natal', today + timedelta(days=60)),
    ('Ibadah Minggu', today - timedelta(days=8)),
    ('Bulan Oikumene', today - timedelta(days=30)),
    ('Ibadah Minggu', today - timedelta(days=45)),
    ('Pengakuan Iman', today - timedelta(days=100)),
    ('Ibadah Minggu', min(today - timedelta(days=200), today.replace(month=1, day=9))),
    ('Ibadah Natal 2025', today - timedelta(days=320)),
    ('Ibadah Tahun Baru', today - timedelta(days=400)),
]

TataIbadah.objects.all().delete()
for name, day in rows:
    TataIbadah.objects.create(name=name, date=day, is_active=True)
    print(f'{day.isoformat()}  {name}')
print(f'today is {today.isoformat()} (Asia/Jakarta); {len(rows)} services seeded')
