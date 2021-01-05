#/usr/bin/python

import guitarpro
from midiutil import MIDIFile

# settings
# FILE = 'GuitarProFiles/Orion.gp5'
FILE = 'GuitarProFiles/Stairway to Heaven.gp5'
song = guitarpro.parse(FILE)
SELECTED_TRACK = 1 # "J. Hetfield (Rhythm)"
MEASURE_START = 1
MEASURE_STOP = 4
NAME = song.title

def getTuning(obj):
    """
    Return an array of given track tuning
    """
    return [string for string in obj.strings]

# midiutils settings
track = 0
channel = 0
tempo = song.tempo  # in BPM
volume = 100        # 0-127, as per the MIDI standard
time = 0            # In ticts start on beat 0  (4 ticts = 1 beat)
tact = 0            # In ticts start on beat 0
duration = 0        # In ticts 

midi = MIDIFile(1)
midi.addTrackName(track, time, NAME)
midi.addTempo(track, time, tempo)
midi.eventtime_is_ticks=True

###################################
# TODO 
# writing diferent voices to midi:
#   Splitting to a secondary channel for certain effects?
# implement some kind of effects: 
#   Different types of harmonics, 
#   bendings, 
#   volume, 
#   muted notes, 
#   vibratos, 
# tempo changing between beats 
# 
###################################

for measure in song.tracks[SELECTED_TRACK].measures:
    tuning = getTuning(song.tracks[SELECTED_TRACK])
    if measure.number >= MEASURE_START and measure.number <= MEASURE_STOP:
        tact += 4.0
        # print("NEW TACT")
        for i, voice in enumerate(measure.voices):
            # print("NEW VOICE")
            if i == 0:
                for beat in voice.beats:
                    for note in beat.notes:
                        duration = 1/beat.duration.value * 4
                        volume = note.velocity
                        pitch = tuning[note.string-1].value + note.value

                        # INTERPRETATION OF EFFECTS 
                        if note.beat.duration.isDotted:
                            duration += duration/2

                        midi.addNote(track, channel, pitch, time, duration, volume)
                        # print(track, channel, pitch, time, duration, volume)

                    time += duration
                    # print('-------')
                time = tact

with open("output.mid", 'wb') as outf:
    midi.writeFile(outf)