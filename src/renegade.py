#!/usr/bin/env python

import pygame
from pygame.locals import *
import getopt, sys
import conf

def main():
    opts = {}
    opts['height'] = 352
    opts['width'] = 352
    opts['debug'] = 0
    game = process_args(opts)

    sys.path.append(conf.RENEGADE_BASE)
    import games
    games.run(game,opts)

def process_args(opts):
    try:
        optlist, args = getopt.getopt(sys.argv[1:], ":hd:g:",["help","debug=","geometry="])
    except getopt.GetoptError:
        print_usage_and_exit()
    for o, val in optlist:
        if o in ("-h","--help"):
            print_usage_and_exit()
        if o in ("-d","--debug"):
            opts['debug'] = val
        if o in ("-g", "--geometry"):
            dimensions = val.split("x")
            opts['width'] = int(dimensions[0])
            opts['height'] = int(dimensions[1])
    if len(args) != 1:
        print_usage_and_exit()
    return args[0]

def print_usage_and_exit():
    print "Usage: renegade.py [-h] [-d debug level] [-g WIDTHxHEIGHT] game"
    sys.exit(2)

main()
