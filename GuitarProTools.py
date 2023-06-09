import os
import subprocess
import guitarpro
from urllib.request import urlopen
from GuitarPro_midi import Midi

class GPTools:
    def __init__(self, FILE):
        self.song = self.__check_file(FILE)

    def __check_file(self, FILE):
        try:
            conditions = [
                True if FILE.endswith('.gp3') else False,
                True if FILE.endswith('.gp4') else False,
                True if FILE.endswith('.gp5') else False
            ]
            if any(conditions):
                if FILE.startswith('https'):
                    with urlopen(FILE) as stream:
                        return guitarpro.parse(stream)
                elif FILE.startswith('file://'):
                    return guitarpro.parse(FILE[7::])
                else:
                    return guitarpro.parse(FILE)
            else:
                raise ValueError
        except FileNotFoundError:
            raise FileNotFoundError

    def __generate_file_name(self):
        file_name = self.song.title
        file_name = 'output' if len(file_name) < 1 else file_name
        return file_name

    def __getTuning(self, track):
        return [str(string) for string in track.strings]

    def print_song_info(self):
        print(f"Title: {self.song.title}")
        print(f'Album: {self.song.album}')
        print(F"Artist: {self.song.artist}")
        print(F"Tempo: {self.song.tempo} BPM")
        print(f"Song have {len(self.song.tracks[0].measures)} measures")
        print(f"Song have {len(self.song.tracks)} tracks:")
        for track in self.song.tracks:
            tuning = ', '.join(self.__getTuning(track)[::-1])
            print(f"{track.number}. {track.name}")
            if track.isPercussionTrack:
                print(f'\t-> drums: {len(track.strings)}')
            else:
                print(f'\t-> strings: {len(track.strings)}')
                print(f'\t-> tuning: {tuning}')
            print()

    def get_song_info(self) -> dict:
        tracks = {}
        for track in self.song.tracks:
            tuning = ', '.join(self.__getTuning(track)[::-1])
            name = track.name
            isPercussion = track.isPercussionTrack
            tracks[track.number] = [name, tuning, isPercussion]
        
        info = {
            'Title': self.song.title,
            'Artist': self.song.artist,
            'Album': self.song.album,
            'Tempo': self.song.tempo,
            'Measures': len(self.song.tracks[0].measures),
            'Tracks': tracks
        }
        return info

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
        if stop == -1:
            stop = len(self.song.tracks[0].measures)
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

    def save_as_midi(self, name = None, use_mscore = False, mscore_path = "", verbose = False):
        """
        Write song to midi file
        """
        if not name:
            name = self.__generate_file_name() + '.mid'

        if use_mscore and os.path.isfile(mscore_path):
            self.save_as_gp('/tmp/ste_tmp.gp5')
            subprocess.run([mscore_path, '/tmp/ste_tmp.gp5', '-o', name])
        else:
            midi = Midi(self.song, verbose)
            midi.write_to_file(name)
