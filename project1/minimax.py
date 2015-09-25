{
'state_str': '',
'value': None,
'content': {
    'player2': {'tiger': (2, 3), 'mouse': (1, 2), 'wolf': (2, 5), 'elephant': (1, 6)},
    'player1': {'tiger': (4, 3), 'mouse': (9, 6), 'wolf': (8, 3), 'elephant': (9, 2)}
  },
'children': {

  }
}

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

    '''
    res = 0
    # sum of the remaining piece
    animal_alive=0
    for _animal in player:
        if not player[_animal].is_dead:
            animal_alive +=1
    print animal_alive
    res += animal_alive

    # sum of the linear distance from each piece to the opponent den
    distance_from_den = 0
    for _animal in player:
        if player[_animal].is_dead:
            continue
        print "[%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, opponent.den, player[_animal].distance_from(opponent.den))
        distance_from_den += player[_animal].distance_from(opponent.den)
    print distance_from_den
    res += distance_from_den

    distance_from_all_prays = 0
    for _animal in player:
        if player[_animal].is_dead:
            continue
        for pray in opponent:
            print "[%s]%s to [%s]%s = %s" % ( player.name, _animal, opponent.name, pray, player[_animal].distance_from(opponent[pray]))
        distance_from_all_prays += player[_animal].distance_from(opponent[pray])
    print distance_from_all_prays

    # sum of the linear distance from each piece to their respective pray


    res = animal_alive + distance_from_den + distance_from_all_prays
    return res

def available_moves(player, str_coordinate=None):
        moves = []
        for _animal in player:
            if _animal not in ['name', 'den']:
                _ani = player.__dict__['' + _animal]

                if str_coordinate:
                    if not _ani.is_dead:
                        moves += [(_animal,) + move for move in get_actual_neighbor(*_ani._row_col_location)]
                else:
                    if not _ani.is_dead:
                        moves += [(_animal,) + move for move in get_actual_neighbor(str_loc=_ani.location)]
        # print mdoves
        return moves

count = 0
def minimax(node, level, depth, player):
    global count
    count += 1
    # print type(node), player, level, depth
    value = None
    rval =  None
    children = available_moves(player)

    if level == depth:
        print "Leaf level reached", player.name
        return _sef(node, player, other_player(player, game))
    elif level%2 == 0:
        value = -1000
        for child in children:  # child is a move  for the current player ('tiger', 4, 3)
            print "even level", player.name, child
            game._move(player[child[0]], new_row=child[1], new_col=child[2])
            game.display_board()
            rval = minimax(game, level + 1, depth, other_player(player, game))
            if (rval > value):
                value = rval
            game.undo()
    else:
        value = 1000
        for child in children:
            print "odd level", player.name, child
            game._move(player[child[0]], new_row=child[1], new_col=child[2])
            rval = minimax(game, level + 1, depth, other_player(player, game))
            if (rval < value):
                value = rval
            game.undo()
    return value


if __name__ == '__main__':
    from AnimalChecker import *
    from helpers import get_actual_neighbor, in_board
    # from sef import _sef, StageEvaluationBoard

    game = AnimalChecker(rows=9, cols=7, starting_player=1)
    game.setup()
    p1, p2 = game.get_players()
    game.display_board()
    print minimax(game, 0, 2, p1)
    print 'number of nodes in tree', count  # (14^(6)-1)/(14-1) =  579 195 node to check


