#!/usr/bin/python

# dependencies
# guitarpro (pip install PyGuitarPro) - tested on version 0.8
# midiutil (pip install MIDIUtil)- tested on version 1.2.1

import argparse
from GuitarProTools import GPTools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Edit and convert GuitarPro files')

    parser.add_argument('-i', '--input',
                        help='Path/url to GP* file',
                        metavar='', required=True)

    parser.add_argument('-t', '--track', action='append', nargs='*', type=int,
                        help='Select tracks', metavar='N')

    parser.add_argument('-m', '--measure', action='append',nargs=2, type=int,
                        help='Select measures', metavar='N')

    parser.add_argument('-o', '--output', type=str,
                        help='Name of output file',
                        metavar='', required=False, default=None)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gp5', action='store_true', help='Save as gp5 file')
    group.add_argument('--midi', action='store_true', help='Save as MIDI file')

    parser.add_argument('--song-info', action='store_true', help='Print info about song')
    parser.add_argument('--debug', action='store_true', help='Print messages to help with debugging (works only with --midi)')


    args = parser.parse_args()

    tool = GPTools(args.input)
    if args.song_info:
        tool.print_song_info()
        exit()
    if args.track:
        tool.grep_track(*args.track[0])
    if args.measure:
        tool.grep_measures(args.measure[0][0], args.measure[0][1])
    if args.gp5 == False and args.midi == False:
        args.gp5 = True
    if args.gp5:
        tool.save_as_gp(args.output)
    if args.midi:
        tool.save_as_midi(args.output, args.debug)
