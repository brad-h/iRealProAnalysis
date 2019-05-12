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

def split_chords_in_measure(bar):
    return [bar]

Chord = namedtuple("Chord", ["key", "quality"])

def extension_to_quality(extension):
    return "Dominant"

def parse_chord(chord):
    (key,extension) = re.findall("([A-G][#b]?)(^7|7)?", chord)
    return Chord(key[0], extension_to_quality(extension))

if __name__ == "__main__":
    tunes = get_tunes(JAZZ1350)
    key_frequency = defaultdict(int)
    chart_frequency = defaultdict(list)
    for tune in tunes:
        key_frequency[tune.key] += 1
        chart_frequency[tune.chord_string].append(tune)
    
    cgroup = os.linesep.join("; ".join(x.title for x in v) for (k, v) in chart_frequency.items() if len(v) > 1)
    
    print(cgroup)
    print(sorted([(f, k) for (k, f) in key_frequency.items()], reverse=True))
    minor_count = sum(f for (x, f) in key_frequency.items() if x.find("-") >= 0)
    print("Minors: " + str(minor_count))
    major_count = sum(f for (x, f) in key_frequency.items() if x.find("-") < 0)
    print("Majors: " + str(major_count))
