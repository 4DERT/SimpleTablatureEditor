#/usr/bin/python

import guitarpro
from midiutil import MIDIFile
from urllib.request import urlopen

class Error(Exception):
    """Base class for other exceptions"""
    pass

class MeasureError(Error):
    """Input measure value is out of range"""
    pass

class TrackError(Error):
    """Input track value is out of range"""
    pass

class FileError(Error):
    """Wrong input file"""
    pass

class GP2Midi():
    def __init__(self, GP_FILE, GP_SELECTED_TRACK = -1, FIRST_MEASURE = 1, LAST_MEASURE = -1, OUTPUT_FILE_NAME = 'output', IS_VERBOSE = False):
        self.gp_file = self._checkFile(GP_FILE)
        self.SELECTED_TRACK = self._checkSelectedTrack(GP_SELECTED_TRACK)
        # Probably every track has the same number of bars
        self.NUM_OF_MEASURES = len(self.gp_file.tracks[0].measures)
        self.FIRST_MEASURE = self._checkFirstMeasure(FIRST_MEASURE)
        self.LAST_MEASURE = self._checkLastMeasure(LAST_MEASURE)
        self.OUTPUT_FILE_NAME = OUTPUT_FILE_NAME
        self.IS_VERBOSE = IS_VERBOSE

    def _checkFile(self, file):
        conditions = [
            True if file.endswith('.gp3') else False,
            True if file.endswith('.gp4') else False,
            True if file.endswith('.gp5') else False]

        if any(conditions):
            if file.startswith('https'):
                with urlopen(file) as stream:
                    return guitarpro.parse(stream)
            else:
                return guitarpro.parse(file)
        else:
            raise FileError(file)

    def _checkSelectedTrack(self, track):
        if track == -1:
            return 'all'
        elif track in range(1, len(self.gp_file.tracks) + 1):
            return self.gp_file.tracks[track-1]
        else:
            raise TrackError(track)

    def _checkFirstMeasure(self, measure):
        if measure in range(1, self.NUM_OF_MEASURES + 1):
            return measure-1
        else:
            raise MeasureError(measure)

    def _checkLastMeasure(self, measure):
        if measure == -1:
            return self.NUM_OF_MEASURES
        elif measure in range(0, self.NUM_OF_MEASURES + 1) and measure >= self.FIRST_MEASURE:
            return measure
        else:
            raise MeasureError(measure)
    
    def _getTuning(self, obj):
        return [string for string in obj.strings]

    def _console_log(self, msg: str, tabs: int = 0):
        if self.IS_VERBOSE:
            print('\t'*tabs, msg)

    def convert2Midi(self):
        self.midi = MIDIFile(1)
        if self.SELECTED_TRACK == 'all':
            for i, gp_track in enumerate(self.gp_file.tracks):
                self._console_log(f'Track name: {gp_track.name}:', tabs = 0)
                self._write2Midi(gp_track, i)
        else:
            self._write2Midi(self.SELECTED_TRACK, 0)

        self._write2MidiFile()
    
    def _write2Midi(self, track, channel: int):
        self.track = 0      # selected fragment will be on midi track 0
        self.channel = channel
        self.tempo = self.gp_file.tempo
        self.new_bar = 0.0      # counter of bars(measures), 4 = 1 bar in 4/4
        self.bar_time = 0.0     # the length of the measure in MIDIUtils ticks
        self.time = 0           # counter of beats in self.bar
        self.duration = 0
        self.numerator = 0
        self.dominator = 0

        self.midi.addTrackName(self.track, 0, self.gp_file.title)
        self.midi.addTempo(self.track, 0, self.tempo)
        self.midi.eventtime_is_ticks = True

        for measure in range(self.FIRST_MEASURE, self.LAST_MEASURE):
            measure = track.measures[measure]
            tuning = self._getTuning(track)

            numerator = measure.timeSignature.numerator
            dominator = measure.timeSignature.denominator.value

            if numerator != self.numerator or dominator != self.dominator:
                self.numerator = numerator
                self.dominator = dominator

                self.bar_time = float(numerator) * 1/float(dominator)*4
                self._console_log(f'~~ New time signature: {self.numerator} {self.dominator}, bar will last {self.bar_time} tics', tabs=1)

                dominator_values = {2 : 1, 4 : 2, 8 : 3, 16 : 4, 32 : 4}
                dominator_midi = dominator_values[self.dominator]

                self.midi.addTimeSignature(self.track, self.new_bar, self.numerator, dominator_midi, 12*dominator_midi)

            self.new_bar += self.bar_time

            self._console_log(f'NEW MEASURE: {measure.number}:', tabs=1)

            for i, voice in enumerate(measure.voices):
                if i==0:
                    for beat in voice.beats:
                        self._console_log(f'New beat:', tabs=2)
                        self.duration = 1/beat.duration.value*4

                        try:
                            tempo = beat.effect.mixTableChange.tempo.value
                            if tempo != self.tempo:
                                self.tempo = tempo
                                self.midi.addTempo(self.track, self.time, self.tempo)
                                self._console_log(f'~~ New tempo: {self.tempo}', tabs=2)
                        except AttributeError:
                            pass
                        
                    # INTERPRETATION:
                        # note with dot
                        if beat.duration.isDotted:
                            self._console_log(f"~~~ Beat is doted:", tabs=2)
                            self.duration += self.duration/2

                        # Tuplet (tripets)
                        tuplet = beat.duration.tuplet
                        if tuplet.enters != 1 or tuplet.times != 1:
                            self._console_log(f"~~~ New tuplet: enters: {tuplet.enters}, times: {tuplet.times}", tabs=2)
                            self.duration = (self.duration / tuplet.enters) * tuplet.times

                        # rest beat
                        if beat.status.value == 2:
                            self._console_log(f'~~~ Rest beat', tabs=2)
                            self.time += self.duration
                            continue
                        
                        for note in beat.notes:
                        # INTERPRETATION OF EFFECTS 
                            # Tied note
                            if note.type.name == 'tie':
                                self._console_log(f'~~~ note is tied', tabs=3)
                                continue
                            
                            self._console_log(f'Adding a note: track: {self.track}, channel: {self.channel}, pitch: {note.realValue}, time: {self.time}, duration: {self.duration}, velocity: {note.velocity}', tabs=3)
                            self.midi.addNote(self.track, self.channel, note.realValue, self.time, self.duration, note.velocity)
                        self.time += self.duration
                    self.time = self.new_bar
        
    def _write2MidiFile(self):
        with open(self.OUTPUT_FILE_NAME+'.mid', 'wb') as outf:
            self.midi.writeFile(outf)