#!/usr/bin/env python

import pygame
from pygame.locals import *
import getopt, sys

def main():
    game = None
    opts = {}
    opts['height'] = 352
    opts['width'] = 352
    opts['debug'] = 0

    process_args(opts)
    try:
        exec ("from %s import *" % opts['game'])
        exec ("game = %s(opts)" % opts['game'])
    except ImportError:
        print "%s is not an available game" % opts['game']
        sys.exit()
    except:
        print "%s has errors, add debug to see why" % opts['game']
        if opts['debug']:
            print "Error: ", sys.exc_type, sys.exc_value
        sys.exit()
    game.run()

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
    opts['game'] = args[0]

def print_usage_and_exit():
    print "Usage: renegade.py [-h] [-d debug level] [-g WIDTHxHEIGHT] game"
    sys.exit(2)

main()
