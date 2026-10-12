"""Who speaks each line of a liturgy text (spec 059).

The projection screen faces the congregation. A leader line is only a cue that the
leader is speaking; a joined line is one the congregation reads and says; every other
voice -- the congregation, Bapa, Inang, Namaposo, any named group -- is the ordinary
text. The mapping is fixed, so a label wears the same voice in every Tata Ibadah.

A speaker is marked at the start of a line ("P: ...", "P. ...", "Paragenda: ...",
"P+K: ..."). A line with no mark keeps the voice of the line before it in the same
body, across blank lines, so the second screen of a leader's prayer is still a cue.
"""

import re
from typing import NamedTuple

LEADER = 'leader'
JOIN = 'join'
ASSEMBLY = 'assembly'

# Bare P is the liturgist (paragenda): the pastor is always spelled out.
LEADER_LABELS = frozenset({
    'l', 'liturgis', 'litrugis', 'p', 'paragenda', 'pendeta', 'pandita', 'pdt',
    'pelayan', 'pemimpin', 'parambilan',
})
ASSEMBLY_LABELS = frozenset({'j', 'k', 'jemaat', 'kuria', 'bapa', 'inang', 'namaposo'})
CUE_WORDS = frozenset({
    'next', 'lagu', 'doding', 'nyanyian', 'mandoding', 'mandodingkon', 'refr', 'reff',
    'puisi', 'bacaan', 'prolog',
})

_PAIR = (r'(?:[LP]\s*\.?\s*[+/]\s*[JK]|[JK]\s*\.?\s*[+/]\s*[LP]'
         r'|[LP]\.?[JK]|[JK]\.?[LP])')
# Capitals only: "Lk 6:27" is Lukas, not a leader and a congregation.
_JOIN_RE = re.compile(
    rf'^\s*(?P<mark>{_PAIR}(?:\s*[:.])?)(?:\s+|(?<=[:.]))(?P<text>\S.*)$')
# A period also ends sentences, so it closes only a single known label.
_DOT_RE = re.compile(r'^\s*(?P<mark>(?P<label>[^\W\d_]+)\.)\s*(?P<text>\S.*)$')
_COLON_RE = re.compile(
    r'^\s*(?P<mark>(?P<label>[^\s:][^:]{0,39}?)\s*:)\s*(?P<text>\S.*)$')
# Any other speaker: a capitalised name of up to three words ("Orang tua", "Ketua Sie
# Namaposo"). Longer runs before a colon are sentences ("Maka jiwaku pun memuji-Mu:").
_OTHER_LABEL_RE = re.compile(r'[A-Z]\S*(?:\s+\S+){0,2}')


class Mark(NamedTuple):
    """A line-start speaker mark: its voice, the mark as written, and the words after it.

    A cue ("Nyanyian: ...") has no voice and no mark; its text is the whole line.
    """

    voice: str
    mark: str
    text: str


class VoicedLine(NamedTuple):
    """One line of a body with the voice it is spoken in.

    ``line`` is the line as written, ``mark`` the lifted speaker mark ('' when the line
    has none) and ``text`` the words after it. ``voice`` is LEADER, JOIN, ASSEMBLY, or ''
    for the ordinary text with no speaker in play.
    """

    line: str
    voice: str
    mark: str
    text: str


def _known_voice(label):
    key = label.strip().lower()
    if key in LEADER_LABELS:
        return LEADER
    if key in ASSEMBLY_LABELS:
        return ASSEMBLY
    return None


def _colon_voice(label, text):
    """The voice of a colon label, '' for a cue, or None when it is not a speaker."""
    known = _known_voice(label)
    if known:
        return known
    if label.split()[0].lower() in CUE_WORDS:
        return ''
    if '. ' in label or text[0].isdigit():      # a sentence, or a "Lukas 6:27" reference
        return None
    return ASSEMBLY if _OTHER_LABEL_RE.fullmatch(label) else None


def read_mark(line):
    """Read the speaker mark at the start of ``line``; None when the line has no mark."""
    match = _JOIN_RE.match(line)
    if match:
        return Mark(JOIN, match['mark'].strip(), match['text'])
    match = _DOT_RE.match(line)
    if match and _known_voice(match['label']):
        return Mark(_known_voice(match['label']), match['mark'], match['text'])
    match = _COLON_RE.match(line)
    if match:
        voice = _colon_voice(match['label'], match['text'])
        if voice == '':
            return Mark('', '', line.strip())
        if voice:
            return Mark(voice, match['mark'], match['text'])
    return None


def voice_lines(lines):
    """Each line with its voice. An unmarked line keeps the previous voice; a blank line
    keeps it too (and is itself voiceless), so the voice survives a screen break."""
    voiced, voice = [], ''
    for line in lines:
        if not line.strip():
            voiced.append(VoicedLine(line, '', '', line))
            continue
        found = read_mark(line)
        if found is None:
            voiced.append(VoicedLine(line, voice, '', line))
            continue
        voice = found.voice
        voiced.append(VoicedLine(line, voice, found.mark, found.text))
    return voiced
