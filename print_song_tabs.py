#/usr/bin/python

import guitarpro

file = 'GuitarProFiles/Orion.gp5'
# file = 'GuitarProFiles/Stairway to Heaven.gp5'
song = guitarpro.parse(file)

selected_track = "J. Hetfield (Rhythm)"
# selected_track = "GuitarProFiles/Jimmy Page - Acoustic Guitar"
measure_start = 72
measure_stop = 72

# for track in song.tracks:
#     if track.name == selected_track:
#         for measure in track.measures:
#             if measure.number >= measure_start and measure.number <= measure_stop:
#                 print(f"NEW MEASURE: {measure.number}")
#                 for voice in measure.voices:
#                     print("\tNEW VOICE")
#                     for beat in voice.beats:
#                         print(f"\t\tNEW BEAT: 1/{beat.duration.value}")
#                         try:
#                             # print(f"\t\t\t{beat.notes}")
#                             for chord in beat.notes:
#                                 print(f"\t\t\t{chord.value}, on string: {chord.string}")
#                                 # print(chord)
#                         except:
#                             pass


print(song.tracks[0].name)
for measure in song.tracks[0].measures:
    if measure.number >= measure_start and measure.number <= measure_stop:
        print(f"NEW MEASURE: {measure.number},\
             measure.timeSignature.beams = {measure.timeSignature.beams}")
        
        for voice in measure.voices:
            print(f"\tNEW VOICE")
            for beat in voice.beats:
                print(f"\t\tNEW BEAT: 1/{beat.duration.value}")
                try:
                    # print(f"\t\t\t{beat.notes}")
                    for chord in beat.notes:
                        print(f"\t\t\t {chord.type}")
                        print(f"\t\t\t {chord.beat.duration.isDotted}")
                        x = chord.effect.palmMute
                        print(f"\t\t\t {x}")
                        print(f"\t\t\t {chord.value}, on string: {chord.string}")
                        # print(chord)
                except:
                    pass