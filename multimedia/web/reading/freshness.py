"""Derived fingerprints for the freshness poll endpoints (spec 258)."""
import hashlib
import json


def list_fingerprint(rows):
    """Fingerprint the ordered (id, version) pairs of a scoped list."""
    pairs = [[row.pk, row.version] for row in rows]
    payload = json.dumps(pairs, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()
