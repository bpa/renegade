import sys

def run(game_name, opts):
    try:
        exec "import games.%s" % game_name
    except ImportError:
        print "%s is not an available game" % game_name
        sys.exit()
    exec "game = games.%s.%s(opts)" % (game_name, game_name)
    game.run()
