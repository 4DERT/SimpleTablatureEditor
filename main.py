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

    def checkSelectedTrack(self, track):
        if track == 'all':
            return 'all'
        elif track in range(1, len(self.gp_file.tracks)):
            return self.gp_file.tracks[track-1]
        else:
            raise TrackError(track)

    def checkFirstMeasure(self, measure):
        if measure in range(1, self.NUM_OF_MEASURES):
            return measure-1
        else:
            raise MeasureError(measure)

    def checkLastMeasure(self, measure):
        if measure == 'last':
            return self.NUM_OF_MEASURES
        elif measure in range(0, self.NUM_OF_MEASURES) and measure >= self.FIRST_MEASURE:
            return measure
        else:
            raise MeasureError(measure)
    
    def getTuning(self, obj):
        return [string for string in obj.strings]

    def convert2Midi(self):
        self.midi = MIDIFile(1)
        if self.SELECTED_TRACK == 'all':
            for i, gp_track in enumerate(self.gp_file.tracks):
                print(i)
                self.write2Midi(gp_track, i)
        else:
            self.write2Midi(self.SELECTED_TRACK, 0)

        self.write2MidiFile()
    
    def write2Midi(self, track, channel: int):
        self.track = 0      # selected fragment will be on midi track 0
        self.channel = channel
        self.tempo = self.gp_file.tempo
        self.new_bar = 0    # counter of bars(measures), 4 = 1 bar 
        self.time = 0       # counter of beats in self.bar
        self.duration = 0

        self.midi.addTrackName(self.track, self.new_bar, self.gp_file.title)
        self.midi.addTempo(self.track, self.new_bar, self.tempo)
        self.midi.eventtime_is_ticks = True

        for measure in range(self.FIRST_MEASURE, self.LAST_MEASURE):
            measure = track.measures[measure]
            tuning = self.getTuning(track)
            self.new_bar += 4.0

            for i, voice in enumerate(measure.voices):
                if i==0:
                    for beat in voice.beats:
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
        
    def write2MidiFile(self):
        with open(self.OUTPUT_FILE_NAME+'.mid', 'wb') as outf:
            self.midi.writeFile(outf)


# obj = GP2Midi('GuitarProFiles/Stairway to Heaven.gp5', 'all', 1, 4, 'uf')
obj = GP2Midi('GuitarProFiles/Deutschland.gp5', 'all', 25, 35, 'uf')
obj.convert2Midi()