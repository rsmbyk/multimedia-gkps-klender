"""Reseed the spec-252 preview database from a fresh process.

Keeping this out of the Playwright process means the preview probe needs no
Django async-guard relaxation: reseeding finishes before the browser starts.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import serve  # noqa: E402  (path prepared above)


def main():
    os.environ.pop('DJANGO_ALLOW_ASYNC_UNSAFE', None)
    serve.prepare_env()
    serve.seed(collect_static=False)


if __name__ == '__main__':
    main()
