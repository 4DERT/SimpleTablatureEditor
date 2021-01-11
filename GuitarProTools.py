#!/usr/bin/python

import guitarpro
from urllib.request import urlopen
from GuitarPro_midi import Midi

class GPTools:
    def __init__(self, FILE):
        self.song = self.__check_file(FILE)

    def __check_file(self, FILE):
        conditions = [
            True if FILE.endswith('.gp3') else False,
            True if FILE.endswith('.gp4') else False,
            True if FILE.endswith('.gp5') else False
        ]
        if any(conditions):
            if FILE.startswith('https'):
                with urlopen(FILE) as stream:
                    return guitarpro.parse(stream)
            else:
                return guitarpro.parse(FILE)
        else:
            raise ValueError

    def __generate_file_name(self):
        file_name = self.song.title
        file_name = 'output' if len(file_name) < 1 else file_name
        return file_name

    def grep_track(self, *track: int):
        """
        Select track you want in output file
        """
        tracks = []
        for t in track:
            tracks.append(self.song.tracks[t-1]) 
        self.song.tracks = tracks
        
        # reset tracks id
        for i, track in enumerate(self.song.tracks):
            track.number = i
    
    def grep_measures(self, start, stop):
        """
        Select measures you want in output file
        """
        for track in self.song.tracks:
            measures = []
            for m in range(start-1, stop):
                measures.append(track.measures[m])
            track.measures = measures

            #reset track measures id
            for i, measure in enumerate(track.measures):
                measure.number = i 
    
    def save_as_gp(self, name = None):
        """
        Write song to .gp5 file
        """
        if not name:
            name = self.__generate_file_name() + '.gp5'
        guitarpro.write(self.song, name)

    def save_as_midi(self, name = None):
        midi = Midi(self.song)
        if not name:
            name = self.__generate_file_name() + '.mid'
        midi.write_to_file(name)
            

# obj = GPTools("https://d12drcwhcokzqv.cloudfront.net/41801025.gp5")
obj = GPTools("GuitarProFiles/stair.gp5")
# obj.grep_track(1, 2, 3, 4, 5, 6, 7, 8, 9)
# obj.grep_track(2)
# obj.grep_measures(1, 1)
# obj.grep_measures(1, 4)
obj.save_as_gp()
obj.save_as_midi()