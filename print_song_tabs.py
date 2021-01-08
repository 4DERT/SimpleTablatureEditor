#/usr/bin/python

import guitarpro
from pprint import pprint

# FILE = 'GuitarProFiles/testgp.gp5'
# FILE = 'GuitarProFiles/Stairway to Heaven.gp5'
# FILE = 'GuitarProFiles/bell.gp5'
# FILE = 'GuitarProFiles/master.gp5'
FILE = 'GuitarProFiles/nothing.gp5'
SELECTED_TRACK = 1
MEASURE_START = 146
MEASURE_STOP = 150

song = guitarpro.parse(FILE)

def print_structure(song, selected_track, measure_start, measure_stop):
    tab = '\t'
    print(song.tracks[selected_track].name)
    for measure in song.tracks[selected_track].measures:
        if measure.number >= measure_start and measure.number <= measure_stop:
            # print("MIDI CHANNNNNEL:",measure.track.channel)
            print(f"NEW MEASURE: {measure.number}")
            # print(f"TIME SIGNATURE: {measure.timeSignature}")
            # print(f"TEMPO: {measure.timeSignature}")
            # print(f"TEMPO: {x}")
            # for x, y in measure.track.song.__dict__.items():
            #     print(f"{x} : {y}")
            
            print(f"measure.tripletFeel: {measure.tripletFeel}")
            
            for voice in measure.voices:
                print(f"{tab}NEW VOICE")

                for beat in voice.beats:
                    print(f"{tab*2}NEW BEAT: 1/{beat.duration.value}")

                    try:
                        x = beat.effect.mixTableChange.tempo.value
                        print(f"{tab*3}NEW TEMPO: {x}")
                    except AttributeError:
                        pass

                    # print(f"{tab*3}BEAT START: {beat.start}")
                    # print(f"{tab*3}beat.startInMeasure: {beat.startInMeasure}")
                    # print(f"{tab*3}beat.status.name: {beat.status.name}")
                    # print(f"{tab*3}beat.status.value: {beat.status.value}")     # jeżeli 0 to beat pusty jak 1 to normalny, jak 2 to jest pauza
                    # print(f"{tab*3}beat.status.name: {beat.status.name}")
                    # print(f"{tab*3}beat.duration.quarter: {beat.duration.quarter}")
                    # print(f"{tab*3}beat.duration.quarterTime: {beat.duration.quarterTime}")
                    
                    for x, y in beat.duration.__dict__.items():
                        print(tab*3,x, y)
                        

                    for note in beat.notes:
                        print(f"{tab*4}VALUE: {str(note.realValue)}")
                        
                        # x = note.effect.
                        # print(x)
                        # for x, y in note.__dict__.items():
                        #     print(f'{tab*3} {x} : {y}')

                        #     if str(x) == 'beat':
                        #         for k, v in beat.__dict__.items():
                        #             print(f'{tab*4} {k} : {v}')
            print('\n\n\n')

if __name__ == "__main__":
    print_structure(song, SELECTED_TRACK, MEASURE_START, MEASURE_STOP)

#TODO
# append time signatures to midi
# fix triplet crash