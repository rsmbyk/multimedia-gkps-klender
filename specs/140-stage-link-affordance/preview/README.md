# Preview: The stage's entry links read as text until hovered

**Spec**: `specs/140-stage-link-affordance/spec.md`
**Shape**: `static` for the two stage widths and the phone, plus the live slice server
**Open**: `specs/140-stage-link-affordance/preview/controls.html` directly (it embeds
`phone.html` in a 390px frame), or live at `/tatib/144/`

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-140
DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8773 --noreload
```

Open `http://127.0.0.1:8773/tatib/144/`.

Regenerate the static pages after a markup or CSS change:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/140-stage-link-affordance/preview/build_controls.py
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| rest | open the route, do not point at the stage | every entry title is the same ink as its text, with no line: `HAL 7 — Porini Dong Marribu Hali`, `HAL 1 — Jahowa Sihol Pujionku`, `Kisah Para Rasul 1:1` |
| hover | point at a title | an underline 3px under the text; the colour does not change |
| focus | click the page, then Tab until a title is focused | the same underline, no colour change |
| dark | press the theme control | the same three states with ink `#F5F3EE` |
| wrapped | resize to ~900px or use a long title | the underline follows every line, and the title stays inside the pane |
| saved copy | open the same service in template mode | identical treatment, since the copy renders the same class |
| elsewhere | hover a search result, open the media library | unchanged: the result underlines as it did, the "used by" links keep `--link` |
| controls, desktop | open `preview/controls.html` and point at an entry | Preview / Edit / Delete keep their labels and sit in a 264px column the title never enters |
| phone | the 390px frame in `controls.html`, or `phone.html` alone at 390px | the labels collapse to three 27px icons, the column narrows to 106px, the title still ends before them |
