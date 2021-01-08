#!/usr/bin/python

import argparse
from GPMIDI import GP2Midi 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert GuitarPro: GP3, GP4, GP5 files to MIDI')

    parser.add_argument('-i', '--input',
                        help='Path to GP* file',
                        metavar='', required=True)

    parser.add_argument('-t', '--track', type=int,
                        help='Track number',
                        metavar='', required=False, default=-1)

    parser.add_argument('-f', '--first_measure', type=int,
                        help='From what bar start converting',
                        metavar='', required=False, default=1)

    parser.add_argument('-l', '--last_measure', type=int,
                        help='Measure on which finish converting',
                        metavar='', required=False, default=-1)

    parser.add_argument('-o', '--output', type=str,
                        help='Name of output file',
                        metavar='', required=False, default='output')

    args = parser.parse_args()

    obj = GP2Midi(args.input, args.track, args.first_measure, args.last_measure, args.output)
    obj.convert2Midi()