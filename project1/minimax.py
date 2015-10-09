from sef import *
from helpers import *
import time
# from AnimalChecker import get_actual_neighbor

def other_player(player, game):
    ''' return the opponent player, used for minimax'''
    for p in game.players:
        if player != p:
            return p

def _sef(board, player, opponent):
    '''
        F(s) = g(s) + h(s) + k(s)
        g = linear distance from den
        k = distance from capturable enemies
        a = number of piece alive
        for each measure
            the actual value is , value for current player minus value of opponent
    '''

    res = 0
    res += 10 * apply_to_both(board, [player, opponent], remaining_pieces)
    # # sum of the linear distance from each piece to the opponent den
    # res += 3 * apply_to_both(board, [player, opponent], distance_from_den)
    # # sum of the linear distance from each piece to their respective pray
    # res += 15 * apply_to_both(board, [player, opponent], distance_from_all_prays)

    _res = 2 * hunting_mode(player, opponent, 'mouse')
    _res += 2 * hunting_mode(player, opponent, 'wolf')
    # _res += 5 * hunting_mode(player, opponent, 'tiger')
    _res += 5 * hunting_mode(player, opponent, 'elephant')
    print res + _res
    return res + _res

def available_moves(game, player, str_coordinate=None):
    moves = []
    for _animal in player:
        if _animal not in ['name', 'den']:
            _ani = player.__dict__['' + _animal]

            if str_coordinate:
                if not _ani.is_dead:
                    moves += [(_animal,) + move for move in get_actual_neighbor(*_ani._row_col_location) if _ani > game._board[move[0] - 1][move[1] - 1]]
            else:
                if not _ani.is_dead:
                    moves += [(_animal,) + move for move in get_actual_neighbor(str_loc=_ani.location) if _ani > game._board[move[0] - 1][move[1] - 1]]
        # print moves
        # moves += [move for move in _moves if _ani > game._board[move[][0] - 1][item[1] - 1]]]
        # print moves
    return moves


def get_actual_neighbor(cur_row=0, cur_col=0, str_loc=None):
    if str_loc:
        cur_row, cur_col = get_xy_coordinates(str_loc)
    _neighbor = {
        'left': (cur_row, cur_col - 1) if in_board(cur_row, cur_col - 1) else None,
        'up': (cur_row - 1, cur_col) if in_board(cur_row - 1, cur_col) else None,
        'right': (cur_row, cur_col + 1) if in_board(cur_row, cur_col + 1) else None,
        'down': (cur_row + 1, cur_col) if in_board(cur_row + 1, cur_col) else None,
    }
    neighbor = []
    [neighbor.append(item) for item in _neighbor.values() if item]
    return neighbor

count = 0
def minimax(game, level, depth, player, currentMove):
    '''
    game = node - current board state
    '''
    global count
    count += 1
    __move = None
    value = None
    rval =  None
    rmov = None
    children = available_moves(game, player)
    # time.sleep(2)
    # print children, level
    # game.display_board()
    print "%s at level %s - after last move %s \n\n available moves(children) : \n\t\t%s" %(player.name, level, currentMove, children)
    if level == depth:
        print "LEAF LEVEL"
        _sef_ref = _sef(game, player, other_player(player, game))
        print "SEF =%s" % _sef_ref
        return _sef_ref, currentMove
    elif level%2 == 0:  # MAXIMIZING NODE
        value = -1000
        for idx, child in enumerate(children):  # child is a move  for the current player ('tiger', 4, 3)
            print "******************=START Exploring Child = %s(sef val = %s)=======================>" % (child, value)
            status = game._move(player[child[0]], new_row=child[1], new_col=child[2])
            print 'status' , status
            if status:
                # print "current move =  ", child
                rval, rmov = minimax(game, level + 1, depth, other_player(player, game), child)
                children[idx] += (rval,)
                if (rval > value):
                    value = rval
                    final_children = children[idx]
                    # __move = rmov
                game.undo()
                # game.is_gameover = False
                    # self.is_gameover = False

            else:
                print "Child %s [%s] skiped - This animal can't perform that move " % (child, player.name)
            print "******************=DONE Exploring Child = %s(sef val = %s)=======================>" % (child, value)

        # final_children = [child for child in children if child[3] != None]  # remove non visited children
        # final_children.sort(key=lambda tup: tup[3], reverse=True)  # put max node up front
        print "MAXIMIZING\n\n", children, "\n\nactual move\n\n", final_children,"\n\n"
    else:  # MINIMIZING NODE
        value = 1000
        for idx, child in enumerate(children):
            # print "odd level", player.name, child
            print "******************=START Exploring Child = %s(sef val = %s)=======================>" % (child, value)
            if game._move(player[child[0]], new_row=child[1], new_col=child[2]):
                rval, rmov = minimax(game, level + 1, depth, other_player(player, game), child)
                children[idx] += (rval,)
                if (rval < value):
                    value = rval
                    final_children = children[idx]
                    # __move = rmov
                game.undo()
            else:
                print "Child %s [%s] skiped - This animal can't perform that move " % (child, player)
            print "******************=DONE Exploring Child = %s(sef val = %s)=======================>" % (child, value)
        # final_children = [child for child in children if child[3] != None]  # remove non visited children
        # final_children.sort(key=lambda tup: tup[3])  # put min node up front
        print "MINIMIZING\n\n", children, "\n\nactual move\n\n", final_children,"\n\n"

    game.is_gameover = False
    print "value = %s - child =  %s" % (level, player.name)
    return value, final_children


if __name__ == '__main__':
    from AnimalChecker import *
    # from helpers import get_actual_neighbor, in_board
    # from sef import _sef, StageEvaluationBoard

    game = AnimalChecker(rows=9, cols=7, starting_player=1)
    game.setup()
    p1, p2 = game.get_players()


    game.display_board()
    _, bestMove = minimax(game, 0, 3, p1, None)
    bestMove = (p1[bestMove[0]], None,)+bestMove[1:-1]
    print "Best move = ",bestMove
    print game._move(*bestMove)


    _, bestMove = minimax(game, 0, 4, p2, None)
    bestMove = (p2[bestMove[0]], None,)+bestMove[1:-1]
    print bestMove
    print game._move(*bestMove)

    # bestMove = (p2[bestMove[0]], None,)+bestMove[1:]
    # print game._move(*bestMove)
    game.display_board()
    # print minimax(game, 0, 2, p1)
    print 'number of nodes in tree', count  # (14^(6)-1)/(14-1) =  579 195 node to check


