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
        # self.NUM_OF_MEASURES = len(self.gp_file.tracks[GP_SELECTED_TRACK].measures)
        self.FIRST_MEASURE = self.checkFirstMeasure(FIRST_MEASURE)
        self.LAST_MEASURE = self.checkLastMeasure(LAST_MEASURE)
        self.OUTPUT_FILE_NAME = OUTPUT_FILE_NAME

    def checkSelectedTrack(self, track):
        if track == 'all':
            return 'all'
        elif track in range(1, len(self.gp_file.tracks)):
            return self.gp_file.tracks[track]
        else:
            raise TrackError(track)

    def checkFirstMeasure(self, measure):
        # TODO
        # if measure in range(0, self.NUM_OF_MEASURES):
        if measure > 0:
            return measure
        else:
            raise MeasureError(measure)

    def checkLastMeasure(self, measure):
        if measure == 'last':
            return 'last'
        # TODO 
        # elif measure in range(0, self.NUM_OF_MEASURES) and measure >= self.FIRST_MEASURE:
        elif measure >= self.FIRST_MEASURE:
            return measure
        else:
            raise MeasureError(measure)

    def convert2Midi(self):
        self.track = 0  # selected fragment will be on midi track 0
        self.channel = 0 
        self.tempo = self.gp_file.tempo
        self.volume = 100
        self.bar = 0    # counter of bars(measures), 4 = 1 bar 
        self.time = 0   # counter of beats in self.bar
        self.duration = 0

        self.midi = MIDIFile(1)
        self.midi.addTrackName(self.track, self.bar, self.gp_file.title)
        self.midi.addTempo(self.track, self.bar, self.tempo)
        self.midi.eventtime_is_ticks = True

        for measure in range(self.FIRST_MEASURE, self.LAST_MEASURE):
            measure = self.SELECTED_TRACK.measures[measure]
            

obj = GP2Midi('GuitarProFiles/Stairway to Heaven.gp5', 1, 1, 4)