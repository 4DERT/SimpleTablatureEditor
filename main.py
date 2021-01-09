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

    parser.add_argument('-m', '--measure', action='append',nargs=2, type=int,
                        help='Select measures', metavar='num')

    parser.add_argument('-o', '--output', type=str,
                        help='Name of output file',
                        metavar='', required=False, default='output')
    
    parser.add_argument('--verbose', action='store_true', help='Print verbose')

    args = parser.parse_args()

    obj = GP2Midi(args.input, args.track, args.measure[0][0], args.measure[0][1], args.output, args.verbose)
    obj.convert2Midi()