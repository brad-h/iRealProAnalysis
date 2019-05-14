from iRealProAnalysis import get_tunes, JAZZ1350, RHYTHM_CHANGES, KEYS, Chord, parse_chord, split_chords_in_measure, extension_to_quality
from ddt import ddt, data
from unittest import TestCase, main
from collections import namedtuple
from itertools import product

class Jazz1350Tests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tunes = get_tunes(JAZZ1350)
    
    def test_all_keys_provided(self):
        unique_keys_in_dataset = set(t.key for t in self.tunes)
        all_keys = set(KEYS.keys())
        self.assertTrue(unique_keys_in_dataset.issubset(all_keys))
    

class RhythmTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tunes = get_tunes(RHYTHM_CHANGES)


Case = namedtuple("Case", ["data", "expected"])

@ddt
class DataTests(TestCase):
    def test_all_keys_have_seven_notes(self):
        split_keys = [x.split(" ") for x in KEYS.values()]
        self.assertTrue(all(len(x) == 7 for x in split_keys))
    
    def test_all_keys_are_ascending_in_ring(self):
        notes = "ABCDEFG"
        all_notes = set(notes[x:] + notes[:x] for x in range(len(notes)))

        remove_sharps_flats = [x.replace("#", "").replace("b", "").replace(" ", "") for x in KEYS.values()]
        
        self.assertTrue(all(x in all_notes for x in remove_sharps_flats))

    @data(
        Case("7", "Dominant"),
        Case("", "Major"),
        Case("^", "Major"),
        Case("^7", "Major"),
        Case("6", "Major"),
        Case("-", "Minor"),
        Case("-7", "Minor"),
        Case("h7", "Half-Diminished"),
        Case("o", "Diminished"),
        Case("o7", "Diminished"))
    def test_extention_to_quality(self, tc):
        actual = extension_to_quality(tc.data)
        self.assertEqual(actual, tc.expected)

    @data(*map("".join, product("ABCDEFG", "#b", "7")))
    def test_parse_dominant_chord_symbol(self, tc):
        actual = parse_chord(tc)
        expected = Chord(tc.replace("7", ""), "Dominant", None)
        self.assertEqual(actual, expected)

    @data(*map("".join, product("ABCDEFG", "#b", ["", "^", "^7", "6"])))
    def test_parse_major_chord_symbol(self, tc):
        actual = parse_chord(tc)
        note = tc.replace("^", "").replace("7", "").replace("6", "")
        expected = Chord(note, "Major", None)
        self.assertEqual(actual, expected)

    @data(*map("".join, product("ABCDEFG", "#b", ["-", "-7"])))
    def test_parse_minor_chord_symbol(self, tc):
        actual = parse_chord(tc)
        note = tc.replace("-", "").replace("7", "")
        expected = Chord(note, "Minor", None)
        self.assertEqual(actual, expected)

    @data(*map("".join, product("ABCDEFG", "#b", ["h7"])))
    def test_parse_halfdiminished_chord_symbol(self, tc):
        actual = parse_chord(tc)
        expected = Chord(tc.replace("h7", ""), "Half-Diminished", None)
        self.assertEqual(actual, expected)

    @data(*map("".join, product("ABCDEFG", "#b", ["o", "o7"])))
    def test_parse_diminished_chord_symbol(self, tc):
        actual = parse_chord(tc)
        note = tc.replace("o", "").replace("7", "")
        expected = Chord(note, "Diminished", None)
        self.assertEqual(actual, expected)
    
    @data(
        Case("Bb6/F", Chord("Bb", "Major", "F")),
        Case("Bb7/D", Chord("Bb", "Dominant", "D")))
    def test_parse_slash_bass_note(self, tc):
        actual = parse_chord(tc.data)
        self.assertEqual(actual, tc.expected)

    @data("D7", "G7", "F7", "Bb6", "C7")
    def test_split_single_chord_in_bar(self, tc):
        chords = split_chords_in_measure(tc)
        self.assertEqual(len(chords), 1)
    
    @data("Bb6F7", "Bb6/FF7", "Bb6/FEb9", "D-7G7", "Eb7Eo7", "D-7G-7", "Bb7Bb7/D", "Bb6G-7", "C-7F7")
    def atest_split_two_chords_in_bar(self, tc):
        chords = split_chords_in_measure(tc)
        self.assertEqual(len(chords), 2)
    
    @data("Bb6F7Bb6G-7")
    def atest_split_four_chords_in_bar(self, tc):
        chords = split_chords_in_measure(tc)
        self.assertEqual(len(chords), 4)

    @data()
    def test_parse_chord(self):
        parse_chord("")

if __name__ == "__main__":
    main().runTests()