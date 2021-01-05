#/usr/bin/python

import guitarpro
from pprint import pprint

# FILE = 'GuitarProFiles/Orion.gp5'
FILE = 'GuitarProFiles/Stairway to Heaven.gp5'
SELECTED_TRACK = 0
MEASURE_START = 33
MEASURE_STOP = 35

song = guitarpro.parse(FILE)

def print_structure(song, selected_track, measure_start, measure_stop):
    tab = '\t'
    print(song.tracks[selected_track].name)
    for measure in song.tracks[selected_track].measures:
        if measure.number >= measure_start and measure.number <= measure_stop:
            print(f"NEW MEASURE: {measure.number}")
            for voice in measure.voices:
                print(f"{tab}NEW VOICE")

                for beat in voice.beats:
                    print(f"{tab*2}NEW BEAT: 1/{beat.duration.value}")

                    for note in beat.notes:
                        for x, y in note.__dict__.items():
                            print(f'{tab*3} {x} : {y}')

                            # if str(x) == 'beat':
                            #     for k, v in beat.__dict__.items():
                            #         print(f'{tab*4} {k} : {v}')

if __name__ == "__main__":
    print_structure(song, 0, MEASURE_START, MEASURE_STOP)