#/usr/bin/python

import guitarpro
from midiutil import MIDIFile

# settings
FILE = 'Orion.gp5'
SELECTED_TRACK = 0 # "J. Hetfield (Rhythm)"
MEASURE_START = 53
MEASURE_STOP = 76
song = guitarpro.parse(FILE)
NAME = song.title

def getTuning(obj):
    """
    Return an array of given track tuning
    """
    return [string for string in obj.strings]
    # output
    # [GuitarString(number=6, value=40), GuitarString(number=5, value=45), GuitarString(number=4, value=50), GuitarString(number=3, value=55), GuitarString(number=2, value=59), GuitarString(number=1, value=64)]

# midiutils settings
track = 0
channel = 0
tempo = song.tempo  # in BPM
volume = 100        # 0-127, as per the MIDI standard
time = 0            # In beats start on beat 0
timeTACT = 0            # In beats start on beat 0
duration = 0        # In beats 1/2 1/4 (2, 4)

midi = MIDIFile(1)
midi.addTrackName(track, time, NAME)
midi.addTempo(track, time, tempo)
midi.eventtime_is_ticks=True


for measure in song.tracks[SELECTED_TRACK].measures:
    tuning = getTuning(song.tracks[SELECTED_TRACK])
    if measure.number >= MEASURE_START and measure.number <= MEASURE_STOP:
        timeTACT += 4.0
        print("NOWY TACT")
        for i, voice in enumerate(measure.voices):
            if i == 0:
                for beat in voice.beats:
                    for note in beat.notes:
                        duration = 1/beat.duration.value * 4
                        if note.beat.duration.isDotted:
                            duration += duration/2
                        if note.effect.palmMute:
                            duration = duration/2
                        volume = note.velocity
                        pitch = tuning[note.string-1].value + note.value
                        print(track, channel, pitch, time, duration, volume)
                        midi.addNote(track, channel, pitch, time, duration, volume)
                        if note.effect.palmMute:
                            duration += duration
                    time += duration
                    print('-------')
                time = timeTACT

with open("output.mid", 'wb') as outf:
    midi.writeFile(outf)