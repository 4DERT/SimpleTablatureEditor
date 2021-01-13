#!/usr/bin/python

from midiutil import MIDIFile

class Midi:
    def __init__(self, GuitarPro, IS_VERBOSE = False):
        self.gp_file = GuitarPro
        self.IS_VERBOSE = IS_VERBOSE
        self.dominator_values = {2 : 1, 4 : 2, 8 : 3, 16 : 4, 32 : 4}   # convert guitar pro domiantor values to midi

        self.midi = MIDIFile(len(self.gp_file.tracks)+1)
        self.midi.eventtime_is_ticks = True
        self.__console_log(f'Number of tracks: {len(self.gp_file.tracks)}')

        self.__write_to_midi_object()

    def __console_log(self, msg: str, tabs: int = 0):
        if self.IS_VERBOSE:
            print('\t'*tabs, msg)

    def __write_to_midi_object(self):
# TRACKS
        for gp_track in self.gp_file.tracks:
            self.numerator = 0
            self.dominator  = 0
            self.time = 0.0
            self.bar = 0.0
            self.bar_duration = 0.0
            self.tempo = self.gp_file.tempo
            self.__console_log(f'NEW TRACK: {gp_track.number} - {gp_track.name}')
            track = gp_track.number
            channel = gp_track.channel.channel

            self.midi.addTrackName(track, 0, gp_track.name)
            self.midi.addTempo(track, 0, self.tempo)
# MEASURES
            for measure in gp_track.measures:

                numerator = measure.timeSignature.numerator
                dominator = measure.timeSignature.denominator.value

                if numerator != self.numerator or dominator != self.dominator:
                    self.numerator = numerator
                    self.dominator = dominator

                    self.bar_duration = float(self.numerator) * 1/float(self.dominator)*4
                    self.__console_log(f'~~ New time signature: {self.numerator} {self.dominator}, bar will last {self.bar_duration} tics', tabs=1)

                    dominator_midi = self.dominator_values[self.dominator]

                    self.midi.addTimeSignature(track, self.bar, self.numerator, dominator_midi, 12*dominator_midi)

                
                self.__console_log(f'NEW MEASURE: {measure.number}:', tabs=1)
# VOICES
                # for voice in measure.voices:
                for i, voice in enumerate(measure.voices):
                    _channel = channel + i if channel != 15 else channel - 1
                    self.__console_log(f'NEW VOICE: {channel}:', tabs=2)
                    time = self.bar
                    tempo = self.tempo
# BEATS
                    for beat in voice.beats:
                        self.__console_log(f'New beat:', tabs=3)
                        duration = 1/beat.duration.value*4

                        try:
                            tempo_ = beat.effect.mixTableChange.tempo.value
                            if tempo_ != tempo:
                                tempo = tempo_
                                self.midi.addTempo(track, time, tempo)
                                self.__console_log(f'~~ New tempo: {tempo}', tabs=3)
                        except AttributeError:
                            pass
                        

                    # INTERPRETATION:
                        # note with dot
                        if beat.duration.isDotted:
                            self.__console_log(f"~~~ Beat is doted:", tabs=3)
                            duration += duration/2
                        
                        # Tuplet (tripets)
                        tuplet = beat.duration.tuplet
                        if tuplet.enters != 1 or tuplet.times != 1:
                            self.__console_log(f"~~~ New tuplet: enters: {tuplet.enters}, times: {tuplet.times}", tabs=3)
                            duration = (duration / tuplet.enters) * tuplet.times
                        
                        # rest beat
                        if beat.status.value == 2:
                            self.__console_log(f'~~~ Rest beat, duration: {duration}', tabs=3)
                            time += duration
                            continue
# NOTES
                        for note in beat.notes:
                        # INTERPRETATION OF EFFECTS 
                            # Tied note
                            if note.type.name == 'tie':
                                self.__console_log(f'~~~ note is tied', tabs=4)
                                continue
                            
                            self.__console_log(f'Adding a note: track: {track}, channel: {_channel}, pitch: {note.realValue}, time: {time}, duration: {duration}, velocity: {note.velocity}', tabs=4)
                            self.midi.addNote(track, _channel, note.realValue, time, duration, note.velocity)
                        time += duration
                    # time = self.bar

                self.bar += self.bar_duration
            
    def write_to_file(self, name):
        with open(name, 'wb') as outf:
            self.midi.writeFile(outf)