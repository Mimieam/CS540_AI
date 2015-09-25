import random
import copy
from helpers import get_actual_neighbor, in_board

# This class create a deepCopy of our board object and
# add the undo functionality to it
# now we can make any change in your staged board
# without affecting the original one.

# board state = position of each players element
# player1[(T,2,3),(M,3,1), (E,2,4), (W, None,None)]  -> wolf dead
# player2[(t,6,3),(m,6,1), (e,6,4), (w, None,None)]  -> wolf dead

class Node(object):
    def __init__(self, state=None, children=[], value=None):
        self.state = state
        self.children = children
        self.value = value

    def __iter__(self):
        return iter(self.children)



class StageEvaluationBoard(object):
    """ a shallow board game """
    def __init__(self, game, current_board):
        self._board = current_board
        self.game = game

    def get_board_string_state(self):
        return self.game.display_board(raw=True).replace('   ', '.')\
        .replace(' ', '').replace('den','d').replace('DEN','D')\
        .replace('|','').replace('*', '').strip()

    def get_root_node(self, player):
        board_str = self.game.display_board(raw=True)
        return {
            "state_str": self.get_board_string_state(),
            "children": self.generate_children_nodes(player),
            "value":None
        }

    def get_board_state(self, game):
        # return position of each elements in the game
        player1, player2 = {}, {}
        for player in game.players:
            for _animal in player:
                if _animal not in ['name', 'den']:
                    if player.name.lower() == 'player1':
                        # print player.name, _animal, player.__dict__['' + _animal]._row_col_location
                        player1['' + _animal] = player.__dict__['' + _animal]._row_col_location
                    else:
                        player2['' + _animal] = player.__dict__['' + _animal]._row_col_location
        return {
            'player1': player1,
            'player2': player2
        }

    def generate_children_nodes(self, player):
        children = []
        move_list = self.available_moves(player, str_coordinate=True)
        for item in move_list:
            print move_list[item]
            for new_location in move_list[item]:
                # print'[%s]%s' % (item, new_location)
                # print game.players[0][item], new_location
                # print in_board(*new_location)
                self.game._move(self.game.players[0][item], new_location, new_row=new_location[0], new_col=new_location[1])
                child = {
                    "state_str": "",
                    "children": self.get_board_state(self.game),
                    "value":None
                }
                children += [child]
                self.minimax(child, 0, 3, self.other_player(player))
                self.game.undo()
        return children

    # def make_move(self, who, where):
    #     self.game.move(who, where)

    # def undo_move(self):
    #     self.game.undo()

    def available_moves(self, player, str_coordinate=None):
        moves = {}
        for _animal in player:
            if _animal not in ['name', 'den']:
                _ani = player.__dict__['' + _animal]
                if str_coordinate:
                    moves['' + _animal] = get_actual_neighbor(*_ani._row_col_location)
                else:
                    moves['' + _animal] = get_actual_neighbor(str_loc=_ani.location)
        return moves

    def other_player(self, player):
        ''' return the opponent player, used for minimax'''
        for p in self.game.players:
            if player != p:
                return p

    def minimax(self, node, level, depth, player):
        '''
            a node is a board state
            children of a nodes are other board states
            node = {
                "state_str": "",
                "children": [{
                        "state_str": "",
                        "children": [],
                        "value":None
                    },
                    {
                        "state_str": "",
                        "children": [],
                        "value":None
                    }],
                "value":None
            }
        '''
        print type(node), player, level, depth
        # player = self.game.players
        # node['children'] = self.generate_children_nodes(player)
        print node

        value = None
        rval =  None
        if level == depth:
            print "Leaf level reached"
            self._sef(node)
        elif level%2 == 0:  # current player
            value = -1000
            print "********************"
            # for child in node:
            move_list = self.available_moves(player, str_coordinate=True)
            for pawn in move_list:
                print move_list[pawn]
                for loc in move_list[pawn]:
                    print'[%s]%s' % (pawn, loc)
                    self.game._move(player[pawn], loc, new_row=loc[0], new_col=loc[1])
                    # Node(
                    #     state="",
                    #     children=self.get_board_state(self.game),
                    #     value=None
                    # )
                    # print Node
                    rval = self.minimax(child, 0, 3, self.other_player(player))
                    if (rval > value):
                        value = rval
                    self.game.undo()

            print "********************"
            print "even branch", player.name, child

        else:  # opponent
            value = 1000
            for child in node:
                print "odd branch", player.name, child
                rval = self.minimax(child, level + 1, depth, self.other_player(player))
                if (rval < value):
                    value = rval
        return value

    def _sef(self, board_state):
        ##
        # compute distance from every object to den
        return 1


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
        # pop a dictionary representing the last move
        last_move = self.move_log.pop()
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

    def get_board_from_player(self, _raw=True):
        staged_board = []
        for row in xrange(0, self.game.rows):
            staged_board.append([])
            for col in xrange(0, self.game.cols):
                staged_board[row].append('   ')

        for player in self.game.players:
            for _animal in player.__dict__ :
                if _animal not in ['name']:
                    r, c = player.__dict__[''+_animal]._row_col_location
                    # print r, c
                    # print [(player.__dict__[''+_animal]._row_col_location, player.__dict__[''+_animal])for _animal in player.__dict__ if _animal not in ['name']]
                    staged_board[r-1][c-1] = player.__dict__[''+_animal]
        # print staged_board

        self.game.display_board(_board=staged_board, raw=_raw)

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
    from AnimalChecker import *
    print sef("")
    print _sef("")
    game = AnimalChecker(rows=9, cols=7, starting_player=1)
    game.setup()
    p1, p2 = game.get_players()


    stage_board = StageEvaluationBoard(game, game._board)

    # test opposite player
    print stage_board.other_player(p2), p1


    # # print stage_board.generate_children_nodes(p1)
    print stage_board.minimax(stage_board.get_root_node(p1),0, 2, p1)
