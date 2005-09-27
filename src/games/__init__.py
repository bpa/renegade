import sys
import games

def load(game_name,opts):
    game = None
    module = "games.%s" % game_name
    try:
        game = __import__(module,None,None,module)
    except ImportError:
        print "%s is not an available game" % game_name
        sys.exit()
    constructor = getattr(game,game_name)
    return constructor(opts)
