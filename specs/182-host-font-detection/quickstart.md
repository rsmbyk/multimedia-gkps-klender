# Quickstart — the computer's own fonts reach the converter

Links, not copies: the mounts and their precedence are in
[`data-model.md`](./data-model.md), the command contract in
[`contracts/launcher.md`](./contracts/launcher.md), and the reasons in [`research.md`](./research.md).

Every command below runs on the working machine **except** the Windows ones, which need a Windows
computer with Office installed (marked *manual, Windows*).

## 1. The default no longer needs `HOME`

```sh
env -u HOME docker compose config | grep -A2 'fonts/operator'
```

Expect a source inside the checkout — `<checkout>/.fonts` — not `/.local/share/gkps-fonts`.

## 2. What the launcher resolves

```sh
./docker/up.sh --print | grep -B1 -A3 'fonts/host'
```

Expect one read-only mount per directory that exists on this machine, numbered `1`, `2`, …; nothing
for a directory that is absent.

## 3. Start the stack

```sh
./docker/up.sh            # same as docker compose up -d
./docker/up.sh --build    # after an image change
```

## 4. What the container sees

```sh
docker compose exec media fc-cache -f
docker compose exec media fc-match 'Liberation Sans'    # a face this machine has
docker compose exec media fc-match 'Britannic Bold'     # the substitute, unless Office supplied it
docker compose exec media python -m multimedia.slide_fonts
```

The last one prints the nine recorded mappings; on a machine with Office, the two Office families
answer with their own names instead of `Noto Sans`.

## 5. The tests that guard the two rules

```sh
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:<port>/gkps182" \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.test_docker_compose tests.test_slides_fonts_conf
```

## 6. A converted deck, end to end — *manual, Windows*

1. On a Windows computer with Office, `docker\up.ps1 --print` should list `C:/Windows/Fonts`.
2. `docker\up.ps1`, then convert a deck that uses `Britannic Bold`.
3. The PDF's embedded fonts name `Britannic Bold`; the same deck converted on a computer without
   Office names the substitute.

## 7. Cost of the scan — *manual*

```sh
time docker compose up -d media
```

Record the delta against the same command with no host mount; the target is under 10 s for a directory
of 1,000 files.
