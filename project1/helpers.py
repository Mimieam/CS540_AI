def get_xy_coordinates(xy):
    if isinstance(xy, tuple):
        return xy
    x = None
    # print xy
    try:
        if 1 <= int(xy[0]) < 8:
            x = xy[0]
        else:
            raise IndexError
        y = xy[1]
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        return (int(x), arr.index(y) + 1)
    except (ValueError, IndexError, TypeError, KeyError):
        raise Exception("Could not convert input (%s) to {row, col} coordinates" % str(xy))


def in_board(row, col):
    in_row = (1 <= int(col) < 8)
    in_col = (1 <= int(row) < 10)
    res = in_row and in_col
    # print "in row (1 <= (row:%s) < 8) = %s , (1 <= (col:%s) < 10) = %s  " %
    # (row, in_row, col, in_col)
    return res


def get_actual_neighbor(cur_row=0, cur_col=0, str_loc=None):
    if str_loc:
        cur_row, cur_col = get_xy_coordinates(str_loc)[::-1]
    _neighbor = {
        'left': (cur_row, cur_col - 1) if in_board(cur_row, cur_col - 1) else None,
        'up': (cur_row - 1, cur_col) if in_board(cur_row - 1, cur_col) else None,
        'right': (cur_row, cur_col + 1) if in_board(cur_row, cur_col + 1) else None,
        'down': (cur_row + 1, cur_col) if in_board(cur_row + 1, cur_col) else None
    }
    neighbor = []
    [neighbor.append(item) for item in _neighbor.values() if item]
    return neighbor



def node(state_str="", children=[]):
    '''An Node state_str is the current_state (the position of all the player in the board as a string

    '''
    return {"state": state_str, "children": children}


def get_board_string_state(game):
    return game.display_board(raw=True).replace('   ', '.')\
    .replace(' ', '').replace('den','d').replace('DEN','D')\
    .replace('|','').replace('*', '').strip()


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
