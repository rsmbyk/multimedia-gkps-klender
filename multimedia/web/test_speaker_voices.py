"""Liturgy speaker voices (spec 059).

The congregation faces the screen: a leader line is a quiet cue, a joined line is one
they read and say, and every other voice is the ordinary text. The classifier is pure,
so most of these tests need no database; the last class renders real pages.
"""

from datetime import date

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from multimedia.web.reading.voices import ASSEMBLY, JOIN, LEADER, read_mark, voice_lines


def voices(*lines):
    return [line.voice for line in voice_lines(list(lines))]


class ReadMarkTests(SimpleTestCase):
    def assert_voice(self, line, voice, mark, text):
        found = read_mark(line)
        self.assertIsNotNone(found, line)
        self.assertEqual((found.voice, found.mark, found.text), (voice, mark, text), line)

    def test_leader_labels_share_one_voice(self):
        for label in ('L', 'Liturgis', 'Litrugis', 'P', 'Paragenda', 'Pendeta', 'Pandita',
                      'Pdt', 'Pelayan', 'Pemimpin', 'Parambilan'):
            with self.subTest(label=label):
                self.assert_voice(f'{label}: Marilah kita berdoa', LEADER, f'{label}:',
                                  'Marilah kita berdoa')

    def test_initials_with_a_period_keep_the_period_in_the_mark(self):
        self.assert_voice('P. Marilah kita bangkit berdiri', LEADER, 'P.',
                          'Marilah kita bangkit berdiri')
        self.assert_voice('L. Tuhan beserta kamu', LEADER, 'L.', 'Tuhan beserta kamu')
        self.assert_voice('J. Amin.', ASSEMBLY, 'J.', 'Amin.')
        self.assert_voice('K. Haleluya', ASSEMBLY, 'K.', 'Haleluya')

    def test_labels_match_without_regard_to_case(self):
        self.assert_voice('PARAGENDA: Ibagas Goran ni Naibata', LEADER, 'PARAGENDA:',
                          'Ibagas Goran ni Naibata')
        self.assert_voice('jemaat: Amin', ASSEMBLY, 'jemaat:', 'Amin')

    def test_every_joined_form_is_the_joined_voice(self):
        for mark in ('P+K', 'P + K', 'P.+K', 'P/K', 'L+J', 'L.+J', 'L. + J', 'P+J',
                     'P + J', 'P.J', 'PJ', 'K+P'):
            for separator in (':', '.'):
                with self.subTest(mark=mark, separator=separator):
                    self.assert_voice(f'{mark}{separator} Marilah kita memuji TUHAN', JOIN,
                                      f'{mark}{separator}', 'Marilah kita memuji TUHAN')

    def test_a_joined_mark_can_be_followed_by_a_space_alone(self):
        self.assert_voice('P+K\t(Mandodingkon) Haleluya', JOIN, 'P+K', '(Mandodingkon) Haleluya')

    def test_the_congregation_and_named_groups_are_the_ordinary_voice(self):
        for label in ('J', 'K', 'Jemaat', 'Kuria', 'Bapa', 'Inang', 'Namaposo', 'Pengkhotbah',
                      'Orang tua', 'Ketua Sie Namaposo', 'SM/Remaja', 'O.T'):
            with self.subTest(label=label):
                self.assert_voice(f'{label}: Amin', ASSEMBLY, f'{label}:', 'Amin')

    def test_named_groups_take_a_period_too(self):
        self.assert_voice('Bapa. Ningon ma', ASSEMBLY, 'Bapa.', 'Ningon ma')
        self.assert_voice('Parambilan. Martonggo ma hita', LEADER, 'Parambilan.',
                          'Martonggo ma hita')

    def test_cues_are_not_speakers(self):
        for label in ('Next', 'Lagu', 'Doding', 'Nyanyian', 'Mandoding', 'Mandodingkon', 'Refr',
                      'Reff', 'Puisi', 'Bacaan', 'Prolog', 'Lagu Penutup',
                      'Nyanyian Persembahan'):
            with self.subTest(label=label):
                found = read_mark(f'{label}: Haleluya')
                self.assertIsNotNone(found)
                self.assertEqual((found.voice, found.mark), ('', ''))
                self.assertEqual(found.text, f'{label}: Haleluya')

    def test_a_sentence_is_not_a_speaker(self):
        for line in ('Maka jiwaku pun memuji-Mu: Haleluya',     # more than three words
                     'Marolob-olob au mamuji Ham. Haleluya',    # a period ends a sentence
                     'Tuhan holong ma Ham. Amen',
                     'Amin. Tuhan berkata: Damai',
                     'Amin.',                                   # nothing after the mark
                     'Lukas 6:27-36',                           # a scripture reference
                     'Lk 6: 27',                                # not L + K
                     '1. Ia datang',
                     '“Horahan Ahu!” (Johannes 19: 5)',
                     'Haleluya, Haleluya, Haleluya.'):
            with self.subTest(line=line):
                self.assertIsNone(read_mark(line))

    def test_a_label_counts_only_at_the_start_of_the_line(self):
        self.assertIsNone(read_mark('Seperti kata Pdt. August Theis: kasih itu sabar'))
        self.assert_voice('Pdt. August Theis menulis', LEADER, 'Pdt.', 'August Theis menulis')


