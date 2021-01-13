#/usr/bin/python

import guitarpro
import os
from urllib.request import urlopen


# file = 'GuitarProFiles/Orion.gp5'
# file = "https://d12drcwhcokzqv.cloudfront.net/44175980.gp5"
# file = 'GuitarProFiles/Stairway to Heaven.gp5'
# file = 'GuitarProFiles/Deutschland.gp5'


def getTuning(obj):
    """
    Return an array of given track tuning
    """
    # return [str(string) for string in obj.strings]
    return [string for string in obj.strings]


def tracksInfo(song):
    for i, track in enumerate(song.tracks):
        tuning = getTuning(track)[::-1]
        # tuning = ', '.join(string for string in tuning)
        print(f"{i}. {track.name}")
        print(f"   {track.channel}")
        print('   -> drum: ', len(track.strings)) if track.isPercussionTrack else print('   -> strings: ', len(track.strings), '\n', '  ->',tuning )
        print()

def fileInfo(file):
    conditions = [
        True if file.endswith('.gp3') else False,
        True if file.endswith('.gp4') else False,
        True if file.endswith('.gp5') else False
    ]
    if any(conditions):
        if file.startswith('https'):
            with urlopen(file) as stream:
                song = guitarpro.parse(stream)
        else:
            song = guitarpro.parse(file)
    else:
        raise ValueError
    
    
    print(f"File: {file}")
    print(f"Song title: {song.title}, from album: {song.album}")
    print(F"Song artist: {song.artist}")
    print(F"Song tempo: {song.tempo}")
    print(F"Song key: {song.key}")
    print(f"Song have {len(song.tracks)} tracks:")
    num_of_bars = []
    for track in song.tracks:
        num_of_bars.append(len(track.measures))
    print("track have",num_of_bars,"measures")
    tracksInfo(song)
    print('\n\n')

if __name__ == "__main__":
    directory = 'GuitarProFiles/'
    # for filename in os.listdir(directory):
    #     fileInfo(directory+filename)

    # fileInfo(directory+'Orion.gp5')

    # file = directory+'Orion.gp5'

    # url test
    file = "https://d12drcwhcokzqv.cloudfront.net/43845421.gp5"
    fileInfo(file)

    