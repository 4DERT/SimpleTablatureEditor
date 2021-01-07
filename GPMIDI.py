#/usr/bin/python

import guitarpro
from midiutil import MIDIFile

class Error(Exception):
    """Base class for other exceptions"""
    pass

class MeasureError(Error):
    """Input measure value is out of range"""
    pass

class TrackError(Error):
    """Input track value is out of range"""
    pass

class GP2Midi():
    def __init__(self, GP_FILE, GP_SELECTED_TRACK = 'all', FIRST_MEASURE = 1, LAST_MEASURE = 'last', OUTPUT_FILE_NAME = 'output'):
        self.gp_file = guitarpro.parse(GP_FILE)
        self.SELECTED_TRACK = self.checkSelectedTrack(GP_SELECTED_TRACK)
        # Probably every track has the same number of bars
        self.NUM_OF_MEASURES = len(self.gp_file.tracks[0].measures)
        self.FIRST_MEASURE = self.checkFirstMeasure(FIRST_MEASURE)
        self.LAST_MEASURE = self.checkLastMeasure(LAST_MEASURE)
        self.OUTPUT_FILE_NAME = OUTPUT_FILE_NAME

    def _checkSelectedTrack(self, track):
        if track == 'all':
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
        if measure == 'last':
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
                self.write2Midi(gp_track, i)
        else:
            self.write2Midi(self.SELECTED_TRACK, 0)

        self.write2MidiFile()
    
    def _write2Midi(self, track, channel: int):
        self.track = 0      # selected fragment will be on midi track 0
        self.channel = channel
        self.tempo = self.gp_file.tempo
        self.new_bar = 0    # counter of bars(measures), 4 = 1 bar 
        self.time = 0       # counter of beats in self.bar
        self.duration = 0
        self.numerator = 0
        self.dominator = 0

        self.midi.addTrackName(self.track, self.new_bar, self.gp_file.title)
        self.midi.addTempo(self.track, self.new_bar, self.tempo)
        self.midi.eventtime_is_ticks = True

        for measure in range(self.FIRST_MEASURE, self.LAST_MEASURE):
            measure = track.measures[measure]
            tuning = self.getTuning(track)
            self.new_bar += 4.0


            numerator = measure.timeSignature.numerator
            dominator = measure.timeSignature.denominator.value
            if numerator != self.numerator or dominator != self.dominator:
                self.midi.addTimeSignature(self.track, self.new_bar, numerator, dominator, 24)

            print("NEW MEASURE",measure.number)
            for i, voice in enumerate(measure.voices):
                if i==0:
                    for beat in voice.beats:
                        
                        try:
                            tempo = beat.effect.mixTableChange.tempo.value
                            if tempo != self.tempo:
                                self.midi.addTempo(self.track, self.time, tempo)
                        except AttributeError:
                            pass

                        for note in beat.notes:
                            self.duration = 1/beat.duration.value*4
                            volume =  note.velocity
                            pitch = tuning[note.string-1].value + note.value

                            # INTERPRETATION OF EFFECTS 
                            if note.beat.duration.isDotted:
                                self.duration += self.duration/2
                            
                            print('\t',self.track, self.channel, pitch, self.time, self.duration, volume)
                            self.midi.addNote(self.track, self.channel, pitch, self.time, self.duration, volume)
                        self.time += self.duration
                    self.time = self.new_bar
        
    def _write2MidiFile(self):
        with open(self.OUTPUT_FILE_NAME+'.mid', 'wb') as outf:
            self.midi.writeFile(outf)