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
    def __init__(self, GP_FILE, GP_SELECTED_TRACK = -1, FIRST_MEASURE = 1, LAST_MEASURE = -1, OUTPUT_FILE_NAME = 'output'):
        
        
        self.gp_file = self._checkFile(GP_FILE)
        self.SELECTED_TRACK = self._checkSelectedTrack(GP_SELECTED_TRACK)
        # Probably every track has the same number of bars
        self.NUM_OF_MEASURES = len(self.gp_file.tracks[0].measures)
        self.FIRST_MEASURE = self._checkFirstMeasure(FIRST_MEASURE)
        self.LAST_MEASURE = self._checkLastMeasure(LAST_MEASURE)
        self.OUTPUT_FILE_NAME = OUTPUT_FILE_NAME

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

    def convert2Midi(self):
        self.midi = MIDIFile(1)
        if self.SELECTED_TRACK == 'all':
            for i, gp_track in enumerate(self.gp_file.tracks):
                print(f"~~~~~~~~~~~~~~{gp_track.name}~~~~~~~~~~~~~~")
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

            
            numerator = measure.timeSignature.numerator                     # ile
            dominator = measure.timeSignature.denominator.value             # jakich nut

            if numerator != self.numerator or dominator != self.dominator:
                self.numerator = numerator
                self.dominator = dominator

                self.bar_time = float(numerator) * 1/float(dominator)*4
                print(measure.number, self.numerator, self.dominator, 'bar end:', self.bar_time)

                dominator_values = {2 : 1, 4 : 2, 8 : 3, 16 : 4, 32 : 4}
                dominator_midi = dominator_values[self.dominator]

                self.midi.addTimeSignature(self.track, self.new_bar, self.numerator, dominator_midi, 12*dominator_midi)

            self.new_bar += self.bar_time

            print("NEW MEASURE",measure.number)
            for i, voice in enumerate(measure.voices):
                if i==0:
                    for beat in voice.beats:
                        self.duration = 1/beat.duration.value*4
                        print(self.duration)

                        try:
                            tempo = beat.effect.mixTableChange.tempo.value
                            if tempo != self.tempo:
                                self.tempo = tempo
                                self.midi.addTempo(self.track, self.time, self.tempo)
                        except AttributeError:
                            pass
                        
                    # INTERPRETATION:
                        # note with dot
                        if beat.duration.isDotted:
                            self.duration += self.duration/2

                        # Tuplet (tripets)
                        if beat.duration.tuplet.enters != 1 or beat.duration.tuplet.times != 1:
                            self.duration = (self.duration / beat.duration.tuplet.enters) * beat.duration.tuplet.times

                        # rest beat
                        if beat.status.value == 2:
                            self.time += self.duration
                            continue
                        

                        for note in beat.notes:
                            volume =  note.velocity
                            # pitch = tuning[note.string-1].value + note.value
                            pitch = note.realValue

                            # INTERPRETATION OF EFFECTS 
                            
                            
                            print('\t',self.track, self.channel, pitch, self.time, self.duration, volume)
                            self.midi.addNote(self.track, self.channel, pitch, self.time, self.duration, volume)
                        self.time += self.duration
                    self.time = self.new_bar
        
    def _write2MidiFile(self):
        with open(self.OUTPUT_FILE_NAME+'.mid', 'wb') as outf:
            self.midi.writeFile(outf)