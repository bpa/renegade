#!/usr/bin/env python

import getopt, sys
import games
import core

def main():
    opts = {}
    opts['width'] = 640
    opts['height'] = 480
    opts['debug'] = 0
    opts['fullscreen'] = False
    game = process_args(opts)
    core.init(opts)
    core.game = games.load(game)
    core.game.run()

def process_args(opts):
    try:
        optlist, args = getopt.getopt(sys.argv[1:], ":hd:g:f",["help","debug=","geometry=","fullscreen"])
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
        if o in ("-f", "--fullscreen"):
            opts['fullscreen'] = True
    if len(args) != 1:
        print_usage_and_exit()
    return args[0]

def print_usage_and_exit():
    print "Usage: renegade.py [-hf] [-d debug level] [-g WIDTHxHEIGHT] game"
    sys.exit(2)

main()
