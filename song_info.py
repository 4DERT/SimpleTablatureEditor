#/usr/bin/python

import guitarpro

file = 'GuitarProFiles/Orion.gp5'
# file = 'GuitarProFiles/Stairway to Heaven.gp5'
# file = 'GuitarProFiles/Deutschland.gp5'
song = guitarpro.parse(file)

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


if __name__ == "__main__":
    print(f"File: {file}")
    print(f"Song title: {song.title}, from album: {song.album}")
    print(F"Song artist: {song.artist}")
    print(F"Song tempo: {song.tempo}")
    print(F"Song key: {song.key}")
    print(f"Song have {len(song.tracks)} tracks:")
    tracksInfo(song)
    