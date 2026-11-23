"""Print a song with verses and an empty song for preview navigation."""
import os
import subprocess
import sys
from urllib.parse import quote, urlsplit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

raw = subprocess.check_output(
    ["docker", "exec", "multimedia-gkps-klender-web-1", "python",
     "-c", "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
os.environ["DATABASE_URL"] = f"{p.scheme}://{p.username}:{quote(p.password or '', safe='')}@127.0.0.1:59075{p.path}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multimedia.settings")

import django
django.setup()
from multimedia.songs.models import Song, Verse

with_v = None
empty = None
for s in Song.objects.order_by("-id").iterator(chunk_size=200):
    n = Verse.objects.filter(song=s, is_deleted=False).count()
    if with_v is None and n >= 2 and s.title and not s.book.is_hymn_book:
        with_v = (s.pk, n, s.title[:60])
    if empty is None and n == 0 and s.title:
        empty = (s.pk, s.title[:60])
    if with_v and empty:
        break

print("WITH_VERSES", with_v)
print("EMPTY", empty)
