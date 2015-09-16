import random
import copy


# This class create a deepCopy of our board object and add the undo functionality to it
# now we can make any change in your staged board without affecting the original one.
class StageEvaluationBoard(object):
    """ a shallow board game """
    def __init__(self, current_board):
        self._board = current_board

    def make_move(self):
        pass

#
# board string rep = sef value
#
TRANSPOSITION_TABLE = { }

def _sef(current_game_state):
    # _board_repr = current_game_state.display_board()
    _board_repr = """   | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
a->|   |   |   |den|   | e |   |
b->|   |   | t |   | w | M |   |
c->|   |   |   |   |   |   |   |
d->|   |   |   |   |   |   |   |
e->|   |   |   |   |   |   |   |
f->|   |   |   |   |   |   |   |
g->|   |   |   |   |   |   |   |
h->|   | m | W |   | T |   |   |
i->|   | E |   |DEN|   |   |   |
"""
    if _board_repr in TRANSPOSITION_TABLE:
        return TRANSPOSITION_TABLE[_board_repr]
    else:
        # run min max algorithm on this board.
        # how far are we from the goal
        #
        pass


def sef(current_game_state):

    # print 'initial =>', id(current_game_state)
    # current_game = copy.deepcopy(current_game_state)
    # print 'Copy =>', id(current_game)
    # print current_game_state.get_players(),'\n', current_game.get_players()
    # print 'current_player =', current_game.players[current_game.plys % 2].name
    animals = ['tiger', 'wolf', 'elephant', 'mouse']
    bestMove = ["down", "up", "left", "right"]
    return (animals[random.randint(0, len(animals) -1)], bestMove[random.randint(0, len(bestMove) -1)])


if __name__ == '__main__':
   print sef("")
   print _sef("")
