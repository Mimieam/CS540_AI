from sef import *
from sef2 import *
from helpers import *
import time
import traceback
# from AnimalChecker import get_actual_neighbor

def other_player(player, game):
    ''' return the opponent player, used for alphaBetaMinimax'''
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

        positive metrics
        - how close is the enemie from my DEN
        - can i capture anyone?

        negative metrics
        - can i be captured ?

    '''

    res = 0

    # # good for me
    # dist = distance_from_den(player, opponent)
    # print "\tdistance_from_den = %s" % dist
    # rem = remaining_pieces(player, None)
    # print "\tremaining_pieces = %s" % rem
    # cap = can_capture(player, opponent)
    # print "\tcan_capture = %s" % cap

    # res -= dist
    # res += rem
    # res += cap

    # # good for opponent
    # # res -=  5*in_danger(player, opponent, "tiger")
    # # res += distance_from_den(opponent, player)
    # # res -= remaining_pieces(opponent, None)
    # # res += can_capture(player, opponent)
    # can_cap = can_be_captured(player, opponent)
    # print "\tcan_be_captured = %s" % can_cap
    # res -= can_cap # return netagive number

    res += piece_importance(player, opponent, "tiger")
    res += piece_importance(player, opponent, "elephant")
    res += piece_importance(player, opponent, "mouse")
    res += piece_importance(player, opponent, "wolf")
    # res -= can_capture(opponent, player)



    # res += 10 * apply_to_both(board, [player, opponent], remaining_pieces)
    # # sum of the linear distance from each piece to the opponent den
    # res += apply_to_both(board, [player, opponent], distance_from_den)
    # res +=  5*in_danger(player, opponent, "elephant")
    # res +=  2*in_danger(player, opponent, "mouse")
    # res +=  2*in_danger(player, opponent, "wolf")
    # # sum of the linear distance from each piece to their respective pray
    # res += 15 * apply_to_both(board, [player, opponent], distance_from_all_prays)

    # res += 2 * hunted(player, opponent)
    # res += 2 * hunting_mode(player, opponent, 'mouse')
    # _res += 2 * hunting_mode(player, opponent, 'wolf')
    # _res += 5 * hunting_mode(player, opponent, 'tiger')
    # _res += 5 * hunting_mode(player, opponent, 'elephant')

    print "INSIDE SEF>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> = ", res
    return res

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

    moves.sort(key=lambda tup: tup[0], reverse=False)
    moves.sort(key=lambda tup: tup[1], reverse=False)  # prioritize going down
    # print moves.sort(key=lambda tup: tup[2], reverse=False)
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

    # print neighbor
    neighbor.sort(key=lambda tup: tup[0], reverse=False)

    return neighbor

count = 0

TRANSPOSITION_TABLE = {

}

def alphaBetaMinimax(game, alpha, beta, level, depth, player, currentMove):
    '''
    game = node - current board state
    '''
    str_state = get_board_string_state(game)
    if str_state in TRANSPOSITION_TABLE :
        # print TRANSPOSITION_TABLE[str_state]
        if currentMove != None:
            # print "STATE FOUND IN TRANSPOSITION_TABLE", str_state
            return TRANSPOSITION_TABLE[str_state][0], currentMove
    try:
        global count
        count += 1
        final_children = None
        value = None
        rval =  None
        # rmov = None
        children = available_moves(game, player)
        # time.sleep(2)
        # print children, level
        # game.display_board()
        # print "%s at level %s - after last move %s \n\n available moves(children) : \n\t\t%s" %(player.name, level, currentMove, children)
        if level == depth:
            print "LEAF LEVEL"
            _sef_ref = _sef(game, player, other_player(player, game))
            # print  "CURRENT PLAYER = ", player.name,"SEF =%s" % _sef_ref
            TRANSPOSITION_TABLE[get_board_string_state(game)] = (_sef_ref, currentMove)
            return _sef_ref, currentMove
        elif level%2 == 0:  # MAXIMIZING NODE
            value = -1000
            for idx, child in enumerate(children):  # child is a move  for the current player ('tiger', 4, 3)
                # print "CURRENT PLAYER = ", game._find_whose_turn()
                # print "******************=START Exploring Child = %s(sef val = %s) GAME PLY= %s =======================>" % (child, value, game.plys)
                status = game._move(player[child[0]], new_row=child[1], new_col=child[2])
                # print 'status' , status
                if status:
                    rval, rmov = alphaBetaMinimax(game, value, 1000,level + 1, depth, other_player(player, game), child)
                    children[idx] += (rval,)
                    if (rval >= value):
                        value = rval
                        final_children = children[idx]
                        TRANSPOSITION_TABLE[get_board_string_state(game)] = (value, children[idx])
                    game.undo()

                else:
                    print "Child %s [%s] skiped - This animal can't perform that move " % (child, player.name)
                # print "******************=DONE Exploring Child = %s(sef val = %s) GAME PLY= %s =======================>" % (child, value, game.plys)
            print "MAXIMIZING Node @ lvl %s=> %s\n\t %s" %(level, children, final_children)
        else:  # MINIMIZING NODE
            value = 1000
            for idx, child in enumerate(children):
                # print "odd level", player.name, child
                # print "CURRENT PLAYER = ", game._find_whose_turn()
                # print "******************=START Exploring Child = %s(sef val = %s)=======================>" % (child, value)
                status = game._move(player[child[0]], new_row=child[1], new_col=child[2])
                # print 'status' , status
                if status:
                    rval, rmov = alphaBetaMinimax(game, -1000 , value, level + 1, depth, other_player(player, game), child)
                    children[idx] += (rval,)
                    if (rval <= value):
                        value = rval
                        final_children = children[idx]
                        # TRANSPOSITION_TABLE[get_board_string_state(game)] = (value, children[idx])
                        # __move = rmov
                    game.undo()
                else:
                    print "Child %s [%s] skiped - This animal can't perform that move " % (child, player)
                # print "******************=DONE Exploring Child = %s(sef val = %s)=======================>" % (child, value)
            print "MINIMIZING Node  @ lvl %s=> %s\n\t %s" %(level,children, final_children)

        game.is_gameover = False
        # print "value = %s - child =  %s" % (level, player.name)
        print 'number of nodes visited in tree', count  # (14^(6)-1)/(14-1) =  579 195 node to check

        return value, final_children
    except Exception, e:
        print traceback.format_exc(e)
        # print "node examined ", count

if __name__ == '__main__':
    from AnimalChecker import *
    # from helpers import get_actual_neighbor, in_board
    # from sef import _sef, StageEvaluationBoard

    game = AnimalChecker(rows=9, cols=7, starting_player=1)
    game.setup()
    p1, p2 = game.get_players()


    game.display_board()
    _, bestMove = alphaBetaMinimax(game, 0, 3, p1, None)
    bestMove = (p1[bestMove[0]], None,)+bestMove[1:-1]
    print "Best move = ",bestMove
    print game._move(*bestMove)


    _, bestMove = alphaBetaMinimax(game, 0, 4, p2, None)
    bestMove = (p2[bestMove[0]], None,)+bestMove[1:-1]
    print bestMove
    print game._move(*bestMove)

    # bestMove = (p2[bestMove[0]], None,)+bestMove[1:]
    # print game._move(*bestMove)
    game.display_board()
    # print alphaBetaMinimax(game, 0, 2, p1)
    print 'number of nodes in tree', count  # (14^(6)-1)/(14-1) =  579 195 node to check


