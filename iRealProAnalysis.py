from pyRealParser import Tune
from collections import defaultdict, namedtuple
from enum import Enum
import re
import os

KEYS = {
    "C":   "C D E F G A B",
    "C-":  "C D Eb F G Ab Bb",

    "F":   "F G A Bb C D E",
    "F-":  "F G Ab Bb C Db Eb",
    
    "Bb":  "Bb C D Eb F G A",
    "Bb-": "Bb C Db Eb F Gb Ab",
    
    "Eb":  "Eb F G Ab Bb C D",
    "Eb-": "Eb F Gb Ab Bb Cb Db",
    
    "Ab":  "Ab Bb C Db Eb F G",
    "G#-": "G# A# B C# D# E F#",
    
    "Db":  "Db Eb F Gb Ab Bb C",
    "C#-": "C# D# E F# G# A B",
    
    "Gb":  "Gb Ab Bb Cb Db Eb F",
    "F#-": "F# G# A B C# D E",
    
    "B":   "B C# D# E F# G# A#",
    "B-":  "B C# D E F# G A",
    
    "E":   "E F# G# A B C# D#",
    "E-":  "E F# G A B C D",
    
    "A":   "A B C# D E F# G#",
    "A-":  "A B C D E F G",
    
    "D":   "D E F# G A B C#",
    "D-":  "D E F G A Bb C",
    
    "G":   "G A B C D E F#",
    "G-":  "G A Bb C D Eb F"
}

JAZZ1350 = "jazz1350.txt"
RHYTHM_CHANGES = "rhythmchanges.txt"

def get_tunes(file_name):
    with open(file_name, "r") as file:
        contents = file.read()
    tunes = Tune.parse_ireal_url(contents)
    return tunes

Chord = namedtuple("Chord", "key quality bass_note")

def split_chords_in_measure(bar):
    chords = re.findall(r"([A-G][#b]?)(7|6|\^7|\^|-7|-|h7|o7?)?(/[A-G][#b]?)?", bar)
    result = []
    for (key, extension, slash_chord) in chords:
        quality = extension_to_quality(extension)
        bass_note = parse_bass_note(slash_chord)
        result.append(Chord(key, quality, bass_note))
    return result

def extension_to_quality(extension):
    lookup = {
        "":   "Major",
        "^":  "Major",
        "^7": "Major",
        "6":  "Major",
        "7":  "Dominant",
        "-":  "Minor",
        "-7": "Minor",
        "h7": "Half-Diminished",
        "o":  "Diminished",
        "o7": "Diminished"
    }
    return lookup[extension]

def parse_bass_note(slash_chord):
    if slash_chord[:1] == "/":
        return slash_chord[1:]
    else:
        return None

def parse_chord(chord):
    return split_chords_in_measure(chord)[0]

def distance_from_natural(note):
    flats = len([x for x in note if x == "b"])
    sharps = len([x for x in note if x == "#"])
    return sharps - flats

def _strip_sharps_flats(note):
    return note.replace("b", "").replace("#", "")

def _distance_to_sharps_flats(distance):
    if distance > 0:
        return "#" * distance
    elif distance < 0:
        return "b" * abs(distance)
    else:
        return ""

def convert_to_roman_numeral(key, chord):
    roman_numerals = "I II III IV V VI VII".split(" ")
    scale = KEYS[key].split(" ")
    scale_notes = [_strip_sharps_flats(x) for x in scale]
    scale_position = scale_notes.index(_strip_sharps_flats(chord.key))
    distance = distance_from_natural(scale[scale_position]) + distance_from_natural(chord.key)
    return chord._replace(key=roman_numerals[scale_position] + _distance_to_sharps_flats(distance))

if __name__ == "__main__":
    tunes = get_tunes(JAZZ1350)
    key_frequency = defaultdict(int)
    chart_frequency = defaultdict(list)
    not_quite_contrafacts = defaultdict(list)

    for tune in tunes:
        assert isinstance(tune, Tune)
        key_frequency[tune.key] += 1
        chart_frequency[tune.chord_string].append(tune)
        chords_in_tune = tuple(chord for measure in tune.measures_as_strings for chord in split_chords_in_measure(measure))
        not_quite_contrafacts[chords_in_tune].append(tune)
    
    for (k, v) in not_quite_contrafacts.items():
        if len(v) > 1:
            for tune in v:
                print(tune.title)
            print()
    