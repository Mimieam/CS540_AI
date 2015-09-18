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


# this class sole purpose is to keep track of which move just happened
# component of the man  Animal checker class
class move_tracker(object):
    def __init__(self, game):
        self.game = game
        self.curr_move = {}
        self.move_log = []

    def __repr__(self):
        return " last move = %s" % self.curr_move

    def update(self, _who, _from, _where, _captured_animal=None):
        self.curr_move = {
            'who': _who,
            'from': _from,
            'where': _where,
            'captured': _captured_animal,
        }

        # append at the end
        self.move_log.append(self.curr_move)
        print "(%s)[%s] moved from %s to %s, old content = {%s}" % (_who, _who.owner, _from, _where, _captured_animal)

    def free_captured(self):
        self.captured.is_dead = False

    def revert(self):
        ''' return the reverted move'''
        print "rewinding last move..."
        # undo a move
        if not self.move_log:
            print "No move to rewind"
            return
        last_move = self.move_log.pop()  # pop a dictionary representing the last move
        self.game._move_animal(last_move['who'], last_move['from'])
        # revive any Ghost
        if last_move['captured'] and not isinstance(last_move['captured'], str):
            last_move['captured'].is_dead = False
            self.game._move_animal(last_move['captured'], last_move['where'])

        self.curr_move = self.move_log[-1] if self.move_log else []
        self.game.plys -= 1
        return last_move

    def get_move_log(self):
        return self.move_log


#
# board string rep = sef value
#
TRANSPOSITION_TABLE = { }

def _sef(current_game_state):
    # _board_repr = current_game_state.display_board()
    _board_repr = """
   | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
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
            # print 'initial =>', id(current_game_state)
        current_game = copy.deepcopy(current_game_state)
        # cp1, cp2 = game_copy.get_players()

    # print 'Copy =>', id(current_game)
    # print current_game_state.get_players(),'\n', current_game.get_players()
        print 'current_game =', current_game
        return current_game


def sef(current_game_state):

    # print 'initial =>', id(current_game_state)
    current_game = copy.deepcopy(current_game_state)
    # print 'Copy =>', id(current_game)
    # print current_game_state.get_players(),'\n', current_game.get_players()
    # print 'current_player =', current_game.players[current_game.plys % 2].name
    animals = ['tiger', 'wolf', 'elephant', 'mouse']
    bestMove = ["down", "up", "left", "right"]
    return (animals[random.randint(0, len(animals) -1)], bestMove[random.randint(0, len(bestMove) -1)])


if __name__ == '__main__':
   print sef("")
   print _sef("")