class VoiceLinesTests(SimpleTestCase):
    def test_an_unmarked_line_keeps_the_previous_voice(self):
        self.assertEqual(voices('P: Marilah kita', 'bangkit berdiri', 'J: Amin.'),
                         [LEADER, LEADER, ASSEMBLY])

    def test_a_blank_line_does_not_reset_the_voice(self):
        self.assertEqual(voices('P+J: Marilah kita', '', 'memuji TUHAN'), [JOIN, '', JOIN])

    def test_another_speaker_breaks_the_cue(self):
        self.assertEqual(voices('P: Marilah kita', 'Bapa: Ningon ma', 'dob ai'),
                         [LEADER, ASSEMBLY, ASSEMBLY])

    def test_a_cue_returns_to_the_ordinary_text(self):
        self.assertEqual(voices('P: Marilah kita', 'Nyanyian: Haleluya', 'Haleluya, Haleluya'),
                         [LEADER, '', ''])

    def test_a_body_starts_ordinary(self):
        self.assertEqual(voices('Haleluya', 'P: Marilah'), ['', LEADER])

    def test_each_line_keeps_what_was_written(self):
        line = voice_lines(['P: Marilah kita'])[0]
        self.assertEqual((line.line, line.mark, line.text), ('P: Marilah kita', 'P:',
                                                             'Marilah kita'))


class RenderedVoicesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = tatib.TataIbadah.objects.create(name='Ibadah Minggu',
                                                      date=date(2026, 10, 18))
        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru',
                                               abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        cls.matius = bible.BookTranslation.objects.create(version=version, book=book,
                                                          translation='Matius')
        bible.Verse.objects.create(book_translation=cls.matius, chapter=5, verse=3,
                                   text='P: ayat tiga')
        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=songbook, number=1, title='Pujilah')
        songs.Verse.objects.create(song=cls.song, number=1, lyric='P: bait satu')

    def entry(self, order, **fields):
        return tatib.ServiceEntry.objects.create(tatib=self.service, order_number=order, **fields)

    def projector(self):
        response = self.client.get(reverse('web-service-projector', args=[self.service.pk]))
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    def stage(self):
        response = self.client.get(reverse('web-tatib-service', args=[self.service.pk]))
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    def test_the_projector_colors_a_text_entry_and_keeps_the_line_as_written(self):
        self.entry(1, kind=tatib.ServiceEntryKind.TEXT, title='Votum',
                   text='P: Marilah kita bangkit berdiri\nJ: Amin.\n\nP+J: Kita memuji TUHAN')
        html = self.projector()
        self.assertIn('<p class="screen__line is-leader">P: Marilah kita bangkit berdiri</p>',
                      html)
        self.assertIn('<p class="screen__line is-assembly">J: Amin.</p>', html)
        self.assertIn('<p class="screen__line is-join">P+J: Kita memuji TUHAN</p>', html)

    def test_the_voice_carries_onto_the_next_screen_of_the_same_item(self):
        self.entry(1, kind=tatib.ServiceEntryKind.TEXT, title='Doa',
                   text='P: Marilah kita berdoa\n\nYa Tuhan kami')
        self.entry(2, kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='Damai sejahtera')
        html = self.projector()
        self.assertIn('<p class="screen__line is-leader">Ya Tuhan kami</p>', html)
        self.assertIn('<p class="screen__line">Damai sejahtera</p>', html)

    def test_single_screen_text_and_legacy_rows_are_voiced(self):
        self.entry(1, kind=tatib.ServiceEntryKind.SINGLE_SCREEN_TEXT, title='Doa',
                   text='L: Marilah\nberdoa')
        tatib.TataIbadahItem.objects.create(tatib=self.service, order_number=2,
                                            item_type=tatib.TataIbadahItemType.TEXT,
                                            title='Introitus', text='Paragenda: Ibagas Goran')
        html = self.projector()
        self.assertIn('<p class="screen__line is-leader">berdoa</p>', html)
        self.assertIn('<p class="screen__line is-leader">Paragenda: Ibagas Goran</p>', html)

    def test_songs_and_scripture_stay_ordinary_on_the_projector(self):
        self.entry(1, kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1])
        self.entry(2, kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                   chapter=5, verse_start=3)
        html = self.projector()
        self.assertIn('<p class="screen__line">P: bait satu</p>', html)
        self.assertIn('<p class="screen__line">P: ayat tiga</p>', html)
        self.assertNotIn('is-leader', html)

    def test_the_stage_lifts_the_mark_as_written_and_voices_the_line(self):
        self.entry(1, kind=tatib.ServiceEntryKind.TEXT, title='Votum',
                   text='Paragenda: Ibagas Goran\nJ. Amin.\nP+J: Kita memuji')
        html = self.stage()
        self.assertInHTML('<p class="tatib__tx is-leader"><span class="tatib__sp">Paragenda:'
                          '</span> Ibagas Goran</p>', html)
        self.assertInHTML('<p class="tatib__tx is-assembly"><span class="tatib__sp">J.</span>'
                          ' Amin.</p>', html)
        self.assertInHTML('<p class="tatib__tx is-join"><span class="tatib__sp">P+J:</span>'
                          ' Kita memuji</p>', html)

    def test_the_preview_of_a_clipped_text_is_voiced(self):
        self.entry(1, kind=tatib.ServiceEntryKind.TEXT, title='Doa',
                   text='P: satu\ndua\ntiga\nJ: empat')
        html = self.stage()
        self.assertIn('<p class="preview__line is-assembly"><span class="tatib__sp">J:</span>'
                      ' empat</p>', html)
        self.assertIn('<p class="preview__line is-leader">dua</p>', html)
