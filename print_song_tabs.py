#/usr/bin/python

import guitarpro
from pprint import pprint

FILE = 'GuitarProFiles/Orion.gp5'
# FILE = 'GuitarProFiles/Stairway to Heaven.gp5'
# FILE = 'GuitarProFiles/bell.gp5'
# FILE = 'GuitarProFiles/master.gp5'
SELECTED_TRACK = 0
MEASURE_START = 120
MEASURE_STOP = 130

song = guitarpro.parse(FILE)

def print_structure(song, selected_track, measure_start, measure_stop):
    tab = '\t'
    print(song.tracks[selected_track].name)
    for measure in song.tracks[selected_track].measures:
        if measure.number >= measure_start and measure.number <= measure_stop:
            print(f"NEW MEASURE: {measure.number}")
            # print(f"TIME SIGNATURE: {measure.timeSignature}")
            # print(f"TEMPO: {measure.timeSignature}")
            # print(f"TEMPO: {x}")
            # for x, y in measure.track.song.__dict__.items():
            #     print(f"{x} : {y}")
            
            for voice in measure.voices:
                print(f"{tab}NEW VOICE")

                for beat in voice.beats:
                    print(f"{tab*2}NEW BEAT: 1/{beat.duration.value}")
                    try:
                        x = beat.effect.mixTableChange.tempo.value
                        print(f"{tab*2}NEW TEMPO: {x}")
                    except AttributeError:
                        pass

                    # for note in beat.notes:
                        # x = note.effect.
                        # print(x)
                        # for x, y in note.__dict__.items():
                        #     print(f'{tab*3} {x} : {y}')

                        #     if str(x) == 'beat':
                        #         for k, v in beat.__dict__.items():
                        #             print(f'{tab*4} {k} : {v}')
            print('\n\n\n')

if __name__ == "__main__":
    print_structure(song, 1, MEASURE_START, MEASURE_STOP)

#TODO
# append time signatures to midi
# fix triplet crash